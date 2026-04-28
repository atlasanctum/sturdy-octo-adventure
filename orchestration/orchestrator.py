"""Intent orchestrator - routes intents to appropriate agents."""

from typing import Dict, Any, Optional
from agents.base import BaseAgent, ActionResult
from agents.health_agent import HealthAgent
from agents.finance_agent import FinanceAgent


class Orchestrator:
    """Routes intents to the appropriate agent."""

    def __init__(self):
        """Initialize orchestrator with available agents."""
        self.agents: Dict[str, BaseAgent] = {
            "health": HealthAgent(),
            "finance": FinanceAgent(),
        }

    async def process(self, intent: str, metadata: Dict[str, Any]) -> Optional[ActionResult]:
        """
        Process an intent by routing to the appropriate agent.
        
        Args:
            intent: User's natural language intent
            metadata: Additional context
            
        Returns:
            ActionResult from the appropriate agent, or None if no agent can handle
        """
        # Find the best agent for this intent
        selected_agent = self._select_agent(intent)
        
        if not selected_agent:
            return ActionResult(
                success=False,
                action_type="orchestrator",
                data={},
                error=f"No agent available to handle intent: {intent}"
            )
        
        # Process with selected agent
        result = await selected_agent.process(intent, metadata)
        return result

    def _select_agent(self, intent: str) -> Optional[BaseAgent]:
        """Select the best agent for the given intent."""
        # Simple strategy: use first agent that can handle it
        for agent in self.agents.values():
            if agent.can_handle(intent):
                return agent
        
        return None

    def list_agents(self) -> Dict[str, str]:
        """Return available agents and their types."""
        return {
            agent_type: agent.agent_type
            for agent_type, agent in self.agents.items()
        }
