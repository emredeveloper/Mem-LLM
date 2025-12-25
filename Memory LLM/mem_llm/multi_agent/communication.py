"""
Communication Protocol for Multi-Agent System
==============================================

Handles message passing, queuing, and broadcasting between agents.

Author: Cihat Emre Karataş
Version: 2.2.0
"""

import logging
import threading
from collections import defaultdict, deque
from typing import Callable, Dict, List, Optional

from .base_agent import AgentMessage

logger = logging.getLogger(__name__)


class MessageQueue:
    """
    Thread-safe message queue for agent communication.

    Features:
    - FIFO message delivery
    - Thread-safe operations
    - Message filtering
    - Queue statistics
    """

    def __init__(self, max_size: int = 1000):
        """
        Initialize message queue.

        Args:
            max_size: Maximum queue size (0 = unlimited)
        """
        self.max_size = max_size
        self._queue: deque = deque(maxlen=max_size if max_size > 0 else None)
        self._lock = threading.Lock()
        logger.info(f"📬 Message Queue initialized (max_size={max_size})")

    def enqueue(self, message: AgentMessage) -> bool:
        """
        Add message to queue.

        Args:
            message: Message to enqueue

        Returns:
            True if successful, False if queue is full
        """
        with self._lock:
            if self.max_size > 0 and len(self._queue) >= self.max_size:
                logger.warning(f"Queue full, dropping message {message.message_id}")
                return False

            self._queue.append(message)
            logger.debug(f"Enqueued message {message.message_id}")
            return True

    def dequeue(self) -> Optional[AgentMessage]:
        """
        Remove and return oldest message.

        Returns:
            Message or None if queue is empty
        """
        with self._lock:
            if not self._queue:
                return None

            message = self._queue.popleft()
            logger.debug(f"Dequeued message {message.message_id}")
            return message

    def peek(self) -> Optional[AgentMessage]:
        """
        View oldest message without removing.

        Returns:
            Message or None if queue is empty
        """
        with self._lock:
            return self._queue[0] if self._queue else None

    def size(self) -> int:
        """Get current queue size."""
        with self._lock:
            return len(self._queue)

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        with self._lock:
            return len(self._queue) == 0

    def clear(self):
        """Clear all messages from queue."""
        with self._lock:
            self._queue.clear()
            logger.info("Queue cleared")

    def get_all(self) -> List[AgentMessage]:
        """
        Get all messages without removing.

        Returns:
            List of all messages
        """
        with self._lock:
            return list(self._queue)


class CommunicationHub:
    """
    Central hub for agent-to-agent communication.

    Features:
    - Direct messaging (agent-to-agent)
    - Broadcast messaging (one-to-many)
    - Message routing
    - Subscription system
    """

    def __init__(self):
        """Initialize communication hub."""
        # Agent-specific message queues
        self._agent_queues: Dict[str, MessageQueue] = {}

        # Broadcast subscribers
        self._subscribers: Dict[str, List[str]] = defaultdict(list)

        # Message handlers (callbacks)
        self._handlers: Dict[str, Callable] = {}

        # Lock for thread safety
        self._lock = threading.Lock()

        logger.info("📡 Communication Hub initialized")

    def register_agent(self, agent_id: str, queue_size: int = 100):
        """
        Register an agent for communication.

        Args:
            agent_id: Agent ID
            queue_size: Size of agent's message queue
        """
        with self._lock:
            if agent_id not in self._agent_queues:
                self._agent_queues[agent_id] = MessageQueue(max_size=queue_size)
                logger.info(f"✅ Registered agent {agent_id} for communication")

    def unregister_agent(self, agent_id: str):
        """
        Unregister an agent.

        Args:
            agent_id: Agent ID
        """
        with self._lock:
            if agent_id in self._agent_queues:
                del self._agent_queues[agent_id]
                logger.info(f"❌ Unregistered agent {agent_id}")

    def send_message(self, message: AgentMessage) -> bool:
        """
        Send message to specific agent.

        Args:
            message: Message to send

        Returns:
            True if delivered, False otherwise
        """
        receiver_id = message.receiver_id

        with self._lock:
            if receiver_id not in self._agent_queues:
                logger.warning(f"Receiver {receiver_id} not registered")
                return False

            success = self._agent_queues[receiver_id].enqueue(message)

            if success:
                logger.debug(f"Message {message.message_id}: {message.sender_id} → {receiver_id}")
            return success

    def broadcast(self, sender_id: str, content: str, channel: str = "default") -> int:
        """
        Broadcast message to all subscribers of a channel.

        Args:
            sender_id: Sender agent ID
            content: Message content
            channel: Broadcast channel

        Returns:
            Number of agents that received the message
        """
        # Get subscribers first (while holding lock)
        with self._lock:
            subscribers = self._subscribers.get(channel, []).copy()

        # Send messages (without holding lock to avoid deadlock)
        delivered = 0
        for receiver_id in subscribers:
            if receiver_id == sender_id:
                continue  # Don't send to self

            message = AgentMessage(
                sender_id=sender_id,
                receiver_id=receiver_id,
                content=content,
                message_type="broadcast",
                metadata={"channel": channel},
            )

            if self.send_message(message):
                delivered += 1

        logger.info(f"📢 Broadcast on '{channel}': {delivered} agents reached")
        return delivered

    def subscribe(self, agent_id: str, channel: str = "default"):
        """
        Subscribe agent to broadcast channel.

        Args:
            agent_id: Agent ID
            channel: Channel name
        """
        with self._lock:
            if agent_id not in self._subscribers[channel]:
                self._subscribers[channel].append(agent_id)
                logger.info(f"🔔 Agent {agent_id} subscribed to '{channel}'")

    def unsubscribe(self, agent_id: str, channel: str = "default"):
        """
        Unsubscribe agent from channel.

        Args:
            agent_id: Agent ID
            channel: Channel name
        """
        with self._lock:
            if agent_id in self._subscribers[channel]:
                self._subscribers[channel].remove(agent_id)
                logger.info(f"🔕 Agent {agent_id} unsubscribed from '{channel}'")

    def get_messages(self, agent_id: str, count: int = -1) -> List[AgentMessage]:
        """
        Get messages for an agent.

        Args:
            agent_id: Agent ID
            count: Number of messages to retrieve (-1 = all)

        Returns:
            List of messages
        """
        with self._lock:
            if agent_id not in self._agent_queues:
                return []

            queue = self._agent_queues[agent_id]
            messages = []

            if count == -1:
                # Get all messages
                while not queue.is_empty():
                    msg = queue.dequeue()
                    if msg:
                        messages.append(msg)
            else:
                # Get specific count
                for _ in range(count):
                    msg = queue.dequeue()
                    if msg:
                        messages.append(msg)
                    else:
                        break

            return messages

    def get_stats(self) -> Dict:
        """
        Get communication statistics.

        Returns:
            Statistics dictionary
        """
        with self._lock:
            stats = {
                "registered_agents": len(self._agent_queues),
                "total_queued_messages": sum(q.size() for q in self._agent_queues.values()),
                "channels": len(self._subscribers),
                "queue_sizes": {
                    agent_id: queue.size() for agent_id, queue in self._agent_queues.items()
                },
                "subscribers_per_channel": {
                    channel: len(subs) for channel, subs in self._subscribers.items()
                },
            }
            return stats

    def clear_all(self):
        """Clear all message queues."""
        with self._lock:
            for queue in self._agent_queues.values():
                queue.clear()
            logger.info("All message queues cleared")
