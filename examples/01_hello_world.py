"""
Example 1: Hello World
======================
The simplest possible example - just 5 lines of code!
"""

from mem_llm import MemAgent

# Create agent
agent = MemAgent()

# Set user
agent.set_user("alice")

# Chat!
response = agent.chat("Hello! My name is Alice")
print(response)

# Test memory
response = agent.chat("What's my name?")
print(response)  # Should remember: "Your name is Alice"
