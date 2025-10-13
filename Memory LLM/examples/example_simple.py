"""
MEM-AGENT SIMPLE EXAMPLE
========================

This example shows how a memory-enabled chatbot works.
We will have 3 very simple conversations and test the bot's memory.
"""

from memory_llm import MemAgent


def main():
    print("🤖 MEMORY-ENABLED CHATBOT EXAMPLE")
    print("=" * 60)
    print("This example step by step tests the bot's memory.\n")

    # 1. Create bot
    print("1️⃣ Creating bot...")
    agent = MemAgent(model="granite4:tiny-h", use_sql=False)

    # Sistem kontrolü
    status = agent.check_setup()
    if status['status'] != 'ready':
        print("❌ ERROR: Ollama is not running or model is not loaded!")
        print("   Solution: Run 'ollama serve' command")
        return

    print("✅ Bot ready!\n")

    # 2. Set user
    user_id = "ahmet123"
    agent.set_user(user_id)

    # 3. FIRST CONVERSATION - Introduction
    print("2️⃣ FIRST CONVERSATION - Introduction")
    print("-" * 40)
    print("👤 Ahmet: Merhaba, benim adım Ahmet")
    response = agent.chat("Merhaba, benim adım Ahmet")
    print(f"🤖 Bot:  {response}\n")

    # 4. SECOND CONVERSATION - Memory recall
    print("3️⃣ SECOND CONVERSATION - Memory")
    print("-" * 40)
    print("👤 Ahmet: Dün sana pizza sipariş etmiştim")
    response = agent.chat("Dün sana pizza sipariş etmiştim")
    print(f"🤖 Bot:  {response}\n")

    # 5. ÜÇÜNCÜ KONUŞMA - Bellek testi
    print("4️⃣ ÜÇÜNCÜ KONUŞMA - Bellek Testi")
    print("-" * 40)
    print("👤 Ahmet: Adımı hatırlıyor musun?")
    response = agent.chat("Adımı hatırlıyor musun?")
    print(f"🤖 Bot:  {response}\n")

    # 6. BELLEK ÖZETİ
    print("5️⃣ BELLEK ÖZETİ")
    print("-" * 40)
    if hasattr(agent.memory, 'get_summary'):
        summary = agent.memory.get_summary(user_id)
        print(summary)

    print("\n" + "=" * 60)
    print("🎯 RESULT: Bot remembers Ahmet's name!")
    print("📚 All conversations saved.")
    print("🔄 Will use this information in future conversations.")
    print("=" * 60)


if __name__ == "__main__":
    main()

