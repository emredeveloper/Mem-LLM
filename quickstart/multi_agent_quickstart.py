"""
Multi-Agent Quickstart
=======================
Two AI agents working together: Researcher finds info, Writer creates summary.
"""

from mem_llm.multi_agent import AgentRole, BaseAgent, CommunicationHub

# Create two specialized agents
researcher = BaseAgent(
    name="Researcher", role=AgentRole.RESEARCHER, backend="ollama", model="granite4:3b"
)

writer = BaseAgent(name="Writer", role=AgentRole.WRITER, backend="ollama", model="granite4:3b")

# Set up communication
hub = CommunicationHub()
hub.register_agent(researcher.agent_id)
hub.register_agent(writer.agent_id)

print("🤖 Multi-Agent System Ready\n")

# Researcher does research
print("📚 Researcher: Gathering information...")
research = researcher.process("What are the key benefits of AI?")
print(f"   Found: {research[:120]}...\n")

# Researcher sends to Writer
print("📤 Researcher → Writer")
msg = researcher.send_message(writer.agent_id, f"Research findings: {research}")
hub.send_message(msg)

# Writer receives and creates summary
messages = hub.get_messages(writer.agent_id)
print(f"📥 Writer: Received {len(messages)} message\n")

print("✍️  Writer: Creating summary...")
summary = writer.process("Write a brief, clear summary about AI benefits")
print(f"   Summary: {summary[:150]}...\n")

print("✅ Done! Two agents collaborated successfully.")
