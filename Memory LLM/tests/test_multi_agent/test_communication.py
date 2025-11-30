"""
Unit tests for Communication Protocol
======================================

Tests MessageQueue and CommunicationHub functionality.
"""

import pytest

from mem_llm.multi_agent import AgentMessage, CommunicationHub, MessageQueue


class TestMessageQueue:
    """Test MessageQueue functionality"""

    def test_queue_creation(self):
        """Test queue initialization"""
        queue = MessageQueue(max_size=10)
        assert queue.size() == 0
        assert queue.is_empty() is True

    def test_enqueue_dequeue(self):
        """Test basic enqueue/dequeue"""
        queue = MessageQueue()
        message = AgentMessage(sender_id="agent-1", receiver_id="agent-2", content="Test")

        # Enqueue
        success = queue.enqueue(message)
        assert success is True
        assert queue.size() == 1

        # Dequeue
        retrieved = queue.dequeue()
        assert retrieved is not None
        assert retrieved.content == "Test"
        assert queue.size() == 0

    def test_fifo_order(self):
        """Test FIFO ordering"""
        queue = MessageQueue()

        # Add multiple messages
        for i in range(5):
            msg = AgentMessage(sender_id="sender", receiver_id="receiver", content=f"Message {i}")
            queue.enqueue(msg)

        # Verify FIFO
        for i in range(5):
            msg = queue.dequeue()
            assert msg.content == f"Message {i}"

    def test_max_size(self):
        """Test queue size limit"""
        queue = MessageQueue(max_size=3)

        # Fill queue
        for i in range(3):
            msg = AgentMessage(sender_id="s", receiver_id="r", content=f"Msg {i}")
            assert queue.enqueue(msg) is True

        # Try to exceed limit
        msg = AgentMessage(sender_id="s", receiver_id="r", content="Overflow")
        # With deque maxlen, it will succeed but drop oldest
        queue.enqueue(msg)
        assert queue.size() == 3

    def test_peek(self):
        """Test peek without removing"""
        queue = MessageQueue()
        msg = AgentMessage(sender_id="s", receiver_id="r", content="Peek test")

        queue.enqueue(msg)

        # Peek should not remove
        peeked = queue.peek()
        assert peeked.content == "Peek test"
        assert queue.size() == 1

        # Dequeue should still work
        dequeued = queue.dequeue()
        assert dequeued.content == "Peek test"
        assert queue.size() == 0

    def test_clear(self):
        """Test clearing queue"""
        queue = MessageQueue()

        # Add messages
        for i in range(5):
            msg = AgentMessage(sender_id="s", receiver_id="r", content=f"Msg {i}")
            queue.enqueue(msg)

        assert queue.size() == 5

        # Clear
        queue.clear()
        assert queue.size() == 0
        assert queue.is_empty() is True

    def test_get_all(self):
        """Test getting all messages without removing"""
        queue = MessageQueue()

        # Add messages
        for i in range(3):
            msg = AgentMessage(sender_id="s", receiver_id="r", content=f"Msg {i}")
            queue.enqueue(msg)

        # Get all
        all_msgs = queue.get_all()
        assert len(all_msgs) == 3
        assert queue.size() == 3  # Should not remove


class TestCommunicationHub:
    """Test CommunicationHub functionality"""

    def test_hub_creation(self):
        """Test hub initialization"""
        hub = CommunicationHub()
        stats = hub.get_stats()
        assert stats["registered_agents"] == 0

    def test_agent_registration(self):
        """Test agent registration"""
        hub = CommunicationHub()

        hub.register_agent("agent-1")
        hub.register_agent("agent-2")

        stats = hub.get_stats()
        assert stats["registered_agents"] == 2

    def test_agent_unregistration(self):
        """Test agent unregistration"""
        hub = CommunicationHub()

        hub.register_agent("agent-1")
        assert hub.get_stats()["registered_agents"] == 1

        hub.unregister_agent("agent-1")
        assert hub.get_stats()["registered_agents"] == 0

    def test_direct_messaging(self):
        """Test direct agent-to-agent messaging"""
        hub = CommunicationHub()

        # Register agents
        hub.register_agent("agent-1")
        hub.register_agent("agent-2")

        # Send message
        message = AgentMessage(sender_id="agent-1", receiver_id="agent-2", content="Hello Agent 2")
        success = hub.send_message(message)
        assert success is True

        # Retrieve message
        messages = hub.get_messages("agent-2")
        assert len(messages) == 1
        assert messages[0].content == "Hello Agent 2"

    def test_broadcast(self):
        """Test broadcast messaging"""
        hub = CommunicationHub()

        # Register agents
        for i in range(1, 4):
            hub.register_agent(f"agent-{i}")

        # Subscribe to channel
        hub.subscribe("agent-1", "news")
        hub.subscribe("agent-2", "news")
        hub.subscribe("agent-3", "news")

        # Broadcast
        delivered = hub.broadcast("agent-1", "Important news!", channel="news")
        assert delivered == 2  # agent-1 doesn't receive own broadcast

        # Check messages
        agent2_msgs = hub.get_messages("agent-2")
        agent3_msgs = hub.get_messages("agent-3")

        assert len(agent2_msgs) == 1
        assert len(agent3_msgs) == 1
        assert agent2_msgs[0].content == "Important news!"

    def test_subscribe_unsubscribe(self):
        """Test channel subscription"""
        hub = CommunicationHub()

        hub.register_agent("agent-1")
        hub.register_agent("agent-2")

        # Subscribe
        hub.subscribe("agent-1", "updates")
        hub.subscribe("agent-2", "updates")

        stats = hub.get_stats()
        assert stats["subscribers_per_channel"]["updates"] == 2

        # Unsubscribe
        hub.unsubscribe("agent-1", "updates")
        stats = hub.get_stats()
        assert stats["subscribers_per_channel"]["updates"] == 1

    def test_multiple_channels(self):
        """Test multiple broadcast channels"""
        hub = CommunicationHub()

        # Register agents
        hub.register_agent("agent-1")
        hub.register_agent("agent-2")
        hub.register_agent("agent-3")

        # Different subscriptions
        hub.subscribe("agent-1", "tech")
        hub.subscribe("agent-2", "tech")
        hub.subscribe("agent-2", "news")
        hub.subscribe("agent-3", "news")

        # Broadcast to tech
        hub.broadcast("agent-1", "Tech update", channel="tech")

        # Only agent-2 should receive (agent-1 is sender)
        assert len(hub.get_messages("agent-2")) == 1
        assert len(hub.get_messages("agent-3")) == 0

    def test_get_stats(self):
        """Test statistics retrieval"""
        hub = CommunicationHub()

        # Setup
        hub.register_agent("agent-1")
        hub.register_agent("agent-2")
        hub.subscribe("agent-1", "channel-1")

        # Send message
        msg = AgentMessage(sender_id="agent-1", receiver_id="agent-2", content="Test")
        hub.send_message(msg)

        stats = hub.get_stats()

        assert stats["registered_agents"] == 2
        assert stats["total_queued_messages"] == 1
        assert "agent-2" in stats["queue_sizes"]
        assert stats["queue_sizes"]["agent-2"] == 1

    def test_clear_all(self):
        """Test clearing all queues"""
        hub = CommunicationHub()

        # Setup with messages
        hub.register_agent("agent-1")
        hub.register_agent("agent-2")

        msg1 = AgentMessage(sender_id="agent-1", receiver_id="agent-2", content="Msg1")
        msg2 = AgentMessage(sender_id="agent-2", receiver_id="agent-1", content="Msg2")

        hub.send_message(msg1)
        hub.send_message(msg2)

        assert hub.get_stats()["total_queued_messages"] == 2

        # Clear all
        hub.clear_all()
        assert hub.get_stats()["total_queued_messages"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
