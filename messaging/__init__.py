"""Messaging module."""

from messaging.nats_client import NATSClient, get_nats_client

__all__ = ["NATSClient", "get_nats_client"]
