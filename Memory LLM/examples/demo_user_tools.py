"""
Kullanıcı Araçları Basit Demo
============================

Bu demo kullanıcı araçlarının nasıl çalıştığını gösterir.
Çok basit - sadece araçları test edin!
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mem_agent import MemAgent


def simple_demo():
    """Çok basit araç demo"""

    print("🤖 KULLANICI ARAÇLARI DEMOSU")
    print("=" * 50)
    print("Şimdi kullanıcı araçlarını test edeceğiz!\n")

    # Agent oluştur
    agent = MemAgent(model="granite4:tiny-h", use_sql=False)

    # Kullanıcı ayarla
    user_id = "test_user_123"
    agent.set_user(user_id, name="Test Kullanıcı")

    print("✅ Kullanıcı hazırlandı!\n")

    # Birkaç örnek konuşma ekle
    print("📝 Örnek konuşmalar ekleniyor...")
    agent.chat("Merhaba, benim adım Test Kullanıcı")
    agent.chat("Laptop almak istiyorum")
    agent.chat("Kargo ücretini öğrenmek istiyorum")
    print("✅ Konuşmalar eklendi!\n")

    # === ARAÇLARI KULLAN ===
    print("🛠️  ARAÇLARI KULLANALIM:")
    print("=" * 50)

    # 1. Geçmiş konuşmaları göster
    print("\n1️⃣  Geçmiş konuşmaları göster:")
    print("Kullanıcı: 'Geçmiş konuşmalarımı göster'")
    response = agent.chat("Geçmiş konuşmalarımı göster")
    print(f"Bot: {response}")

    # 2. Arama yap
    print("\n\n2️⃣  Laptop hakkında arama:")
    print("Kullanıcı: 'laptop kelimesi geçen konuşmalarımı ara'")
    response = agent.chat("laptop kelimesi geçen konuşmalarımı ara")
    print(f"Bot: {response}")

    # 3. Hakkımda bilgi
    print("\n\n3️⃣  Hakkımda bilgi:")
    print("Kullanıcı: 'Hakkımda ne biliyorsun?'")
    response = agent.chat("Hakkımda ne biliyorsun?")
    print(f"Bot: {response}")

    print("\n" + "=" * 50)
    print("✅ Demo tamamlandı!")
    print("=" * 50)


def main():
    """Ana fonksiyon"""
    try:
        simple_demo()
    except Exception as e:
        print(f"\n❌ Hata oluştu: {e}")


if __name__ == "__main__":
    main()

