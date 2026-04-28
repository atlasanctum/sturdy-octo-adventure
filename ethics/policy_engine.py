"""Policy engine for ethics validation."""

import re
from typing import Dict, Tuple
from sqlalchemy.orm import Session
from data.models import PolicyRule, ActionStatus


class PolicyEngine:
    """Validates actions against defined policies."""

    def __init__(self, db: Session = None):
        """Initialize policy engine."""
        self.db = db
        self.default_policies = [
            ("dangerous_operation", r"(destroy|delete|poison|bomb|harm)", "deny"),
            ("unauthorized_access", r"(steal|hack|breach|penetrate)", "deny"),
            ("humanitarian_health", r"(vaccine|medicine|treatment|health|medical)", "allow"),
            ("humanitarian_finance", r"(fund|allocate|transfer|support)", "allow"),
        ]

    async def validate(self, intent: str, agent_type: str) -> Tuple[bool, str]:
        """
        Validate intent against policies.
        
        Args:
            intent: The user's intent
            agent_type: Type of agent processing the intent
            
        Returns:
            (is_authorized, reason)
        """
        # Load policies from database or use defaults
        policies = self._get_policies()
        
        # Check against each policy
        for policy_name, pattern, action in policies:
            if re.search(pattern, intent, re.IGNORECASE):
                if action == "deny":
                    return (False, f"Policy violation: {policy_name}")
                else:
                    return (True, f"Authorized by policy: {policy_name}")
        
        # Default: allow humanitarian operations
        if agent_type == "health":
            return (True, "Authorized: Health operations permitted")
        elif agent_type == "finance":
            return (True, "Authorized: Finance operations permitted")
        
        # Default deny for unknown operations
        return (False, "No matching policy found")

    def _get_policies(self) -> list:
        """Get policies from database or return defaults."""
        if self.db:
            try:
                rules = self.db.query(PolicyRule).all()
                return [(r.rule_name, r.rule_pattern, r.action) for r in rules]
            except Exception:
                pass
        
        return self.default_policies
