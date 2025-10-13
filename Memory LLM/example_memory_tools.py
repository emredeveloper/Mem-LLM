"""
BELLEK ARAÇLARI ÖRNEĞİ
======================

Bu örnek, kullanıcıların kendi bellek verilerini nasıl yönetebileceğini gösterir.
Kullanıcılar artık:
- Geçmiş konuşmalarını görebilir
- Konuşmalarda arama yapabilir
- Verilerini silebilir
- Hakkında ne bilindiğini öğrenebilir
"""

from mem_agent import MemAgent


def demonstrate_memory_tools():
    """Bellek araçlarını gösterir"""

    print("🛠️  BELLEK ARAÇLARI DEMOSU")
    print("=" * 70)
    print("Bu demo kullanıcı araçlarının nasıl çalıştığını gösterir.\n")

    # Agent oluştur
    agent = MemAgent(model="granite4:tiny-h")

    # Kullanıcı belirle
    user_id = "ahmet_demo"
    agent.set_user(user_id)

    print("✅ Demo kullanıcısı hazırlandı!\n")

    # === ÖRNEK KONUŞMALAR EKLE ===
    print("📝 Örnek konuşmalar ekleniyor...")

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

    print("✅ Örnek konuşmalar eklendi!\n")

    # === ARAÇLARI KULLAN ===
    print("🎯 ŞİMDİ ARAÇLARI KULLANACAĞIZ:")
    print("=" * 70)

    # 1. Geçmiş konuşmaları listele
    print("\n1️⃣  GEÇMİŞ KONUŞMALARI LİSTELE")
    print("-" * 50)
    print("👤 Kullanıcı: 'Geçmiş konuşmalarımı göster'")
    response = agent.chat("Geçmiş konuşmalarımı göster")
    print(f"🤖 Bot: {response[:200]}...")

    # 2. Arama yap
    print("\n\n2️⃣  KONUŞMALARDA ARAMA")
    print("-" * 50)
    print("👤 Kullanıcı: 'laptop kelimesi geçen konuşmalarımı ara'")
    response = agent.chat("laptop kelimesi geçen konuşmalarımı ara")
    print(f"🤖 Bot: {response[:200]}...")

    # 3. Kullanıcı bilgilerini göster
    print("\n\n3️⃣  KULLANICI BİLGİLERİ")
    print("-" * 50)
    print("👤 Kullanıcı: 'Hakkımda ne biliyorsun?'")
    response = agent.chat("Hakkımda ne biliyorsun?")
    print(f"🤖 Bot: {response}")

    # 4. Verileri dışa aktar
    print("\n\n4️⃣  VERİLERİ DIŞA AKTAR")
    print("-" * 50)
    print("👤 Kullanıcı: 'Verilerimi dışa aktar'")
    response = agent.chat("Verilerimi dışa aktar")
    print(f"🤖 Bot: {response[:300]}...")

    # 5. Tüm verileri silme (demo - gerçekte onay gerektirir)
    print("\n\n5️⃣  VERİLERİ SİLME (SİMÜLASYON)")
    print("-" * 50)
    print("👤 Kullanıcı: 'Tüm verilerimi sil'")
    response = agent.chat("Tüm verilerimi sil")
    print(f"🤖 Bot: {response}")

    print("\n" + "=" * 70)
    print("🎉 ARAÇLAR BAŞARIYLA ÇALIŞTI!")
    print("=" * 70)
    print("Kullanıcılar artık kendi verilerini yönetebiliyor!")

    # Araç listesini göster
    print("\n📋 Kullanılabilir Tüm Araçlar:")
    print("-" * 40)
    tools = [
        "list_memories - Geçmiş konuşmaları listele",
        "search_memories - Konuşmalarda ara",
        "show_user_info - Kullanıcı bilgilerini göster",
        "export_memories - Verileri dışa aktar",
        "clear_all_memories - Tüm verileri sil",
        "delete_memory - Belirli konuşmayı sil"
    ]

    for tool in tools:
        print(f"• {tool}")


def interactive_demo():
    """Etkileşimli demo"""
    print("\n🕹️  ETKİLEŞİMLİ DEMO")
    print("=" * 50)
    print("Şimdi siz de araçları deneyebilirsiniz!")
    print("(Çıkmak için 'çıkış' yazın)\n")

    agent = MemAgent(model="granite4:tiny-h")
    agent.set_user("interactive_user")

    while True:
        try:
            message = input("👤 Siz: ").strip()

            if message.lower() in ['çıkış', 'exit', 'quit']:
                print("👋 Görüşürüz!")
                break

            if not message:
                continue

            print("🤖 Bot:", end=" ")
            response = agent.chat(message)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n👋 Demo sonlandırıldı!")
            break
        except Exception as e:
            print(f"❌ Hata: {e}")


def main():
    """Ana demo fonksiyonu"""
    print("🚀 BELLEK ARAÇLARI ÖRNEĞİ")
    print("=" * 70)

    try:
        # Otomatik demo
        demonstrate_memory_tools()

        print("\n" + "=" * 70)

        # Kullanıcıya etkileşimli demo seçeneği sor
        choice = input("Etkileşimli demo yapmak ister misiniz? (e/h): ").lower().strip()

        if choice in ['e', 'evet', 'yes', 'y']:
            interactive_demo()
        else:
            print("Demo tamamlandı! 🎉")

    except Exception as e:
        print(f"❌ Demo hatası: {e}")
        print("\n💡 Çözüm önerileri:")
        print("• Ollama servisinin çalıştığından emin olun")
        print("• Modelin yüklü olduğunu kontrol edin")
        print("• Python ortamının doğru olduğunu kontrol edin")


if __name__ == "__main__":
    main()
