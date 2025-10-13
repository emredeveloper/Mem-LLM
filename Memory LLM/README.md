# 🧠 Mem-Agent: Belleği Olan Mini Asistan

Sadece **4 milyar parametreli** yerel bir LLM ile çalışan, kullanıcı etkileşimlerini hatırlayan ve bağlam farkındalığı ile cevap veren yapay zeka asistanı.

## 🎯 Proje Amacı

Büyük dil modellerinin (LLM) çoğu her konuşmayı "yeni" olarak görür ve geçmiş etkileşimleri hatırlamaz. Mem-Agent, **yerel olarak çalışan küçük bir model** kullanarak:

- 🧠 Kullanıcı etkileşimlerini hatırlar
- 💾 Konuşma geçmişini saklar
- 🎯 Bağlam farkındalığı ile cevaplar
- 🏠 Tamamen yerel ve gizli çalışır

## 📦 Kurulum

### 1. Ollama Kurulumu

```bash
# Ollama'yı yükleyin (https://ollama.ai/)
# Windows: ollama.exe installer
# Mac: brew install ollama
# Linux: curl https://ollama.ai/install.sh | sh

# Ollama servisini başlatın
ollama serve
```

### 2. Model İndirme

```bash
# Granite4 tiny model'i indirin (yaklaşık 2.5 GB)
ollama pull granite4:tiny-h
```

### 3. Mem-Agent Kurulumu

```bash
# Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

# Veya development modu için:
pip install -e .
```

## 🚀 Hızlı Başlangıç

### Basit Kullanım

```python
from mem_agent import MemAgent

# Agent oluştur
agent = MemAgent(model="granite4:tiny-h")

# Sistem kontrolü
status = agent.check_setup()
if status['status'] == 'ready':
    print("✅ Sistem hazır!")
else:
    print("❌ Hata:", status)

# Kullanıcı ayarla
agent.set_user("user123")

# İlk konuşma
response = agent.chat("Merhaba, benim adım Ali")
print(response)

# İkinci konuşma - Beni hatırlıyor!
response = agent.chat("Adımı hatırlıyor musun?")
print(response)
```

### Müşteri Hizmetleri Örneği

```python
from mem_agent import MemAgent

agent = MemAgent()
agent.set_user("ahmet123")

# İlk gün
response = agent.chat(
    "Siparişim nerede?",
    metadata={"order": "#12345", "issue": "kargo gecikmesi"}
)

# 3 gün sonra - Geçmişi hatırlıyor
response = agent.chat("Merhaba yine ben")
# Bot: "Merhaba Ahmet! #12345 numaralı siparişinizle ilgilenmiştim..."
```

## 📚 Örnek Scriptler

### 1. Basit Test

```bash
python example_simple.py
```

### 2. Müşteri Hizmetleri Simülasyonu

```bash
python example_customer_service.py
```

## 🏗️ Proje Yapısı

```
Memory LLM/
├── __init__.py              # Paket başlatma
├── mem_agent.py             # Ana asistan sınıfı
├── memory_manager.py        # Bellek yönetimi
├── llm_client.py            # Ollama entegrasyonu
├── example_simple.py        # Basit örnek
├── example_customer_service.py  # Müşteri hizmetleri örneği
├── setup.py                 # Kurulum scripti
├── requirements.txt         # Bağımlılıklar
└── README.md               # Bu dosya
```

## 🔧 API Kullanımı

### MemAgent Sınıfı

```python
from mem_agent import MemAgent

agent = MemAgent(
    model="granite4:tiny-h",           # Ollama model adı
    memory_dir="memories",             # Bellek dizini
    ollama_url="http://localhost:11434" # Ollama API URL
)
```

#### Temel Metodlar

```python
# Kullanıcı ayarla
agent.set_user("user_id")

# Sohbet et
response = agent.chat(
    message="Merhaba",
    user_id="optional_user_id",  # set_user kullanılmadıysa
    metadata={"key": "value"}     # Ek bilgiler
)

# Bellek özeti al
summary = agent.memory_manager.get_summary("user_id")

# Geçmişte ara
results = agent.search_user_history("anahtar_kelime", "user_id")

# Profil güncelle
agent.update_user_info({
    "name": "Ali",
    "preferences": {"language": "tr"}
})

# İstatistikler
stats = agent.get_statistics()

# Belleği export et
json_data = agent.export_memory("user_id")

# Belleği temizle (DİKKAT!)
agent.clear_user_memory("user_id", confirm=True)
```

### MemoryManager Sınıfı

```python
from memory_manager import MemoryManager

memory = MemoryManager(memory_dir="memories")

# Bellek yükle
data = memory.load_memory("user_id")

# Etkileşim ekle
memory.add_interaction(
    user_id="user_id",
    user_message="Merhaba",
    bot_response="Merhaba! Nasıl yardımcı olabilirim?",
    metadata={"timestamp": "2025-10-13"}
)

# Son konuşmaları al
recent = memory.get_recent_conversations("user_id", limit=5)

# Arama
results = memory.search_memory("user_id", "sipariş")
```

### OllamaClient Sınıfı

```python
from llm_client import OllamaClient

client = OllamaClient(model="granite4:tiny-h")

# Basit üretim
response = client.generate("Merhaba dünya!")

# Sohbet formatı
response = client.chat([
    {"role": "system", "content": "Sen yardımsever bir asistansın"},
    {"role": "user", "content": "Merhaba"}
])

# Bağlantı kontrolü
is_ready = client.check_connection()

# Model listesi
models = client.list_models()
```

## 💡 Kullanım Senaryoları

### 1. Müşteri Hizmetleri Botu
- Müşteri geçmişini hatırlar
- Önceki sorunları bilir
- Kişiselleştirilmiş öneriler yapar

### 2. Kişisel Asistan
- Günlük aktiviteleri takip eder
- Tercihleri öğrenir
- Hatırlatmalar yapar

### 3. Eğitim Asistanı
- Öğrenci ilerlemesini takip eder
- Zorluk seviyesini ayarlar
- Geçmiş hataları hatırlar

### 4. Destek Ticket Sistemi
- Ticket geçmişini saklar
- İlgili eski ticket'ları bulur
- Çözüm önerileri sunar

## 📊 Bellek Formatı

Bellekler JSON formatında saklanır:

```json
{
  "conversations": [
    {
      "timestamp": "2025-10-13T10:30:00",
      "user_message": "Merhaba",
      "bot_response": "Merhaba! Nasıl yardımcı olabilirim?",
      "metadata": {
        "topic": "selamlama"
      }
    }
  ],
  "profile": {
    "user_id": "user123",
    "first_seen": "2025-10-13T10:30:00",
    "preferences": {},
    "summary": {}
  },
  "last_updated": "2025-10-13T10:35:00"
}
```

## 🔒 Gizlilik ve Güvenlik

- ✅ Tamamen yerel çalışır (internet bağlantısı gerektirmez)
- ✅ Veriler bilgisayarınızda saklanır
- ✅ Üçüncü parti servislere veri gönderilmez
- ✅ Bellekler JSON formatında, kolayca silinebilir

## 🛠️ Geliştirme

### Test Modu

```python
# Belleksiz basit sohbet (test için)
response = agent.simple_chat("Test mesajı")
```

### Kendi Modelinizi Kullanma

```python
# Farklı bir Ollama modeli
agent = MemAgent(model="llama2:7b")

# Veya başka bir LLM API
# llm_client.py dosyasını özelleştirin
```

## 🐛 Sorun Giderme

### Ollama Bağlantı Hatası

```bash
# Ollama servisini başlatın
ollama serve

# Port kontrolü
netstat -an | findstr "11434"
```

### Model Bulunamadı

```bash
# Model listesini kontrol edin
ollama list

# Model indirin
ollama pull granite4:tiny-h
```

### Bellek Sorunları

```python
# Bellek dizinini kontrol edin
import os
os.path.exists("memories")

# Bellek dosyalarını listeleyin
os.listdir("memories")
```

## 📈 Performans

- **Model Boyutu**: ~2.5 GB
- **Yanıt Süresi**: ~1-3 saniye (CPU'ya bağlı)
- **Bellek Kullanımı**: ~4-6 GB RAM
- **Disk Kullanımı**: Kullanıcı başına ~10-50 KB

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'feat: Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📝 Lisans

MIT License - Detaylar için LICENSE dosyasına bakın.

## 🙏 Teşekkürler

- [Ollama](https://ollama.ai/) - Yerel LLM sunucusu
- [Granite](https://www.ibm.com/granite) - IBM Granite modelleri

## 📞 İletişim

Sorularınız için issue açabilirsiniz.

---

**Not**: Bu proje eğitim ve araştırma amaçlıdır. Üretim ortamında kullanmadan önce kapsamlı test yapın.

