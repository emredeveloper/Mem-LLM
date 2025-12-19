"""
Unit tests for BaseAgent and AgentRegistry
===========================================

Tests the core multi-agent functionality.
"""

import pytest

from mem_llm.multi_agent import AgentRegistry, AgentRole, AgentStatus, BaseAgent


class TestBaseAgent:
    """Test BaseAgent functionality"""

    def test_agent_creation(self):
        """Test basic agent creation"""
        agent = BaseAgent(name="Test Agent", role=AgentRole.RESEARCHER, model="rnj-1:latest")

        assert agent.name == "Test Agent"
        assert agent.role == AgentRole.RESEARCHER
        assert agent.status == AgentStatus.IDLE
        assert agent.agent_id is not None

    def test_agent_with_custom_id(self):
        """Test agent with custom ID"""
        agent = BaseAgent(agent_id="custom-123", name="Custom Agent")

        assert agent.agent_id == "custom-123"

    def test_agent_process(self):
        """Test agent task processing"""
        agent = BaseAgent(role=AgentRole.GENERAL, model="rnj-1:latest")

        # Simple task
        response = agent.process("Say hello")

        assert response is not None
        assert isinstance(response, str)
        assert len(agent.conversation_history) == 1

    def test_agent_messaging(self):
        """Test agent-to-agent messaging"""
        agent1 = BaseAgent(agent_id="agent-1", name="Agent 1")
        agent2 = BaseAgent(agent_id="agent-2", name="Agent 2")

        # Send message
        message = agent1.send_message("agent-2", "Hello Agent 2!")

        assert message.sender_id == "agent-1"
        assert message.receiver_id == "agent-2"
        assert message.content == "Hello Agent 2!"

        # Receive message
        agent2.receive_message(message)
        assert len(agent2.inbox) == 1

        # Get messages
        messages = agent2.get_messages()
        assert len(messages) == 1
        assert messages[0].content == "Hello Agent 2!"

    def test_agent_info(self):
        """Test agent info retrieval"""
        agent = BaseAgent(name="Info Agent", role=AgentRole.ANALYST)

        info = agent.get_info()

        assert info["name"] == "Info Agent"
        assert info["role"] == "analyst"
        assert info["status"] == "idle"
        assert "agent_id" in info


class TestAgentRegistry:
    """Test AgentRegistry functionality"""

    def test_registry_creation(self):
        """Test registry initialization"""
        registry = AgentRegistry()
        assert registry.count() == 0

    def test_agent_registration(self):
        """Test agent registration"""
        registry = AgentRegistry()
        agent = BaseAgent(name="Test Agent")

        # Register
        success = registry.register(agent)
        assert success is True
        assert registry.count() == 1

        # Try duplicate registration
        success = registry.register(agent)
        assert success is False
        assert registry.count() == 1

    def test_agent_deregistration(self):
        """Test agent deregistration"""
        registry = AgentRegistry()
        agent = BaseAgent(agent_id="test-123")

        registry.register(agent)
        assert registry.count() == 1

        # Deregister
        success = registry.deregister("test-123")
        assert success is True
        assert registry.count() == 0

        # Try deregistering non-existent agent
        success = registry.deregister("non-existent")
        assert success is False

    def test_agent_lookup(self):
        """Test agent lookup by ID"""
        registry = AgentRegistry()
        agent = BaseAgent(agent_id="lookup-test", name="Lookup Agent")

        registry.register(agent)

        # Get by ID
        found = registry.get("lookup-test")
        assert found is not None
        assert found.name == "Lookup Agent"

        # Get non-existent
        not_found = registry.get("non-existent")
        assert not_found is None

    def test_get_by_role(self):
        """Test getting agents by role"""
        registry = AgentRegistry()

        # Create agents with different roles
        agent1 = BaseAgent(name="Researcher 1", role=AgentRole.RESEARCHER)
        agent2 = BaseAgent(name="Researcher 2", role=AgentRole.RESEARCHER)
        agent3 = BaseAgent(name="Analyst", role=AgentRole.ANALYST)

        registry.register(agent1)
        registry.register(agent2)
        registry.register(agent3)

        # Get researchers
        researchers = registry.get_by_role(AgentRole.RESEARCHER)
        assert len(researchers) == 2

        # Get analysts
        analysts = registry.get_by_role(AgentRole.ANALYST)
        assert len(analysts) == 1

    def test_get_by_status(self):
        """Test getting agents by status"""
        registry = AgentRegistry()

        agent1 = BaseAgent(name="Agent 1")
        agent2 = BaseAgent(name="Agent 2")

        agent1.status = AgentStatus.IDLE
        agent2.status = AgentStatus.BUSY

        registry.register(agent1)
        registry.register(agent2)

        # Get idle agents
        idle = registry.get_by_status(AgentStatus.IDLE)
        assert len(idle) == 1

        # Get busy agents
        busy = registry.get_by_status(AgentStatus.BUSY)
        assert len(busy) == 1

    def test_registry_stats(self):
        """Test registry statistics"""
        registry = AgentRegistry()

        # Create diverse agents
        registry.register(BaseAgent(role=AgentRole.RESEARCHER))
        registry.register(BaseAgent(role=AgentRole.RESEARCHER))
        registry.register(BaseAgent(role=AgentRole.ANALYST))

        stats = registry.get_stats()

        assert stats["total_agents"] == 3
        assert stats["by_role"]["researcher"] == 2
        assert stats["by_role"]["analyst"] == 1

    def test_health_check(self):
        """Test health monitoring"""
        registry = AgentRegistry()

        agent1 = BaseAgent(name="Healthy")
        agent2 = BaseAgent(name="Unhealthy")

        agent1.status = AgentStatus.IDLE
        agent2.status = AgentStatus.ERROR

        registry.register(agent1)
        registry.register(agent2)

        health = registry.health_check()

        assert health["healthy_count"] == 1
        assert health["unhealthy_count"] == 1
        assert len(health["unhealthy_agents"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
