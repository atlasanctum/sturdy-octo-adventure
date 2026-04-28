"""FastAPI gateway for Atlas Sanctum OS."""

import os
import json
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session

from data.database import init_db, get_db
from data.models import ActionLog, ActionStatus
from orchestration.orchestrator import Orchestrator
from ethics.policy_engine import PolicyEngine
from messaging.nats_client import get_nats_client
from blockchain.blockchain_client import get_blockchain_client

# Initialize app
app = FastAPI(
    title="Atlas Sanctum OS API",
    description="AI-agent orchestration with ethics engine and blockchain audit",
    version="1.0.0"
)

# Global instances
orchestrator = Orchestrator()


class IntentRequest(BaseModel):
    """Intent request model."""
    intent: str
    metadata: Optional[dict] = {}


class IntentResponse(BaseModel):
    """Intent response model."""
    action_id: int
    status: str
    agent_type: str
    data: dict
    message: str


async def execute_action_async(
    action_log: ActionLog,
    db: Session,
    intent: str,
    metadata: dict
):
    """Execute action asynchronously."""
    try:
        # Process with orchestrator
        result = await orchestrator.process(intent, metadata)
        
        if not result or not result.success:
            action_log.status = ActionStatus.FAILED
            action_log.result = result.error if result else "Unknown error"
        else:
            action_log.status = ActionStatus.EXECUTED
            action_log.result = json.dumps(result.data)
        
        action_log.executed_at = datetime.utcnow()
        
        # Publish to NATS
        nats = await get_nats_client()
        event = {
            "action_id": action_log.id,
            "intent": intent,
            "agent_type": result.action_type if result else "unknown",
            "status": action_log.status.value,
            "timestamp": datetime.utcnow().isoformat(),
            "data": result.data if result else {},
        }
        await nats.publish_action(event)
        
        # Log to blockchain
        blockchain = await get_blockchain_client()
        tx_hash = await blockchain.log_action(
            action=intent,
            metadata=event,
            tx_hash=f"0x{action_log.id:064x}"
        )
        action_log.blockchain_tx_hash = tx_hash
        
        db.commit()
    except Exception as e:
        action_log.status = ActionStatus.FAILED
        action_log.result = str(e)
        action_log.executed_at = datetime.utcnow()
        db.commit()


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()
    print("✓ Database initialized")
    print("✓ Atlas Sanctum OS Gateway started")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Atlas Sanctum OS - Intent Gateway",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/agents")
async def list_agents():
    """List available agents."""
    return {
        "agents": orchestrator.list_agents()
    }


@app.post("/intent", response_model=IntentResponse)
async def process_intent(
    request: IntentRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Process a user intent through the system.
    
    Flow:
    1. Validate intent with ethics engine
    2. Log action to database
    3. Route to appropriate agent
    4. Publish event to NATS
    5. Log to blockchain
    """
    # Validate intent with ethics engine
    policy_engine = PolicyEngine(db)
    is_authorized, reason = await policy_engine.validate(
        request.intent,
        agent_type="general"
    )
    
    if not is_authorized:
        raise HTTPException(status_code=403, detail=f"Action denied: {reason}")
    
    # Find the agent that will handle this
    selected_agent = orchestrator._select_agent(request.intent)
    agent_type = selected_agent.agent_type if selected_agent else "unknown"
    
    # Create action log entry
    action_log = ActionLog(
        intent=request.intent,
        agent_type=agent_type,
        status=ActionStatus.AUTHORIZED,
        metadata=request.metadata or {},
        created_at=datetime.utcnow()
    )
    db.add(action_log)
    db.commit()
    db.refresh(action_log)
    
    # Execute action asynchronously
    background_tasks.add_task(
        execute_action_async,
        action_log,
        db,
        request.intent,
        request.metadata or {}
    )
    
    return IntentResponse(
        action_id=action_log.id,
        status=ActionStatus.AUTHORIZED.value,
        agent_type=agent_type,
        data={
            "intent": request.intent,
            "queued_for_processing": True
        },
        message="Intent authorized and queued for processing"
    )


@app.get("/actions/{action_id}")
async def get_action(action_id: int, db: Session = Depends(get_db)):
    """Get the status of an action."""
    action = db.query(ActionLog).filter(ActionLog.id == action_id).first()
    
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    
    return {
        "id": action.id,
        "intent": action.intent,
        "agent_type": action.agent_type,
        "status": action.status.value,
        "created_at": action.created_at,
        "executed_at": action.executed_at,
        "result": action.result,
        "blockchain_tx_hash": action.blockchain_tx_hash,
    }


@app.get("/actions")
async def list_actions(db: Session = Depends(get_db), limit: int = 50):
    """List recent actions."""
    actions = db.query(ActionLog).order_by(ActionLog.created_at.desc()).limit(limit).all()
    
    return {
        "count": len(actions),
        "actions": [
            {
                "id": a.id,
                "intent": a.intent,
                "agent_type": a.agent_type,
                "status": a.status.value,
                "created_at": a.created_at,
            }
            for a in actions
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
