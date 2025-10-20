"""
Example 4: Customer Service Bot
================================
Demonstrates how memory helps in customer service scenarios.
"""

from mem_llm import MemAgent
import time

def main():
    print("=" * 60)
    print("🤖 Customer Service Bot with Memory")
    print("=" * 60)
    
    # Create agent
    agent = MemAgent(use_sql=False)
    
    # Check setup
    status = agent.check_setup()
    if status['status'] != 'ready':
        print("❌ Please start Ollama: ollama serve")
        return
    
    print("✅ Bot ready!\n")
    
    # === Day 1: Customer Alice ===
    print("📅 DAY 1 - Customer: Alice")
    print("-" * 60)
    
    agent.set_user("customer_alice")
    
    print("Alice: Hi, where is my order #12345?")
    response = agent.chat("Hi, where is my order #12345?")
    print(f"Bot: {response}\n")
    
    time.sleep(0.5)
    
    print("Alice: What's the shipping cost?")
    response = agent.chat("What's the shipping cost?")
    print(f"Bot: {response}\n")
    
    # === Day 2: Alice Returns ===
    print("📅 DAY 2 - Alice calls again")
    print("-" * 60)
    
    agent.set_user("customer_alice")
    
    print("Alice: Hi, I called yesterday about my order...")
    response = agent.chat("Hi, I called yesterday about my order")
    print(f"Bot: {response}")
    print("🧠 Bot remembers yesterday's conversation!\n")
    
    # === Day 3: New Customer Bob ===
    print("📅 DAY 3 - New Customer: Bob")
    print("-" * 60)
    
    agent.set_user("customer_bob")
    
    print("Bob: Can I return a product?")
    response = agent.chat("Can I return a product?")
    print(f"Bot: {response}\n")
    
    # === Summary ===
    print("=" * 60)
    print("📊 Benefits:")
    print("   ✅ Remembers each customer's history")
    print("   ✅ No need to repeat information")
    print("   ✅ Better customer experience")
    print("   ✅ Separate memory per customer")
    print("=" * 60)

if __name__ == "__main__":
    main()
