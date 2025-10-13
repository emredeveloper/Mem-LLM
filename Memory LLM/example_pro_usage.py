# BU DOSYA ARTIK KULLANILMIYOR - BİRLEŞİK SİSTEM KULLANIN
# Lütfen example_memory_tools.py veya diğer örnek dosyalarını kullanın


def example_1_basic_setup():
    """Örnek 1: Temel Kurulum ve Kullanım"""
    print("=" * 60)
    print("ÖRNEK 1: Temel Kurulum")
    print("=" * 60)
    
    # Agent oluştur (config.yaml'dan ayarları okur)
    with MemAgentPro() as agent:
        # Sistem kontrolü
        status = agent.check_setup()
        print(f"\n✅ Sistem Durumu:")
        print(f"   Ollama: {'✓' if status['ollama_running'] else '✗'}")
        print(f"   Model: {status['target_model']}")
        print(f"   Veritabanı: {'✓' if status['database_ready'] else '✗'}")
        print(f"   Toplam Kullanıcı: {status['total_users']}")
        print(f"   Bilgi Bankası: {status['kb_entries']} kayıt")
        
        if status['status'] != 'ready':
            print("\n❌ Sistem hazır değil! Ollama'yı başlatın.")
            return
        
        # Kullanıcı ayarla ve sohbet et
        agent.set_user("user001", name="Ali Yılmaz")
        
        response = agent.chat("Merhaba, siparişim nerede?")
        print(f"\n👤 Ali: Merhaba, siparişim nerede?")
        print(f"🤖 Bot: {response}")


def example_2_knowledge_base():
    """Örnek 2: Bilgi Bankası Kullanımı"""
    print("\n" + "=" * 60)
    print("ÖRNEK 2: Bilgi Bankası ile Çalışma")
    print("=" * 60)
    
    with MemAgentPro() as agent:
        # Bilgi bankasına yeni kayıt ekle
        print("\n📚 Bilgi bankasına kayıt ekleniyor...")
        
        agent.add_knowledge(
            category="promosyon",
            question="Şu an hangi kampanyalar var?",
            answer="Bu ay tüm ürünlerde %20 indirim kampanyamız var. Ayrıca 500 TL üzeri alışverişlerde 100 TL hediye çeki kazanıyorsunuz.",
            keywords=["kampanya", "indirim", "promosyon", "hediye"],
            priority=10
        )
        
        agent.set_user("user002", name="Ayşe Demir")
        
        # Bilgi bankasından cevap alacak
        response = agent.chat("Kampanya var mı?")
        print(f"\n👤 Ayşe: Kampanya var mı?")
        print(f"🤖 Bot: {response}")
        
        time.sleep(1)
        
        # Başka bir bilgi bankası sorusu
        response = agent.chat("Kargo ne zaman gelir?")
        print(f"\n👤 Ayşe: Kargo ne zaman gelir?")
        print(f"🤖 Bot: {response}")


def example_3_prompt_templates():
    """Örnek 3: Farklı Prompt Şablonları"""
    print("\n" + "=" * 60)
    print("ÖRNEK 3: Prompt Şablonları")
    print("=" * 60)
    
    with MemAgentPro() as agent:
        # Mevcut şablonları listele
        templates = agent.list_prompt_templates()
        print(f"\n📋 Mevcut Şablonlar:")
        for i, template in enumerate(templates, 1):
            print(f"   {i}. {template}")
        
        # Teknik destek modu
        print("\n\n--- Teknik Destek Modu ---")
        agent.change_prompt_template(
            "tech_support",
            product_name="Mem-Agent",
            user_level="ileri seviye"
        )
        
        agent.set_user("user003", name="Mehmet Kaya")
        response = agent.chat("Program açılmıyor, ne yapmalıyım?")
        print(f"\n👤 Mehmet: Program açılmıyor, ne yapmalıyım?")
        print(f"🤖 Bot: {response}")
        
        # Satış asistanı modu
        print("\n\n--- Satış Asistanı Modu ---")
        agent.change_prompt_template(
            "sales_assistant",
            store_name="TechStore",
            sales_approach="danışmanlık odaklı"
        )
        
        agent.set_user("user004", name="Zeynep Arslan")
        response = agent.chat("Yeni laptop almak istiyorum, öneri var mı?")
        print(f"\n👤 Zeynep: Yeni laptop almak istiyorum, öneri var mı?")
        print(f"🤖 Bot: {response}")


def example_4_memory_context():
    """Örnek 4: Bellek ve Bağlam Kullanımı"""
    print("\n" + "=" * 60)
    print("ÖRNEK 4: Bellek ve Bağlam")
    print("=" * 60)
    
    with MemAgentPro() as agent:
        agent.set_user("user005", name="Can Öztürk")
        
        # İlk etkileşim
        print("\n--- Etkileşim 1 ---")
        response = agent.chat(
            "Merhaba, dün #12345 numaralı sipariş verdim",
            metadata={"order_number": "#12345", "date": "2025-10-12"}
        )
        print(f"👤 Can: Merhaba, dün #12345 numaralı sipariş verdim")
        print(f"🤖 Bot: {response}")
        
        time.sleep(1)
        
        # İkinci etkileşim - Bağlam hatırlanır
        print("\n--- Etkileşim 2 ---")
        response = agent.chat("Bu sipariş ne zaman gelir?")
        print(f"👤 Can: Bu sipariş ne zaman gelir?")
        print(f"🤖 Bot: {response}")
        
        time.sleep(1)
        
        # Üçüncü etkileşim - Profil güncelleme
        print("\n--- Etkileşim 3 ---")
        agent.update_profile({
            "preferences": {"notification": "email"},
            "summary": {"favorite_category": "elektronik"}
        })
        
        response = agent.chat("Yeni ürünlerden haberdar olmak istiyorum")
        print(f"👤 Can: Yeni ürünlerden haberdar olmak istiyorum")
        print(f"🤖 Bot: {response}")
        
        # Geçmişte arama
        print("\n\n📝 Geçmiş Arama:")
        results = agent.search_history("sipariş", "user005")
        print(f"   'sipariş' kelimesi için {len(results)} sonuç bulundu")


def example_5_statistics():
    """Örnek 5: İstatistikler ve Raporlama"""
    print("\n" + "=" * 60)
    print("ÖRNEK 5: İstatistikler")
    print("=" * 60)
    
    with MemAgentPro() as agent:
        stats = agent.get_statistics()
        
        print(f"\n📊 Sistem İstatistikleri:")
        print(f"   Toplam Kullanıcı: {stats['total_users']}")
        print(f"   Toplam Etkileşim: {stats['total_interactions']}")
        print(f"   Çözülmemiş Sorunlar: {stats['unresolved_issues']}")
        print(f"   Bilgi Bankası Kayıtları: {stats['knowledge_base_entries']}")
        print(f"   Kullanıcı Başına Ortalama: {stats['avg_interactions_per_user']:.2f}")


def main():
    """Tüm örnekleri çalıştır"""
    print("\n" + "🚀" * 30)
    print("MEM-AGENT PRO - Gelişmiş Kullanım Örnekleri")
    print("🚀" * 30)
    
    try:
        example_1_basic_setup()
        time.sleep(2)
        
        example_2_knowledge_base()
        time.sleep(2)
        
        example_3_prompt_templates()
        time.sleep(2)
        
        example_4_memory_context()
        time.sleep(2)
        
        example_5_statistics()
        
        print("\n\n" + "✅" * 30)
        print("Tüm örnekler başarıyla tamamlandı!")
        print("✅" * 30)
        
    except Exception as e:
        print(f"\n❌ Hata oluştu: {e}")
        print("\n💡 Çözüm:")
        print("   1. Ollama servisinin çalıştığından emin olun: ollama serve")
        print("   2. Model yüklü olmalı: ollama pull granite4:tiny-h")
        print("   3. config.yaml dosyasını kontrol edin")


if __name__ == "__main__":
    main()

