"""Base agent class."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ActionResult:
    """Result of an agent action."""
    success: bool
    action_type: str
    data: Dict[str, Any]
    error: Optional[str] = None


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(self, agent_type: str):
        """Initialize agent with type identifier."""
        self.agent_type = agent_type

    @abstractmethod
    async def process(self, intent: str, metadata: Dict[str, Any]) -> ActionResult:
        """
        Process an intent and return result.
        
        Args:
            intent: The user's natural language intent
            metadata: Additional context/metadata
            
        Returns:
            ActionResult containing success status and data
        """
        pass

    def can_handle(self, intent: str) -> bool:
        """
        Determine if this agent can handle the given intent.
        Override in subclasses for custom logic.
        """
        return True
