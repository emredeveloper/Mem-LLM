"""
Personal Mod Örneği
Kişisel kullanım için MemAgent demo
"""

from mem_agent import MemAgent


def personal_mode_demo():
    """Kişisel kullanım modu demo"""

    print("🏠 KİŞİSEL KULLANIM MODU DEMO")
    print("=" * 60)
    print("Bu örnek kişisel asistan olarak kullanımını gösterir.\n")

    # Personal modda agent oluştur
    agent = MemAgent(
        config_file="config.yaml",  # personal mod ayarları ile
        use_sql=True,
        load_knowledge_base=True
    )

    print(f"✅ Kullanım modu: {agent.usage_mode}")
    print(f"✅ Sistem promptu: {agent.current_system_prompt[:50]}...")
    print()

    # Kullanıcı ayarla
    user_id = "personal_user"
    agent.set_user(user_id, name="Ahmet Yılmaz")

    print("👤 Ahmet Yılmaz kişisel asistanı kullanıyor...\n")

    # Kişisel sorular
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
