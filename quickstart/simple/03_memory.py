"""
Simple Example 3: Memory
=========================
Multi-user memory - Separate conversations
"""

from mem_llm import MemAgent

agent = MemAgent(
    backend='ollama',
    model='llama3.2:3b',
    use_sql=False  # JSON memory (simple)
    # use_sql=True  # SQLite memory (advanced)
)

# User 1
agent.set_user("alice")
print("👤 Alice:")
print(agent.chat("Hello, my name is Alice and I'm a software engineer"))
print()

# User 2
agent.set_user("bob")
print("👤 Bob:")
print(agent.chat("Hi, I'm Bob and I'm a doctor"))
print()

# Back to Alice - remembers her info
agent.set_user("alice")
print("👤 Alice (again):")
print(agent.chat("What's my profession?"))
print()

# Clear memory (if needed)
# agent.clear_memory("alice")
