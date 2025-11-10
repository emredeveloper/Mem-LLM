"""
Example 3: Multiple Users
==========================

Shows how different users have separate memories.

Quick Usage:
    agent.set_user("alice")
    agent.chat("I love cats")
    agent.set_user("bob")
    agent.chat("I love dogs")
    # Each user has separate memory!
"""

from mem_llm import MemAgent

print("=" * 60)
print("Multiple Users")
print("=" * 60)

agent = MemAgent()

# User 1: Alice
print("\n👤 USER 1: Alice")
agent.set_user("alice")
print("Alice: I love cats and reading books")
response = agent.chat("I love cats and reading books")
print(f"Bot: {response}\n")

# User 2: Bob
print("👤 USER 2: Bob")
agent.set_user("bob")
print("Bob: I'm a software engineer who enjoys hiking")
response = agent.chat("I'm a software engineer who enjoys hiking")
print(f"Bot: {response}\n")

# Back to Alice
print("👤 BACK TO USER 1: Alice")
agent.set_user("alice")
print("Alice: What do you know about me?")
response = agent.chat("What do you know about me?")
print(f"Bot: {response}\n")

# Back to Bob
print("👤 BACK TO USER 2: Bob")
agent.set_user("bob")
print("Bob: What's my job?")
response = agent.chat("What's my job?")
print(f"Bot: {response}\n")

print("=" * 60)
print("✅ Each user has completely separate memory!")
print("=" * 60)
