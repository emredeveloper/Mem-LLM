"""
Agent Registry - Manages all agents in the system
==================================================

Provides centralized agent management, lookup, and health monitoring.

Author: Cihat Emre Karataş
Version: 2.2.0
"""

import logging
from typing import Dict, List, Optional

from .base_agent import AgentRole, AgentStatus, BaseAgent

logger = logging.getLogger(__name__)


class AgentRegistry:
    """
    Central registry for managing agents.

    Features:
    - Agent registration/deregistration
    - Agent lookup by ID or role
    - Status tracking
    - Health monitoring
    """

    def __init__(self):
        """Initialize registry."""
        self._agents: Dict[str, BaseAgent] = {}
        logger.info("📋 Agent Registry initialized")

    def register(self, agent: BaseAgent) -> bool:
        """
        Register an agent.

        Args:
            agent: Agent to register

        Returns:
            True if successful, False if ID already exists
        """
        if agent.agent_id in self._agents:
            logger.warning(f"Agent {agent.agent_id} already registered")
            return False

        self._agents[agent.agent_id] = agent
        logger.info(f"✅ Registered agent: {agent.name} ({agent.agent_id})")
        return True

    def deregister(self, agent_id: str) -> bool:
        """
        Deregister an agent.

        Args:
            agent_id: Agent ID to remove

        Returns:
            True if successful, False if not found
        """
        if agent_id not in self._agents:
            logger.warning(f"Agent {agent_id} not found")
            return False

        agent = self._agents.pop(agent_id)
        logger.info(f"❌ Deregistered agent: {agent.name} ({agent_id})")
        return True

    def get(self, agent_id: str) -> Optional[BaseAgent]:
        """
        Get agent by ID.

        Args:
            agent_id: Agent ID

        Returns:
            Agent instance or None
        """
        return self._agents.get(agent_id)

    def get_by_role(self, role: AgentRole) -> List[BaseAgent]:
        """
        Get all agents with specific role.

        Args:
            role: Agent role

        Returns:
            List of agents with that role
        """
        return [agent for agent in self._agents.values() if agent.role == role]

    def get_by_status(self, status: AgentStatus) -> List[BaseAgent]:
        """
        Get all agents with specific status.

        Args:
            status: Agent status

        Returns:
            List of agents with that status
        """
        return [agent for agent in self._agents.values() if agent.status == status]

    def get_all(self) -> List[BaseAgent]:
        """
        Get all registered agents.

        Returns:
            List of all agents
        """
        return list(self._agents.values())

    def count(self) -> int:
        """
        Get total number of registered agents.

        Returns:
            Agent count
        """
        return len(self._agents)

    def get_stats(self) -> Dict[str, any]:
        """
        Get registry statistics.

        Returns:
            Statistics dictionary
        """
        stats = {
            "total_agents": len(self._agents),
            "by_role": {},
            "by_status": {},
        }

        # Count by role
        for role in AgentRole:
            count = len(self.get_by_role(role))
            if count > 0:
                stats["by_role"][role.value] = count

        # Count by status
        for status in AgentStatus:
            count = len(self.get_by_status(status))
            if count > 0:
                stats["by_status"][status.value] = count

        return stats

    def health_check(self) -> Dict[str, any]:
        """
        Perform health check on all agents.

        Returns:
            Health status dictionary
        """
        healthy = []
        unhealthy = []

        for agent in self._agents.values():
            if agent.status == AgentStatus.ERROR or agent.status == AgentStatus.OFFLINE:
                unhealthy.append(
                    {
                        "agent_id": agent.agent_id,
                        "name": agent.name,
                        "status": agent.status.value,
                    }
                )
            else:
                healthy.append(agent.agent_id)

        return {
            "healthy_count": len(healthy),
            "unhealthy_count": len(unhealthy),
            "healthy_agents": healthy,
            "unhealthy_agents": unhealthy,
        }

    def __repr__(self) -> str:
        return f"AgentRegistry(agents={len(self._agents)})"
