"""Database models for Atlas Sanctum OS."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum

Base = declarative_base()


class ActionStatus(PyEnum):
    """Status of an action."""
    PENDING = "pending"
    AUTHORIZED = "authorized"
    REJECTED = "rejected"
    EXECUTED = "executed"
    FAILED = "failed"


class ActionLog(Base):
    """Log of all actions executed in the system."""
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True, index=True)
    intent = Column(String, nullable=False)
    agent_type = Column(String, nullable=False)
    status = Column(SQLEnum(ActionStatus), default=ActionStatus.PENDING)
    metadata = Column(JSON, nullable=True)
    blockchain_tx_hash = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    executed_at = Column(DateTime, nullable=True)
    result = Column(String, nullable=True)


class PolicyRule(Base):
    """Policy rules for ethics engine."""
    __tablename__ = "policy_rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String, unique=True, nullable=False)
    rule_pattern = Column(String, nullable=False)  # Regex or keyword pattern
    action = Column(String, nullable=False)  # "allow" or "deny"
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
