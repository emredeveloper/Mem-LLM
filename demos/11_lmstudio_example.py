"""
Example 11: LM Studio Backend
=============================

Use LM Studio local server as backend.

Quick Usage:
    agent = MemAgent(
        backend='lmstudio',
        model='local-model',
        base_url='http://localhost:1234'
    )
"""

from mem_llm import MemAgent

print("=" * 60)
print("LM Studio Backend")
print("=" * 60)

# Create agent with LM Studio
agent = MemAgent(
    backend='lmstudio',
    model='local-model',
    base_url='http://localhost:1234',
    use_sql=False,
    check_connection=False
)

agent.set_user("alice")

# Chat
print("\n💬 Conversation:")
messages = [
    "Hello! My name is Alice and I'm a Python developer.",
    "I'm interested in machine learning.",
    "Do you remember my name and interests?"
]

for msg in messages:
    print(f"\nUser: {msg}")
    response = agent.chat(msg)
    print(f"AI: {response}")

print("\n" + "=" * 60)
