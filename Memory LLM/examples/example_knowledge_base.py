"""
KNOWLEDGE BASE EXAMPLE
======================
Demonstrates how to use knowledge base for FAQ/support systems
"""

from mem_llm import MemAgent


def main():
    print("=" * 70)
    print("🤖 KNOWLEDGE BASE EXAMPLE - Customer Support Bot")
    print("=" * 70)
    print()
    
    # Create agent with SQL memory (required for KB)
    print("1️⃣ Creating agent with knowledge base...")
    agent = MemAgent(
        model="granite4:tiny-h",
        use_sql=True,
        memory_dir="kb_example.db"
    )
    
    # Check setup
    status = agent.check_setup()
    if status['status'] != 'ready':
        print("❌ Ollama not running or model not available!")
        print("   Run: ollama serve")
        return
    
    print("✅ Agent ready!\n")
    
    # Add knowledge base entries
    print("2️⃣ Adding knowledge base entries...")
    
    # Shipping knowledge
    agent.add_knowledge(
        category="shipping",
        question="What is the shipping cost?",
        answer="Shipping is free for orders over $150. Below that: $19.90 for orders $50-150, $29.90 for orders under $50.",
        keywords=["shipping", "cost", "delivery", "fee"],
        priority=10
    )
    
    agent.add_knowledge(
        category="shipping",
        question="How long does delivery take?",
        answer="Istanbul: 1-2 business days, Turkey-wide: 2-5 business days, Remote areas: 3-7 business days.",
        keywords=["delivery", "time", "when", "arrive"],
        priority=10
    )
    
    # Return knowledge
    agent.add_knowledge(
        category="returns",
        question="How can I return a product?",
        answer="You can return within 14 days of delivery. The product must be in its original packaging. Call 0850 123 4567 for a return code.",
        keywords=["return", "refund", "send back"],
        priority=10
    )
    
    agent.add_knowledge(
        category="returns",
        question="What is the return phone number?",
        answer="For returns, call 0850 123 4567 (Mon-Fri, 9am-6pm).",
        keywords=["return", "phone", "contact", "number"],
        priority=10
    )
    
    # Payment knowledge
    agent.add_knowledge(
        category="payment",
        question="Can I pay in installments?",
        answer="Yes! 3 installments for orders over $100, 6 installments over $500, 9 installments over $1000.",
        keywords=["installment", "payment", "credit card"],
        priority=10
    )
    
    print("✅ 5 knowledge entries added!\n")
    
    # Test conversations
    print("3️⃣ Testing customer support conversations...\n")
    
    # Customer 1: Shipping question
    print("-" * 60)
    print("📞 Customer 1: Ahmed (Shipping cost)")
    print("-" * 60)
    agent.set_user("ahmed123", name="Ahmed")
    
    print("\n👤 Ahmed: Hello, how much is shipping?")
    response = agent.chat("Hello, how much is shipping?")
    print(f"🤖 Bot: {response}\n")
    
    print("👤 Ahmed: My order is $200.")
    response = agent.chat("My order is $200.")
    print(f"🤖 Bot: {response}\n")
    
    # Customer 2: Return question
    print("-" * 60)
    print("📞 Customer 2: Sarah (Return)")
    print("-" * 60)
    agent.set_user("sarah456", name="Sarah")
    
    print("\n👤 Sarah: Can I return the product I bought?")
    response = agent.chat("Can I return the product I bought?")
    print(f"🤖 Bot: {response}\n")
    
    print("👤 Sarah: What's the return phone number?")
    response = agent.chat("What's the return phone number?")
    print(f"🤖 Bot: {response}\n")
    
    # Customer 3: Installment question
    print("-" * 60)
    print("📞 Customer 3: Michael (Installments)")
    print("-" * 60)
    agent.set_user("michael789", name="Michael")
    
    print("\n👤 Michael: Can I pay in installments for a $600 product?")
    response = agent.chat("Can I pay in installments for a $600 product?")
    print(f"🤖 Bot: {response}\n")
    
    # Show statistics
    print("=" * 70)
    print("📊 STATISTICS")
    print("=" * 70)
    
    stats = agent.get_statistics()
    print(f"\n👥 Total users: {stats.get('total_users', 0)}")
    print(f"💬 Total conversations: {stats.get('total_interactions', 0)}")
    print(f"📚 Knowledge base entries: {stats.get('kb_entries', 0)}")
    
    # Show user profiles
    print("\n👤 Customer Profiles:")
    for user_id in ["ahmed123", "sarah456", "michael789"]:
        profile = agent.get_user_profile(user_id)
        print(f"  - {profile.get('name', user_id)}: {profile}")
    
    print("\n" + "=" * 70)
    print("✅ EXAMPLE COMPLETED!")
    print("=" * 70)
    print("\n💡 Key Takeaways:")
    print("  1. Knowledge base provides accurate answers from your database")
    print("  2. Bot uses KB info instead of making up answers")
    print("  3. Each customer conversation is saved separately")
    print("  4. User profiles are automatically created and updated")
    print("  5. Statistics help track usage")
    print("=" * 70)


if __name__ == "__main__":
    main()

