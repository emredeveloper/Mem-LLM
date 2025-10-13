"""
User Tools Simple Demo
=====================

This demo shows how user tools work.
Very simple - just test the tools!
"""

from memory_llm import MemAgent


def simple_demo():
    """Very simple tool demo"""

    print("🤖 USER TOOLS DEMO")
    print("=" * 50)
    print("Now we will test the user tools!\n")

    # Create agent
    agent = MemAgent(model="granite4:tiny-h", use_sql=False)

    # Set user
    user_id = "test_user_123"
    agent.set_user(user_id, name="Test User")

    print("✅ User prepared!\n")

    # Add a few sample conversations
    print("📝 Adding sample conversations...")
    agent.chat("Hello, my name is Test User")
    agent.chat("I want to buy a laptop")
    agent.chat("I want to learn about shipping costs")
    print("✅ Conversations added!\n")

    # === USE TOOLS ===
    print("🛠️  LET'S USE TOOLS:")
    print("=" * 50)

    # 1. Show past conversations
    print("\n1️⃣  Show past conversations:")
    print("User: 'Show my past conversations'")
    response = agent.chat("Show my past conversations")
    print(f"Bot: {response}")

    # 2. Search
    print("\n\n2️⃣  Search about laptop:")
    print("User: 'Search my conversations containing the word laptop'")
    response = agent.chat("Search my conversations containing the word laptop")
    print(f"Bot: {response}")

    # 3. Information about me
    print("\n\n3️⃣  Information about me:")
    print("User: 'What do you know about me?'")
    response = agent.chat("What do you know about me?")
    print(f"Bot: {response}")

    print("\n" + "=" * 50)
    print("✅ Demo completed!")
    print("=" * 50)


def main():
    """Main function"""
    try:
        simple_demo()
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")


if __name__ == "__main__":
    main()

