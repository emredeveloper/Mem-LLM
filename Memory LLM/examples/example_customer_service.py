"""
Örnek Kullanım: Müşteri Hizmetleri Botu
Senaryonuza uygun müşteri hizmetleri asistanı örneği
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mem_agent import MemAgent
import time


def simulate_customer_service():
    """Müşteri hizmetleri senaryosunu simüle eder"""

    print("=" * 70)
    print("🤖 BELLEKLİ MÜŞTERİ HİZMETLERİ BOTU")
    print("=" * 70)
    print("Bu örnek gerçek bir müşteri hizmetleri konuşmasını simüle eder.")
    print("Bot müşterinin geçmişini hatırlar ve kişiselleştirilmiş cevap verir.\n")

    # Agent'ı başlat
    print("🔄 Bot başlatılıyor...")
    agent = MemAgent(
        model="granite4:tiny-h",
        use_sql=False,
        memory_dir="customer_memories"
    )

    # Kurulum kontrolü
    print("🔍 Sistem kontrolü...")
    status = agent.check_setup()

    if status['status'] != 'ready':
        print("❌ HATA: Ollama çalışmıyor!")
        print("   Çözüm: 'ollama serve' komutunu çalıştırın")
        return

    print("✅ Sistem hazır!\n")
    
    # === GÜN 1: İlk Müşteri - Ahmet ===
    print("-" * 60)
    print("📅 GÜN 1 - İlk Müşteri: Ahmet")
    print("-" * 60)
    
    agent.set_user("ahmet123")
    
    print("\n👤 Ahmet: Merhaba, siparişim nerede?")
    response = agent.chat(
        message="Merhaba, siparişim nerede?",
        metadata={
            "name": "Ahmet",
            "topic": "sipariş sorgusu"
        }
    )
    print(f"🤖 Bot: {response}\n")
    
    time.sleep(1)
    
    print("👤 Ahmet: Kargo ücreti ne kadar?")
    response = agent.chat("Kargo ücreti ne kadar?")
    print(f"🤖 Bot: {response}\n")
    
    # === GÜN 2: Aynı Müşteri Geri Dönüyor ===
    print("-" * 60)
    print("📅 GÜN 2 - Ahmet tekrar arıyor")
    print("-" * 60)
    
    agent.set_user("ahmet123")  # Aynı kullanıcı
    
    print("\n👤 Ahmet: Merhabalar, dün size sormuştum...")
    response = agent.chat("Merhabalar, dün size sormuştum...")
    print(f"🤖 Bot: {response}")
    print("   (🧠 Bot geçmiş konuşmayı hatırlıyor!)\n")
    
    # === GÜN 3: Yeni Müşteri - Ayşe ===
    print("-" * 60)
    print("📅 GÜN 3 - Yeni Müşteri: Ayşe")
    print("-" * 60)
    
    agent.set_user("ayse456")
    
    print("\n👤 Ayşe: Ürün iade edebilir miyim?")
    response = agent.chat(
        message="Ürün iade edebilir miyim?",
        metadata={
            "name": "Ayşe",
            "topic": "iade talebi"
        }
    )
    print(f"🤖 Bot: {response}\n")
    
    # === SONUÇ ===
    print("=" * 70)
    print("📊 ÖZET VE İSTATİSTİKLER")
    print("=" * 70)
    
    # İstatistikleri göster
    stats = agent.get_statistics()
    print(f"Toplam kullanıcı: {stats.get('total_users', 'N/A')}")
    print(f"Toplam etkileşim: {stats.get('total_interactions', 'N/A')}")
    
    print("\n🎯 DEMO SONUÇLARI:")
    print("✅ Müşteriler farklı günlerde geri döndüğünde geçmişlerini hatırlıyor")
    print("✅ Her müşterinin ayrı belleği var")
    print("✅ Metadata ile ek bilgi kaydediliyor")
    print("✅ Gerçek müşteri hizmetleri için kullanıma hazır!")
    print("=" * 70)


def main():
    """Ana fonksiyon"""
    try:
        simulate_customer_service()
    except Exception as e:
        print(f"\n❌ Hata oluştu: {e}")
        print("\n💡 Çözüm önerileri:")
        print("   1. Ollama servisinin çalıştığından emin olun: ollama serve")
        print("   2. Model yüklü olmalı: ollama pull granite4:tiny-h")


if __name__ == "__main__":
    main()

