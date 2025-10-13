"""
Business Mode Example
MemAgent demo for corporate use
"""

from memory_llm import MemAgent


def business_mode_demo():
    """Corporate usage mode demo"""

    print("🏢 CORPORATE USAGE MODE DEMO")
    print("=" * 60)
    print("This example demonstrates its use as corporate customer service.\n")

    # Create agent in Business mode
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

    # Set corporate user
    user_id = "business_user"
    agent.set_user(user_id, name="Corporate Customer")

    print("👤 Corporate customer calling support line...\n")

    # Corporate questions
    conversations = [
        "Merhaba, şirketimiz için teknik destek istiyorum. SLA süreniz nedir?",
        "Şirketimiz 500+ çalışanlı büyük bir kuruluş. Kurumsal fiyatlandırma hakkında bilgi alabilir miyim?",
        "Acil bir sistem arızası yaşıyoruz. Kritik öncelik seviyesiyle destek alabilir miyiz?",
        "Şirketimiz ISO 27001 sertifikalı. Güvenlik standartlarınız neler?",
        "Çoklu kanal entegrasyonunuz var mı? Slack ve Teams ile bağlantı kurabilir miyiz?"
    ]

    for i, message in enumerate(conversations, 1):
        print(f"{i}. 👤 Müşteri: {message}")
        response = agent.chat(message)
        print(f"   🤖 Destek: {response[:100]}...")
        print()

    # Kurumsal araçları göster
    print("🛠️  KURUMSAL ARAÇLAR:")
    print("-" * 40)
    tools_info = agent.list_available_tools()
    print(tools_info)

    print("\n" + "=" * 60)
    print("🎯 KURUMSAL MOD ÖZETİ:")
    print("=" * 60)
    print("• Kurumsal müşteri hizmetleri")
    print("• SLA tabanlı destek")
    print("• Çoklu kanal entegrasyonu")
    print("• Güvenlik ve uyumluluk")
    print("• Raporlama ve analitik")
    print("• 7/24 kesintisiz destek")


def main():
    """Ana demo fonksiyonu"""
    try:
        business_mode_demo()
    except Exception as e:
        print(f"❌ Demo hatası: {e}")
        print("\n💡 Çözüm önerileri:")
        print("• config.yaml dosyasının doğru ayarlandığından emin olun")
        print("• usage_mode: business olarak ayarlayın")
        print("• business bölümünde şirket bilgilerini doldurun")


if __name__ == "__main__":
    main()

