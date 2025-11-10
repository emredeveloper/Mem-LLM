"""
Example 5: Knowledge Base
=========================

Shows how to add FAQ/support knowledge (requires SQL mode).

Quick Usage:
    agent = MemAgent(use_sql=True)
    agent.add_knowledge(
        category="shipping",
        question="What is the shipping cost?",
        answer="Free shipping for orders over $150.",
        keywords=["shipping", "cost"]
    )
    agent.chat("How much is shipping?")  # Uses KB!
"""

from mem_llm import MemAgent

print("=" * 60)
print("Knowledge Base")
print("=" * 60)

# Create agent with SQL mode (required for KB)
agent = MemAgent(use_sql=True, memory_dir="kb_demo.db")

print("\n📚 Adding knowledge base entries...")

# Add shipping knowledge
agent.add_knowledge(
    category="shipping",
    question="What is the shipping cost?",
    answer="Free shipping for orders over $150. Orders $50-150: $19.90. Under $50: $29.90.",
    keywords=["shipping", "cost", "delivery", "free"],
    priority=10
)

# Add return knowledge
agent.add_knowledge(
    category="returns",
    question="How can I return a product?",
    answer="You can return within 14 days. Product must be unused in original packaging.",
    keywords=["return", "refund", "send back"],
    priority=10
)

# Add payment knowledge
agent.add_knowledge(
    category="payment",
    question="Can I pay in installments?",
    answer="Yes! 3 installments over $100, 6 installments over $500.",
    keywords=["installment", "payment", "credit"],
    priority=10
)

print("✅ Knowledge base loaded!\n")

# Test with customers
agent.set_user("customer1")

print("💬 Customer 1:")
print("  Q: How much is shipping?")
response = agent.chat("How much is shipping?")
print(f"  A: {response}\n")

print("  Q: My order is $200")
response = agent.chat("My order is $200")
print(f"  A: {response}\n")

# Different customer
agent.set_user("customer2")

print("💬 Customer 2:")
print("  Q: Can I return my purchase?")
response = agent.chat("Can I return my purchase?")
print(f"  A: {response}\n")

print("  Q: Can I pay monthly?")
response = agent.chat("Can I pay monthly?")
print(f"  A: {response}\n")

print("=" * 60)
print("✅ Bot uses knowledge base for accurate answers!")
print("=" * 60)
