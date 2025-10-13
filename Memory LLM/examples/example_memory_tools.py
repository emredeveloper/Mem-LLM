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

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mem_agent import MemAgent


def demonstrate_memory_tools():
    """Bellek araçlarını gösterir"""

    print("🛠️  BELLEK ARAÇLARI DEMOSU")
    print("=" * 70)
    print("Bu demo kullanıcı araçlarının nasıl çalıştığını gösterir.\n")

    # Agent oluştur
    agent = MemAgent(model="granite4:tiny-h", use_sql=False)

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
    print("\n1️⃣  Geçmiş Konuşmaları Göster")
    print("-" * 40)
    print("Kullanıcı komutu: 'geçmiş konuşmalarımı göster'")
    response = agent.chat("geçmiş konuşmalarımı göster")
    print(f"\n📋 Sonuç:\n{response}\n")

    # 2. Arama yap
    print("\n2️⃣  Konuşmalarda Arama")
    print("-" * 40)
    print("Kullanıcı komutu: 'laptop kelimesi geçen konuşmalarımı ara'")
    response = agent.chat("laptop kelimesi geçen konuşmalarımı ara")
    print(f"\n🔍 Sonuç:\n{response}\n")

    # 3. Hakkımda ne biliyorsun
    print("\n3️⃣  Kullanıcı Bilgileri")
    print("-" * 40)
    print("Kullanıcı komutu: 'hakkımda ne biliyorsun'")
    response = agent.chat("hakkımda ne biliyorsun")
    print(f"\n👤 Sonuç:\n{response}\n")

    # 4. Kullanılabilir araçları listele
    print("\n4️⃣  Kullanılabilir Araçlar")
    print("-" * 40)
    tools_info = agent.list_available_tools()
    print(f"\n🛠️  Araçlar:\n{tools_info}\n")

    # === ÖZET ===
    print("=" * 70)
    print("📊 BELLEK ARAÇLARI ÖZETİ")
    print("=" * 70)
    print("✅ Kullanıcılar kendi verilerini yönetebilir")
    print("✅ Doğal dille komut verebilir")
    print("✅ Arama, görüntüleme, silme işlemleri yapabilir")
    print("✅ Gizlilik ve kontrol kullanıcıda")
    print("=" * 70)


def main():
    """Ana fonksiyon"""
    try:
        demonstrate_memory_tools()
    except Exception as e:
        print(f"\n❌ Hata oluştu: {e}")
        print("\n💡 Çözüm önerileri:")
        print("   1. Ollama servisinin çalıştığından emin olun")
        print("   2. Model yüklü olmalı: ollama pull granite4:tiny-h")


if __name__ == "__main__":
    main()

