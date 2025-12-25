"""
Example 2: Basic Memory
========================

Shows how the agent remembers information across conversations.

Quick Usage:
    agent.set_user("john")
    agent.chat("My name is John and I love pizza")
    agent.chat("What's my name?")  # Remembers!
"""

from mem_llm import MemAgent

print("=" * 60)
print("Basic Memory")
print("=" * 60)

# Create agent
agent = MemAgent(model="granite4:3b", use_sql=False)
agent.set_user("john")

print("\n💬 Conversation 1: Share Information")
response = agent.chat("My name is John and I love pizza")
print(f"Bot: {response}\n")

print("💬 Conversation 2: Test Memory")
response = agent.chat("What's my name?")
print(f"Bot: {response}\n")

print("💬 Conversation 3: Test Memory Again")
response = agent.chat("What food do I like?")
print(f"Bot: {response}\n")

# Show saved profile
profile = agent.get_user_profile()
print("📋 Saved Profile:")
print(f"  Name: {profile.get('name', 'N/A')}")
print(f"  Favorite Food: {profile.get('favorite_food', 'N/A')}")

print("\n" + "=" * 60)
