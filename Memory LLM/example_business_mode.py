"""
Business Mod Örneği
Kurumsal kullanım için MemAgent demo
"""

from mem_agent import MemAgent


def business_mode_demo():
    """Kurumsal kullanım modu demo"""

    print("🏢 KURUMSAL KULLANIM MODU DEMO")
    print("=" * 60)
    print("Bu örnek kurumsal müşteri hizmetleri olarak kullanımını gösterir.\n")

    # Business modda agent oluştur
    agent = MemAgent(
        config_file="config.yaml",  # business mod ayarları ile
        use_sql=True,
        load_knowledge_base=True
    )

    print(f"✅ Kullanım modu: {agent.usage_mode}")
    print(f"✅ Sistem promptu: {agent.current_system_prompt[:50]}...")
    print()

    # Kurumsal kullanıcı ayarla
    user_id = "business_user"
    agent.set_user(user_id, name="Şirket Müşterisi")

    print("👤 Kurumsal müşteri destek hattını arıyor...\n")

    # Kurumsal sorular
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
