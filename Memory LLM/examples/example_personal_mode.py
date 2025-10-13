"""
Personal Mode Example
MemAgent demo for personal use
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mem_agent import MemAgent


def personal_mode_demo():
    """Personal usage mode demo"""

    print("🏠 PERSONAL USAGE MODE DEMO")
    print("=" * 60)
    print("This example demonstrates its use as a personal assistant.\n")

    # Create agent in Personal mode
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")
    agent = MemAgent(
        config_file=config_path,
        use_sql=True,
        load_knowledge_base=True
    )

    print(f"✅ Usage mode: {agent.usage_mode}")
    if agent.current_system_prompt:
        print(f"✅ System prompt: {agent.current_system_prompt[:50]}...")
    print()

    # Set user
    user_id = "personal_user"
    agent.set_user(user_id, name="Ahmet Yılmaz")

    print("👤 Ahmet Yılmaz is using personal assistant...\n")

    # Personal questions
    conversations = [
        "Merhaba! Ben Ahmet Yılmaz. Bugünkü hava durumu nasıl?",
        "Yarın için bir hatırlatma ayarla: Saat 15:00'de dişçi randevusu",
        "Bu hafta ne öğrenmek istersin? Python programlama hakkında bir kurs önerir misin?",
        "Finansal durumum hakkında ne biliyorsun?",
        "Hakkımda ne biliyorsun?"
    ]

    for i, message in enumerate(conversations, 1):
        print(f"{i}. 👤 Ahmet: {message}")
        response = agent.chat(message)
        print(f"   🤖 Bot: {response[:100]}...")
        print()

    # Kişisel araçları göster
    print("🛠️  KİŞİSEL ARAÇLAR:")
    print("-" * 40)
    tools_info = agent.list_available_tools()
    print(tools_info)

    print("\n" + "=" * 60)
    print("🎯 KİŞİSEL MOD ÖZETİ:")
    print("=" * 60)
    print("• Kişiselleştirilmiş günlük asistan")
    print("• Öğrenme ve gelişim takibi")
    print("• Finansal danışmanlık")
    print("• Sağlık ve wellness hatırlatmaları")
    print("• Özel notlar ve anılar")


def main():
    """Ana demo fonksiyonu"""
    try:
        personal_mode_demo()
    except Exception as e:
        print(f"❌ Demo hatası: {e}")
        print("\n💡 Çözüm önerileri:")
        print("• config.yaml dosyasının doğru ayarlandığından emin olun")
        print("• usage_mode: personal olarak ayarlayın")


if __name__ == "__main__":
    main()

