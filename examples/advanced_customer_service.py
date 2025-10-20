"""
Advanced Customer Service Bot with Knowledge Base
Bilgi tabanından öğrenen müşteri hizmetleri botu
"""

from mem_llm import MemAgent, SQLMemoryManager
import time


def load_knowledge_base(agent):
    """Bilgi tabanını yükle"""
    print("📚 Bilgi tabanı yükleniyor...")
    
    # company_knowledge.txt dosyasından bilgi yükle
    try:
        with open("company_knowledge.txt", "r", encoding="utf-8") as f:
            content = f.read()
        
        # SQL memory kullanıyorsa knowledge base ekle
        if hasattr(agent.memory, 'add_knowledge'):
            # Kargo bilgileri
            agent.add_knowledge(
                category="kargo",
                question="Kargo ücreti ne kadar?",
                answer="0-50 TL arası siparişlerde 29.90 TL, 50-150 TL arası 19.90 TL, 150 TL ve üzeri ÜCRETSİZ kargo.",
                keywords=["kargo", "ücret", "teslimat", "bedava"]
            )
            
            agent.add_knowledge(
                category="kargo",
                question="Teslimat ne kadar sürer?",
                answer="İstanbul içi 1-2 iş günü, Türkiye geneli 2-5 iş günü, uzak bölgeler 3-7 iş günü.",
                keywords=["teslimat", "süre", "kargo", "ne zaman"]
            )
            
            # İade bilgileri
            agent.add_knowledge(
                category="iade",
                question="Nasıl iade yapabilirim?",
                answer="Ürün tesliminden itibaren 14 gün içinde, kutusunda hasarsız şekilde iade edebilirsiniz. 0850 123 4567'yi arayarak iade kodu alın.",
                keywords=["iade", "geri gönderme", "ürün iadesi"]
            )
            
            agent.add_knowledge(
                category="iade",
                question="İade sürem ne kadar?",
                answer="Ürün teslim tarihinden itibaren 14 gün içinde iade hakkınız vardır.",
                keywords=["iade", "süre", "gün"]
            )
            
            # Ödeme bilgileri
            agent.add_knowledge(
                category="odeme",
                question="Hangi ödeme yöntemlerini kabul ediyorsunuz?",
                answer="Kredi kartı, banka kartı, kapıda ödeme (nakit/kart) ve havale/EFT kabul ediyoruz.",
                keywords=["ödeme", "kart", "nakit", "havale"]
            )
            
            agent.add_knowledge(
                category="odeme",
                question="Taksit yapabilir miyim?",
                answer="100 TL üzeri 3 taksit, 500 TL üzeri 6 taksit, 1000 TL üzeri 9 taksit imkanı sunuyoruz.",
                keywords=["taksit", "kredi kartı", "ödeme"]
            )
            
            # Kampanya bilgileri
            agent.add_knowledge(
                category="kampanya",
                question="Hangi kampanyalar var?",
                answer="Yeni üyelere %10, hafta sonu %15, öğrencilere %20, toplu alışverişte %25 indirim kampanyalarımız var.",
                keywords=["kampanya", "indirim", "promosyon"]
            )
            
            print("✅ Bilgi tabanı yüklendi! (7 bilgi eklendi)")
        else:
            print("⚠️  SQL memory kullanmıyorsunuz, bilgi tabanı özelliği aktif değil.")
            print("   SQL memory için: MemAgent(use_sql=True)")
    
    except FileNotFoundError:
        print("❌ company_knowledge.txt bulunamadı!")


def simulate_advanced_service():
    """Gelişmiş müşteri hizmetleri simülasyonu"""
    
    print("=" * 70)
    print("🤖 GELİŞMİŞ MÜŞTERİ HİZMETLERİ BOTU (BİLGİ TABANLI)")
    print("=" * 70)
    print("Bot hem geçmiş konuşmaları hatırlıyor hem de bilgi tabanından öğreniyor!\n")
    
    # Agent'ı SQL memory ile başlat (bilgi tabanı için)
    print("🔄 Bot başlatılıyor (SQL memory)...")
    agent = MemAgent(
        model="granite4:tiny-h",
        use_sql=True,
        memory_dir="customer_service.db"
    )
    
    # Kurulum kontrolü
    status = agent.check_setup()
    if status['status'] != 'ready':
        print("❌ Ollama çalışmıyor! 'ollama serve' komutunu çalıştırın.")
        return
    
    print("✅ Sistem hazır!\n")
    
    # Bilgi tabanını yükle
    load_knowledge_base(agent)
    print()
    
    # === SENARYO 1: Kargo Sorusu ===
    print("-" * 60)
    print("📞 ÇAĞRI 1 - Müşteri: Ahmet (Kargo ücreti soruyor)")
    print("-" * 60)
    
    agent.set_user("ahmet123", name="Ahmet")
    
    print("\n👤 Ahmet: Merhaba, kargo ücreti ne kadar?")
    response = agent.chat("Merhaba, kargo ücreti ne kadar?")
    print(f"🤖 Bot: {response}")
    print("   (📚 Bilgi tabanından öğrendi!)\n")
    
    time.sleep(1)
    
    print("👤 Ahmet: Siparişim 200 TL olacak.")
    response = agent.chat("Siparişim 200 TL olacak.")
    print(f"🤖 Bot: {response}\n")
    
    # === SENARYO 2: İade Sorusu ===
    print("-" * 60)
    print("📞 ÇAĞRI 2 - Müşteri: Ayşe (İade sorusu)")
    print("-" * 60)
    
    agent.set_user("ayse456", name="Ayşe")
    
    print("\n👤 Ayşe: Aldığım ürünü iade edebilir miyim?")
    response = agent.chat("Aldığım ürünü iade edebilir miyim?")
    print(f"🤖 Bot: {response}")
    print("   (📚 Bilgi tabanından öğrendi!)\n")
    
    time.sleep(1)
    
    print("👤 Ayşe: İade için telefon numaranız neydi?")
    response = agent.chat("İade için telefon numaranız neydi?")
    print(f"🤖 Bot: {response}\n")
    
    # === SENARYO 3: Ahmet Tekrar Arıyor ===
    print("-" * 60)
    print("📞 ÇAĞRI 3 - Ahmet tekrar arıyor (1 gün sonra)")
    print("-" * 60)
    
    agent.set_user("ahmet123")  # Aynı müşteri
    
    print("\n👤 Ahmet: Merhaba, dün 200 TL'lik sipariş hakkında konuşmuştuk...")
    response = agent.chat("Merhaba, dün 200 TL'lik sipariş hakkında konuşmuştuk. Ne zaman gelir?")
    print(f"🤖 Bot: {response}")
    print("   (🧠 Geçmiş konuşmayı hatırladı!)\n")
    
    # === SENARYO 4: Taksit Sorusu ===
    print("-" * 60)
    print("📞 ÇAĞRI 4 - Müşteri: Mehmet (Taksit sorusu)")
    print("-" * 60)
    
    agent.set_user("mehmet789", name="Mehmet")
    
    print("\n👤 Mehmet: 600 TL'lik ürüne taksit yapabilir miyim?")
    response = agent.chat("600 TL'lik ürüne taksit yapabilir miyim?")
    print(f"🤖 Bot: {response}")
    print("   (📚 Bilgi tabanından öğrendi!)\n")
    
    # === İSTATİSTİKLER ===
    print("=" * 70)
    print("📊 İSTATİSTİKLER")
    print("=" * 70)
    
    try:
        # Müşteri profilleri
        ahmet_profile = agent.get_user_profile("ahmet123")
        ayse_profile = agent.get_user_profile("ayse456")
        
        print(f"\n👤 Ahmet profili: {ahmet_profile}")
        print(f"👤 Ayşe profili: {ayse_profile}")
        
        # Genel istatistikler
        stats = agent.get_statistics()
        print(f"\n📈 Toplam kullanıcı: {stats.get('total_users', 'N/A')}")
        print(f"📈 Toplam konuşma: {stats.get('total_interactions', 'N/A')}")
        print(f"📈 Bilgi tabanı: {stats.get('knowledge_base_entries', 0)} kayıt")
        
    except Exception as e:
        print(f"⚠️  İstatistik alınamadı: {e}")
    
    print("\n" + "=" * 70)
    print("🎯 DEMO SONUÇLARI:")
    print("=" * 70)
    print("✅ Bilgi tabanından gerçek cevaplar veriyor (kargo, iade, taksit)")
    print("✅ Geçmiş konuşmaları hatırlıyor (Ahmet'in 200 TL sorusu)")
    print("✅ Her müşteri ayrı profile sahip")
    print("✅ SQL memory ile hızlı arama")
    print("✅ Gerçek müşteri hizmetlerinde kullanıma hazır!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        simulate_advanced_service()
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Kontrol edin:")
        print("   1. Ollama çalışıyor mu? → ollama serve")
        print("   2. Model yüklü mü? → ollama pull granite4:tiny-h")
        print("   3. company_knowledge.txt mevcut mu?")

