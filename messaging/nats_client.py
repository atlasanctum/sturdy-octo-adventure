"""NATS messaging client for event publishing."""

import json
import os
from typing import Dict, Any, Optional
import asyncio


class NATSClient:
    """Client for publishing events to NATS."""

    def __init__(self):
        """Initialize NATS client."""
        self.nats_url = os.getenv("NATS_URL", "nats://nats:4222")
        self.connection = None
        self.is_connected = False

    async def connect(self) -> bool:
        """Connect to NATS server."""
        try:
            import nats
            self.connection = await nats.connect(self.nats_url)
            self.is_connected = True
            print(f"Connected to NATS at {self.nats_url}")
            return True
        except ImportError:
            # NATS package not installed, use mock
            print("Warning: nats-py not installed, using mock NATS client")
            self.is_connected = False
            return False
        except Exception as e:
            print(f"Failed to connect to NATS: {e}")
            self.is_connected = False
            return False

    async def publish_action(self, action_event: Dict[str, Any]) -> bool:
        """
        Publish an action event to NATS.
        
        Args:
            action_event: Event data to publish
            
        Returns:
            Success status
        """
        try:
            if self.connection and self.is_connected:
                subject = "actions.executed"
                message = json.dumps(action_event).encode()
                await self.connection.publish(subject, message)
                return True
            else:
                # Mock publishing for development
                print(f"[NATS Mock] Published to 'actions.executed': {action_event}")
                return True
        except Exception as e:
            print(f"Failed to publish event: {e}")
            return False

    async def subscribe(self, subject: str, callback):
        """Subscribe to a subject."""
        try:
            if self.connection and self.is_connected:
                await self.connection.subscribe(subject, cb=callback)
        except Exception as e:
            print(f"Failed to subscribe: {e}")

    async def disconnect(self):
        """Disconnect from NATS."""
        if self.connection:
            await self.connection.close()
            self.is_connected = False


# Global instance
_nats_client: Optional[NATSClient] = None


async def get_nats_client() -> NATSClient:
    """Get or create NATS client."""
    global _nats_client
    if _nats_client is None:
        _nats_client = NATSClient()
        await _nats_client.connect()
    return _nats_client
