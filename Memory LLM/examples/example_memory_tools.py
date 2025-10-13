"""
MEMORY TOOLS EXAMPLE
===================

This example shows how users can manage their own memory data.
Users can now:
- View their conversation history
- Search through conversations
- Verilerini silebilir
- Hakkında ne bilindiğini öğrenebilir
"""

from memory_llm import MemAgent


def demonstrate_memory_tools():
    """Shows memory tools"""

    print("🛠️  MEMORY TOOLS DEMO")
    print("=" * 70)
    print("This demo shows how user tools work.\n")

    # Create agent
    agent = MemAgent(model="granite4:tiny-h", use_sql=False)

    # Set user
    user_id = "ahmet_demo"
    agent.set_user(user_id)

    print("✅ Demo user prepared!\n")

    # === ADD SAMPLE CONVERSATIONS ===
    print("📝 Adding sample conversations...")

    conversations = [
        "Merhaba, benim adım Ahmet Yılmaz",
        "Dün bir laptop siparişi verdim, durumu nedir?",
        "Kargo ne zaman gelecek?",
        "İade politikası nedir?",
        "Başka bir ürün daha almak istiyorum"
    ]

    for i, msg in enumerate(conversations, 1):
        print(f"   {i}. '{msg[:30]}...'")
        response = agent.chat(msg, metadata={"demo": True})

    print("✅ Sample conversations added!\n")

    # === USE TOOLS ===
    print("🎯 NOW WE WILL USE THE TOOLS:")
    print("=" * 70)

    # 1. List past conversations
    print("\n1️⃣  Show Past Conversations")
    print("-" * 40)
    print("User command: 'show my past conversations'")
    response = agent.chat("show my past conversations")
    print(f"\n📋 Result:\n{response}\n")

    # 2. Search
    print("\n2️⃣  Search in Conversations")
    print("-" * 40)
    print("User command: 'search my conversations containing the word laptop'")
    response = agent.chat("search my conversations containing the word laptop")
    print(f"\n🔍 Result:\n{response}\n")

    # 3. What do you know about me
    print("\n3️⃣  User Information")
    print("-" * 40)
    print("User command: 'what do you know about me'")
    response = agent.chat("what do you know about me")
    print(f"\n👤 Result:\n{response}\n")

    # 4. List available tools
    print("\n4️⃣  Available Tools")
    print("-" * 40)
    tools_info = agent.list_available_tools()
    print(f"\n🛠️  Tools:\n{tools_info}\n")

    # === SUMMARY ===
    print("=" * 70)
    print("📊 MEMORY TOOLS SUMMARY")
    print("=" * 70)
    print("✅ Users can manage their own data")
    print("✅ Can give commands in natural language")
    print("✅ Can perform search, display, deletion operations")
    print("✅ Privacy and control with user")
    print("=" * 70)


def main():
    """Main function"""
    try:
        demonstrate_memory_tools()
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("\n💡 Solution suggestions:")
        print("   1. Make sure Ollama service is running")
        print("   2. Model must be loaded: ollama pull granite4:tiny-h")


if __name__ == "__main__":
    main()

