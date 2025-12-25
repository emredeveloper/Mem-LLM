"""
Base Agent Class for Multi-Agent System
========================================

Defines the core agent interface and functionality.

Author: Cihat Emre Karataş
Version: 2.2.0
"""

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Predefined agent roles"""

    GENERAL = "general"  # General purpose agent
    RESEARCHER = "researcher"  # Information gathering
    ANALYST = "analyst"  # Data analysis
    WRITER = "writer"  # Content creation
    VALIDATOR = "validator"  # Quality checking
    COORDINATOR = "coordinator"  # Task coordination


class AgentStatus(Enum):
    """Agent status"""

    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class AgentMessage:
    """Message between agents"""

    sender_id: str
    receiver_id: str
    content: str
    message_type: str = "chat"
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))


class BaseAgent:
    """
    Base class for all agents in the multi-agent system.

    Features:
    - Unique agent ID and name
    - Role-based behavior
    - Memory access (shared/private)
    - Tool access
    - Inter-agent communication
    """

    def __init__(
        self,
        agent_id: Optional[str] = None,
        name: Optional[str] = None,
        role: AgentRole = AgentRole.GENERAL,
        model: str = "rnj-1:latest",
        backend: str = "ollama",
        enable_tools: bool = False,
        private_memory: bool = True,
        **kwargs,
    ):
        """
        Initialize agent.

        Args:
            agent_id: Unique agent identifier (auto-generated if None)
            name: Human-readable agent name
            role: Agent role (determines behavior)
            model: LLM model to use
            backend: LLM backend (ollama, lmstudio)
            enable_tools: Enable tool usage
            private_memory: Use private memory (True) or shared (False)
            **kwargs: Additional arguments for MemAgent
        """
        self.agent_id = agent_id or str(uuid.uuid4())
        self.name = name or f"{role.value}-{self.agent_id[:8]}"
        self.role = role
        self.status = AgentStatus.IDLE
        self.private_memory = private_memory

        # Import here to avoid circular dependency
        from ..mem_agent import MemAgent

        # Create underlying MemAgent
        self.mem_agent = MemAgent(
            model=model,
            backend=backend,
            enable_tools=enable_tools,
            **kwargs,
        )

        # Set user ID for memory isolation
        memory_user = self.agent_id if private_memory else "shared_agent_memory"
        self.mem_agent.set_user(memory_user)

        # Message inbox
        self.inbox: List[AgentMessage] = []

        # Conversation history with other agents
        self.conversation_history: List[Dict[str, Any]] = []

        logger.info(f"🤖 Agent created: {self.name} (ID: {self.agent_id}, Role: {role.value})")

    def process(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process a task.

        Args:
            task: Task description
            context: Additional context information

        Returns:
            Agent's response
        """
        self.status = AgentStatus.BUSY

        try:
            # Build prompt with role-specific instructions
            prompt = self._build_prompt(task, context)

            # Get response from underlying LLM
            response = self.mem_agent.chat(prompt)

            # Log interaction
            self.conversation_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "task": task,
                    "context": context,
                    "response": response,
                }
            )

            self.status = AgentStatus.IDLE
            return response

        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"Agent {self.name} error: {e}")
            raise

    def _build_prompt(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Build role-specific prompt.

        Args:
            task: Task description
            context: Additional context

        Returns:
            Formatted prompt
        """
        # Role-specific instructions
        role_instructions = {
            AgentRole.RESEARCHER: (
                "You are a research specialist. Focus on gathering accurate, "
                "comprehensive information. Cite sources when possible."
            ),
            AgentRole.ANALYST: (
                "You are a data analyst. Focus on analyzing information, "
                "finding patterns, and drawing insights."
            ),
            AgentRole.WRITER: (
                "You are a content writer. Focus on creating clear, engaging, "
                "well-structured content."
            ),
            AgentRole.VALIDATOR: (
                "You are a quality validator. Focus on checking accuracy, "
                "consistency, and completeness."
            ),
            AgentRole.COORDINATOR: (
                "You are a task coordinator. Focus on organizing work, "
                "delegating tasks, and ensuring completion."
            ),
            AgentRole.GENERAL: "You are a helpful assistant.",
        }

        instruction = role_instructions.get(self.role, role_instructions[AgentRole.GENERAL])

        prompt = f"{instruction}\n\nTask: {task}"

        if context:
            prompt += f"\n\nContext: {context}"

        return prompt

    def send_message(
        self, receiver_id: str, content: str, message_type: str = "chat"
    ) -> AgentMessage:
        """
        Send message to another agent.

        Args:
            receiver_id: Target agent ID
            content: Message content
            message_type: Type of message

        Returns:
            Created message
        """
        message = AgentMessage(
            sender_id=self.agent_id,
            receiver_id=receiver_id,
            content=content,
            message_type=message_type,
        )

        logger.debug(f"Agent {self.name} sending message to {receiver_id}")
        return message

    def receive_message(self, message: AgentMessage):
        """
        Receive message from another agent.

        Args:
            message: Incoming message
        """
        self.inbox.append(message)
        logger.debug(f"Agent {self.name} received message from {message.sender_id}")

    def get_messages(self, unread_only: bool = True) -> List[AgentMessage]:
        """
        Get messages from inbox.

        Args:
            unread_only: Return only unread messages

        Returns:
            List of messages
        """
        if unread_only:
            messages = self.inbox.copy()
            self.inbox.clear()  # Mark as read
            return messages
        return self.inbox.copy()

    def get_info(self) -> Dict[str, Any]:
        """
        Get agent information.

        Returns:
            Agent info dictionary
        """
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role.value,
            "status": self.status.value,
            "private_memory": self.private_memory,
            "inbox_count": len(self.inbox),
            "conversation_count": len(self.conversation_history),
        }

    def __repr__(self) -> str:
        return (
            f"BaseAgent(id={self.agent_id}, name={self.name}, "
            f"role={self.role.value}, status={self.status.value})"
        )
