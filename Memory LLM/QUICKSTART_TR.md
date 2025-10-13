# ⚡ Hızlı Başlangıç - Mem-Agent

5 dakikada Mem-Agent'ı çalıştırmaya başlayın!

## 🎯 Adım 1: Ollama Kurulumu

### Windows
```bash
# Ollama web sitesinden indirin ve kurun
# https://ollama.ai/download/windows

# Kurulum sonrası terminal açın ve kontrol edin:
ollama --version
```

### Mac/Linux
```bash
# Tek komutla kurulum:
curl https://ollama.ai/install.sh | sh

# Veya Homebrew ile (Mac):
brew install ollama
```

## 🚀 Adım 2: Ollama Servisini Başlatın

```bash
# Yeni bir terminal açın ve servisi başlatın:
ollama serve
```

**Not**: Bu terminal açık kalmalı! Başka bir terminal açarak devam edin.

## 📦 Adım 3: Model İndirin

```bash
# Granite4 tiny modelini indirin (yaklaşık 2.5 GB)
ollama pull granite4:tiny-h

# İndirme tamamlandığında modeli kontrol edin:
ollama list
```

Çıktıda `granite4:tiny-h` görmelisiniz.

## 🔧 Adım 4: Python Bağımlılıklarını Yükleyin

```bash
# Memory LLM dizinine gidin
cd "Memory LLM"

# Gereksinimleri yükleyin
pip install -r requirements.txt

# VEYA geliştirme modu için:
pip install -e .
```

## ⚙️ Adım 4.5: Config Dosyasını Hazırlayın (Opsiyonel)

Config dosyası kullanmadan da başlayabilirsiniz, ancak gelişmiş özellikler için önerilir:

```bash
# Örnek config'i kopyalayın
cp config.yaml.example config.yaml

# Windows için:
copy config.yaml.example config.yaml
```

**Basit başlangıç config'i (config.yaml):**

```yaml
usage_mode: "personal"

llm:
  model: "granite4:tiny-h"
  base_url: "http://localhost:11434"

memory:
  backend: "json"
```

**💡 Not:** Config kullanmadan da çalışır! Detaylar için `docs/CONFIG_GUIDE.md`

## ✅ Adım 5: İlk Testinizi Yapın

```bash
# Basit örneği çalıştırın:
python example_simple.py
```

Eğer her şey doğruysa şöyle bir çıktı görmelisiniz:

```
🤖 Mem-Agent Basit Örnek

✅ Sistem hazır!

--- Konuşma 1 ---
👤: Merhaba, benim adım Ali
🤖: [Bot cevabı]

--- Konuşma 2 ---
👤: Dün sana pizza sipariş etmiştim
🤖: [Bot cevabı]

--- Konuşma 3 ---
👤: Adımı hatırlıyor musun?
🤖: [Bot Ali'yi hatırlayarak cevap verir]
```

## 🎉 Adım 6: Müşteri Hizmetleri Demo

```bash
# Gelişmiş örneği çalıştırın:
python example_customer_service.py
```

Bu, tam bir müşteri hizmetleri senaryosunu simüle eder.

## 💻 Kendi Kodunuzda Kullanım

```python
from mem_agent import MemAgent

# 1. Agent oluştur
agent = MemAgent(model="granite4:tiny-h")

# 2. Sistem kontrolü (opsiyonel ama önerilen)
status = agent.check_setup()
if status['status'] != 'ready':
    print("❌ Hata:", status)
    exit(1)

# 3. Kullanıcı ayarla
agent.set_user("kullanici_id")

# 4. Sohbet et
response = agent.chat("Merhaba!")
print(response)

# 5. Metadata ile kayıt
response = agent.chat(
    "Sipariş #12345 nerede?",
    metadata={
        "order_number": "#12345",
        "topic": "sipariş sorgu"
    }
)
print(response)

# 6. Bellek özeti
summary = agent.memory_manager.get_summary("kullanici_id")
print(summary)
```

## 🐛 Sorun mu Yaşıyorsunuz?

### "Connection refused" hatası
```bash
# Ollama servisinin çalıştığından emin olun:
ollama serve

# Başka bir terminalde test edin:
curl http://localhost:11434/api/tags
```

### "Model not found" hatası
```bash
# Modeli tekrar indirin:
ollama pull granite4:tiny-h

# Model listesini kontrol edin:
ollama list
```

### Import hatası
```bash
# Doğru dizinde olduğunuzdan emin olun:
cd "Memory LLM"

# Bağımlılıkları tekrar yükleyin:
pip install -r requirements.txt
```

## 📚 Sonraki Adımlar

1. ✅ `README.md` dosyasını okuyun - Detaylı API dokümantasyonu
2. ✅ `example_simple.py` kodunu inceleyin - Basit örnekler
3. ✅ `example_customer_service.py` kodunu inceleyin - İleri seviye örnekler
4. ✅ Kendi use case'iniz için özelleştirin

## 🎯 Önerilen Kullanım Örnekleri

### 1. Chatbot Oluşturma
```python
agent = MemAgent()
agent.set_user("chat_user")

while True:
    user_input = input("Siz: ")
    if user_input.lower() == 'çıkış':
        break
    
    response = agent.chat(user_input)
    print(f"Bot: {response}")
```

### 2. Müşteri Destek Sistemi
```python
def handle_support_ticket(user_id, message, ticket_no):
    agent = MemAgent()
    agent.set_user(user_id)
    
    response = agent.chat(
        message,
        metadata={
            "ticket": ticket_no,
            "timestamp": datetime.now().isoformat()
        }
    )
    
    return response
```

### 3. Kişisel Asistan
```python
agent = MemAgent()
agent.set_user("personal_user")

# Kullanıcı tercihlerini kaydet
agent.update_user_info({
    "name": "Ali",
    "preferences": {
        "language": "Turkish",
        "notification_time": "09:00"
    }
})

# Daha sonra bu bilgileri kullan
response = agent.chat("Bugün ne yapmam gerek?")
```

## 🔗 Faydalı Linkler

- 📖 [Tam Dokümantasyon](README.md)
- 🌐 [Ollama Resmi Site](https://ollama.ai/)
- 💬 [GitHub Issues](https://github.com/yourusername/mem-agent/issues)

---

**Başarılar!** 🎉

Herhangi bir sorunla karşılaşırsanız README.md dosyasındaki "Sorun Giderme" bölümüne bakın.

