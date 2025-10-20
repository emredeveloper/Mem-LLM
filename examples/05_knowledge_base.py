"""
Example 5: Knowledge Base
==========================
Shows how to add FAQ/support knowledge (requires SQL mode).
"""

from mem_llm import MemAgent

def main():
    print("=" * 60)
    print("📚 Knowledge Base Example")
    print("=" * 60)
    
    # Create agent with SQL mode (required for KB)
    agent = MemAgent(use_sql=True, memory_dir="kb_demo.db")
    
    # Check setup
    status = agent.check_setup()
    if status['status'] != 'ready':
        print("❌ Please start Ollama: ollama serve")
        return
    
    print("Adding knowledge base entries...\n")
    
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
        answer="You can return within 14 days. Product must be unused in original packaging. Call 1-800-RETURN for return code.",
        keywords=["return", "refund", "send back"],
        priority=10
    )
    
    # Add payment knowledge
    agent.add_knowledge(
        category="payment",
        question="Can I pay in installments?",
        answer="Yes! 3 installments over $100, 6 installments over $500, 9 installments over $1000.",
        keywords=["installment", "payment", "credit"],
        priority=10
    )
    
    print("✅ Knowledge base loaded!\n")
    
    # Test with customers
    agent.set_user("customer1")
    
    print("Customer 1: How much is shipping?")
    response = agent.chat("How much is shipping?")
    print(f"Bot: {response}\n")
    
    print("Customer 1: My order is $200")
    response = agent.chat("My order is $200")
    print(f"Bot: {response}\n")
    
    # Different customer
    agent.set_user("customer2")
    
    print("Customer 2: Can I return my purchase?")
    response = agent.chat("Can I return my purchase?")
    print(f"Bot: {response}\n")
    
    print("Customer 2: Can I pay monthly?")
    response = agent.chat("Can I pay monthly?")
    print(f"Bot: {response}\n")
    
    print("=" * 60)
    print("✅ Bot uses knowledge base for accurate answers!")
    print("=" * 60)

if __name__ == "__main__":
    main()
