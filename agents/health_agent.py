"""Health-focused agent for vaccine distribution, medical logistics, etc."""

import re
from typing import Dict, Any
from agents.base import BaseAgent, ActionResult


class HealthAgent(BaseAgent):
    """Agent specializing in health and medical operations."""

    def __init__(self):
        super().__init__("health")
        self.health_keywords = [
            "vaccine", "medical", "health", "disease", "treatment",
            "diagnosis", "hospital", "clinic", "medicine", "patient"
        ]

    async def process(self, intent: str, metadata: Dict[str, Any]) -> ActionResult:
        """Process health-related intents."""
        try:
            # Extract key information from intent
            action_details = self._parse_health_intent(intent)
            
            # Simulate processing
            result_data = {
                "operation_type": action_details["operation"],
                "location": action_details["location"],
                "resource_type": action_details["resource"],
                "status": "queued",
                "processing_timestamp": metadata.get("timestamp"),
            }
            
            return ActionResult(
                success=True,
                action_type=self.agent_type,
                data=result_data
            )
        except Exception as e:
            return ActionResult(
                success=False,
                action_type=self.agent_type,
                data={},
                error=str(e)
            )

    def can_handle(self, intent: str) -> bool:
        """Check if intent contains health keywords."""
        intent_lower = intent.lower()
        return any(keyword in intent_lower for keyword in self.health_keywords)

    def _parse_health_intent(self, intent: str) -> Dict[str, str]:
        """Extract structured data from health intent."""
        # Simple regex-based parsing
        location_match = re.search(r'in\s+([A-Z][a-zA-Z\s]+)', intent)
        location = location_match.group(1) if location_match else "Unknown"
        
        operation = "health_operation"
        if "vaccine" in intent.lower():
            operation = "vaccine_distribution"
        elif "medical" in intent.lower() or "treatment" in intent.lower():
            operation = "medical_support"
        elif "disease" in intent.lower():
            operation = "disease_tracking"
        
        resource = "vaccines" if "vaccine" in intent.lower() else "medical_supplies"
        
        return {
            "operation": operation,
            "location": location,
            "resource": resource
        }
