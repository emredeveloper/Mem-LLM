"""
Örnek Kullanım: Müşteri Hizmetleri Botu
Senaryonuza uygun müşteri hizmetleri asistanı örneği
"""

from mem_agent import MemAgent  # Artık tek birleşik sistem!
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
    print(f"🤖 Bot: {response}")
    
    time.sleep(1)
    
    print("\n👤 Ahmet: Sipariş numaram #12345")
    response = agent.chat(
        message="Sipariş numaram #12345",
        metadata={
            "order_number": "#12345",
            "topic": "sipariş bilgisi"
        }
    )
    print(f"🤖 Bot: {response}")
    
    time.sleep(1)
    
    print("\n👤 Ahmet: Kargo çok geç kalıyor, ne zaman gelecek?")
    response = agent.chat(
        message="Kargo çok geç kalıyor, ne zaman gelecek?",
        metadata={
            "order_number": "#12345",
            "issue": "kargo gecikmesi"
        }
    )
    print(f"🤖 Bot: {response}")
    
    # Profil güncelleme
    agent.update_user_info({
        "name": "Ahmet",
        "summary": {
            "last_order": "#12345",
            "last_issue": "kargo gecikmesi",
            "issue_date": "2025-10-13"
        }
    })
    
    print("\n💾 Ahmet'in belleği kaydedildi.")
    
    # === GÜN 3: Ahmet Tekrar Geliyor ===
    print("\n" + "-" * 60)
    print("📅 GÜN 3 - Ahmet Tekrar Geliyor")
    print("-" * 60)
    
    time.sleep(2)
    
    print("\n👤 Ahmet: Merhaba yine ben")
    response = agent.chat(
        message="Merhaba yine ben"
    )
    print(f"🤖 Bot: {response}")
    
    time.sleep(1)
    
    print("\n👤 Ahmet: O kargo geldi mi?")
    response = agent.chat(
        message="O kargo geldi mi?",
        metadata={
            "order_number": "#12345",
            "topic": "kargo takip"
        }
    )
    print(f"🤖 Bot: {response}")
    
    # === 1 HAFTA SONRA: Yeni Sipariş ===
    print("\n" + "-" * 60)
    print("📅 1 HAFTA SONRA - Ahmet Yeni Sipariş Veriyor")
    print("-" * 60)
    
    time.sleep(2)
    
    print("\n👤 Ahmet: Yeni sipariş vermek istiyorum")
    response = agent.chat(
        message="Yeni sipariş vermek istiyorum"
    )
    print(f"🤖 Bot: {response}")
    
    # === YENİ MÜŞTERİ: Ayşe ===
    print("\n" + "-" * 60)
    print("📅 YENİ MÜŞTERİ: Ayşe")
    print("-" * 60)
    
    agent.set_user("ayse456")
    
    print("\n👤 Ayşe: Merhaba, ürün iade etmek istiyorum")
    response = agent.chat(
        message="Merhaba, ürün iade etmek istiyorum",
        metadata={
            "name": "Ayşe",
            "topic": "iade"
        }
    )
    print(f"🤖 Bot: {response}")
    
    # === BELLEK ANALİZİ ===
    print("\n" + "=" * 60)
    print("📊 BELLEK ANALİZİ")
    print("=" * 60)
    
    # Ahmet'in belleği
    print("\n👤 Ahmet'in Geçmişi:")
    print(agent.memory_manager.get_summary("ahmet123"))
    
    print("\n" + "-" * 60)
    
    # Ayşe'nin belleği
    print("\n👤 Ayşe'nin Geçmişi:")
    print(agent.memory_manager.get_summary("ayse456"))
    
    print("\n" + "-" * 60)
    
    # Genel istatistikler
    print("\n📈 Genel İstatistikler:")
    stats = agent.get_statistics()
    print(f"  Toplam Kullanıcı: {stats['total_users']}")
    print(f"  Toplam Etkileşim: {stats['total_interactions']}")
    print(f"  Kullanıcı Başına Ortalama: {stats['average_interactions_per_user']:.2f}")
    print(f"  Bellek Dizini: {stats['memory_directory']}")
    
    # Arama örneği
    print("\n🔍 'Kargo' kelimesini Ahmet'in geçmişinde ara:")
    results = agent.search_user_history("kargo", "ahmet123")
    print(f"  {len(results)} sonuç bulundu")
    
    print("\n" + "=" * 60)
    print("✅ Simülasyon tamamlandı!")
    print("=" * 60)


if __name__ == "__main__":
    simulate_customer_service()

