"""
Example 11: LM Studio Backend
==============================
Simple example using LM Studio local server.
"""

from mem_llm import MemAgent

print("\n" + "="*50)
print("LM STUDIO EXAMPLE")
print("="*50 + "\n")

# Create agent with LM Studio
agent = MemAgent(
    backend='lmstudio',
    model='local-model',
    base_url='http://localhost:1234',
    use_sql=False
)

agent.set_user("alice")

# Chat
conversations = [
    "Hello! My name is Alice and I'm a Python developer.",
    "I'm interested in machine learning.",
    "Do you remember my name and interests?"
]

for msg in conversations:
    print(f"User: {msg}")
    response = agent.chat(msg)
    print(f"AI: {response}\n")

print("="*50 + "\n")
