"""Finance-focused agent for transactions, budget, payments, etc."""

import re
from typing import Dict, Any
from agents.base import BaseAgent, ActionResult


class FinanceAgent(BaseAgent):
    """Agent specializing in financial operations."""

    def __init__(self):
        super().__init__("finance")
        self.finance_keywords = [
            "payment", "transaction", "budget", "fund", "finance",
            "transfer", "money", "cost", "expense", "invoice"
        ]

    async def process(self, intent: str, metadata: Dict[str, Any]) -> ActionResult:
        """Process finance-related intents."""
        try:
            action_details = self._parse_finance_intent(intent)
            
            result_data = {
                "operation_type": action_details["operation"],
                "amount": action_details["amount"],
                "destination": action_details["destination"],
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
        """Check if intent contains finance keywords."""
        intent_lower = intent.lower()
        return any(keyword in intent_lower for keyword in self.finance_keywords)

    def _parse_finance_intent(self, intent: str) -> Dict[str, Any]:
        """Extract structured data from finance intent."""
        # Simple regex-based parsing
        amount_match = re.search(r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)', intent)
        amount = amount_match.group(1) if amount_match else "0"
        
        destination_match = re.search(r'to\s+([A-Z][a-zA-Z\s]+)', intent)
        destination = destination_match.group(1) if destination_match else "Unknown"
        
        operation = "financial_transaction"
        if "payment" in intent.lower():
            operation = "payment"
        elif "transfer" in intent.lower():
            operation = "fund_transfer"
        elif "budget" in intent.lower():
            operation = "budget_allocation"
        
        return {
            "operation": operation,
            "amount": amount,
            "destination": destination
        }
