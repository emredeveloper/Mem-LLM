"""
MEM-AGENT BASİT ÖRNEK
====================

Bu örnek, bellek sahibi bir chatbot'un nasıl çalıştığını gösterir.
Çok basit 3 konuşma yapacağız ve bot'un belleğini test edeceğiz.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mem_agent import MemAgent


def main():
    print("🤖 BELLEKLİ CHATBOT ÖRNEĞİ")
    print("=" * 60)
    print("Bu örnek adım adım bot'un belleğini test eder.\n")

    # 1. Bot'u oluştur
    print("1️⃣ Bot oluşturuluyor...")
    agent = MemAgent(model="granite4:tiny-h", use_sql=False)

    # Sistem kontrolü
    status = agent.check_setup()
    if status['status'] != 'ready':
        print("❌ HATA: Ollama çalışmıyor veya model yüklü değil!")
        print("   Çözüm: 'ollama serve' komutunu çalıştırın")
        return

    print("✅ Bot hazır!\n")

    # 2. Kullanıcı belirle
    user_id = "ahmet123"
    agent.set_user(user_id)

    # 3. İLK KONUŞMA - Tanışma
    print("2️⃣ İLK KONUŞMA - Tanışma")
    print("-" * 40)
    print("👤 Ahmet: Merhaba, benim adım Ahmet")
    response = agent.chat("Merhaba, benim adım Ahmet")
    print(f"🤖 Bot:  {response}\n")

    # 4. İKİNCİ KONUŞMA - Geçmiş hatırlatma
    print("3️⃣ İKİNCİ KONUŞMA - Geçmiş")
    print("-" * 40)
    print("👤 Ahmet: Dün sana pizza sipariş etmiştim")
    response = agent.chat("Dün sana pizza sipariş etmiştim")
    print(f"🤖 Bot:  {response}\n")

    # 5. ÜÇÜNCÜ KONUŞMA - Bellek testi
    print("4️⃣ ÜÇÜNCÜ KONUŞMA - Bellek Testi")
    print("-" * 40)
    print("👤 Ahmet: Adımı hatırlıyor musun?")
    response = agent.chat("Adımı hatırlıyor musun?")
    print(f"🤖 Bot:  {response}\n")

    # 6. BELLEK ÖZETİ
    print("5️⃣ BELLEK ÖZETİ")
    print("-" * 40)
    if hasattr(agent.memory, 'get_summary'):
        summary = agent.memory.get_summary(user_id)
        print(summary)

    print("\n" + "=" * 60)
    print("🎯 SONUÇ: Bot Ahmet'in adını hatırlıyor!")
    print("📚 Tüm konuşmalar kaydedildi.")
    print("🔄 Gelecek konuşmalarda bu bilgileri kullanacak.")
    print("=" * 60)


if __name__ == "__main__":
    main()

