"""
Example 4: Customer Service Bot
================================

Demonstrates how memory helps in customer service scenarios.

Quick Usage:
    agent.set_user("customer_alice")
    agent.chat("Where is my order #12345?")
    # Next day, bot remembers the conversation!
"""

from mem_llm import MemAgent

print("=" * 60)
print("Customer Service Bot")
print("=" * 60)

# Create agent
agent = MemAgent(use_sql=False)

print("\n📅 DAY 1 - Customer: Alice")
agent.set_user("customer_alice")

print("Alice: Hi, where is my order #12345?")
response = agent.chat("Hi, where is my order #12345?")
print(f"Bot: {response}\n")

print("Alice: What's the shipping cost?")
response = agent.chat("What's the shipping cost?")
print(f"Bot: {response}\n")

print("📅 DAY 2 - Alice calls again")
agent.set_user("customer_alice")

print("Alice: Hi, I called yesterday about my order...")
response = agent.chat("Hi, I called yesterday about my order")
print(f"Bot: {response}")
print("🧠 Bot remembers yesterday's conversation!\n")

print("📅 DAY 3 - New Customer: Bob")
agent.set_user("customer_bob")

print("Bob: Can I return a product?")
response = agent.chat("Can I return a product?")
print(f"Bot: {response}\n")

print("=" * 60)
print("📊 Benefits:")
print("  ✅ Remembers each customer's history")
print("  ✅ No need to repeat information")
print("  ✅ Better customer experience")
print("  ✅ Separate memory per customer")
print("=" * 60)
