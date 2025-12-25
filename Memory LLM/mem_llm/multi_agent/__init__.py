"""
Multi-Agent System for Memory LLM (v2.2.0+)
===========================================

Enables collaborative AI agents that work together to solve complex tasks.

Features:
- Multiple specialized agents with different roles
- Inter-agent communication
- Workflow orchestration
- Shared and private memory spaces

Author: Cihat Emre Karataş
Version: 2.2.0
"""

from .agent_registry import AgentRegistry
from .base_agent import AgentMessage, AgentRole, AgentStatus, BaseAgent
from .communication import CommunicationHub, MessageQueue

__all__ = [
    "BaseAgent",
    "AgentRole",
    "AgentStatus",
    "AgentMessage",
    "AgentRegistry",
    "CommunicationHub",
    "MessageQueue",
]
