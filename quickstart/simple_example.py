"""
Simple Multi-Agent Example
===========================

The simplest possible example - 2 agents talking to each other.
"""

from mem_llm.multi_agent import AgentRole, BaseAgent, CommunicationHub

# Create 2 agents
agent1 = BaseAgent(role=AgentRole.RESEARCHER, backend="ollama", model="granite4:3b")
agent2 = BaseAgent(role=AgentRole.ANALYST, backend="ollama", model="granite4:3b")

# Set up communication
hub = CommunicationHub()
hub.register_agent(agent1.agent_id)
hub.register_agent(agent2.agent_id)

# Agent 1 sends message to Agent 2
message = agent1.send_message(agent2.agent_id, "Hello! Can you help me?")
hub.send_message(message)

# Agent 2 receives message
messages = hub.get_messages(agent2.agent_id)
print(f"Agent 2 received: '{messages[0].content}'")

# Agent 2 responds
response = agent2.process("How can I help you with your research?")
print(f"Agent 2 responds: {response[:100]}...")
