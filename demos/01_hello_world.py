"""
Example 1: Hello World
======================

The simplest possible example - just a few lines!

Quick Usage:
    agent = MemAgent()
    agent.set_user("alice")
    response = agent.chat("Hello! My name is Alice")
"""

from mem_llm import MemAgent

print("=" * 60)
print("Hello World")
print("=" * 60)

# Create agent
agent = MemAgent()

# Set user
agent.set_user("alice")

# Chat!
print("\n💬 Conversation:")
response = agent.chat("Hello! My name is Alice")
print(f"Bot: {response}")

# Test memory
print()
response = agent.chat("What's my name?")
print(f"Bot: {response}  # Should remember: 'Your name is Alice'")

print("\n" + "=" * 60)
