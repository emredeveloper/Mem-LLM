# 🧠 Mem-Agent: Belleği Olan Mini Asistan

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Ollama](https://img.shields.io/badge/Ollama-Compatible-orange.svg)](https://ollama.ai/)

**Sadece 4 milyon parametreli yerel bir LLM ile çalışan, kullanıcı etkileşimlerini hatırlayan ve bağlam farkındalığı ile cevap veren yapay zeka asistanı.**

[Hızlı Başlangıç](#-hızlı-başlangıç) • [Özellikler](#-özellikler) • [Dokümantasyon](#-dokümantasyon) • [Örnekler](#-kullanım-örnekleri)

</div>

---

## 🎯 Neden Mem-Agent?

Büyük dil modellerinin (LLM) çoğu her konuşmayı "yeni" olarak görür ve geçmiş etkileşimleri hatırlamaz. **Mem-Agent**, yerel olarak çalışan küçük bir model kullanarak:

- ✅ **Kullanıcı geçmişini hatırlar** - Her müşteri/kullanıcı için ayrı bellek
- ✅ **Bağlam farkındalığı** - Önceki konuşmalara göre cevap verir
- ✅ **Tamamen yerel** - İnternet bağlantısı gerektirmez
- ✅ **Hafif ve hızlı** - Sadece 2.5 GB model boyutu
- ✅ **Kolay entegrasyon** - 3 satır kod ile başlayın

## 🚀 Hızlı Başlangıç

### 1. Ollama'yı Kurun

```bash
# Windows/Mac/Linux için: https://ollama.ai/download
curl https://ollama.ai/install.sh | sh

# Servisi başlatın
ollama serve
```

### 2. Modeli İndirin

```bash
ollama pull granite4:tiny-h
```

### 3. Mem-Agent'ı Kullanın

```python
from mem_agent import MemAgent

# Agent oluştur
agent = MemAgent(model="granite4:tiny-h")

# Kullanıcı ayarla
agent.set_user("ahmet123", name="Ahmet")

# Konuşmaya başla
response = agent.chat("Merhaba, siparişim nerede?")
print(response)

# Bot geçmişi hatırlayacak
response = agent.chat("Kargo ne zaman gelir?")
print(response)  # Önceki konuşmayı hatırlayarak cevap verir
```

**Bu kadar!** ✨

## ⭐ Özellikler

### 🧠 Bellek Sistemi

- **JSON Bellek**: Basit, dosya bazlı bellek (başlangıç için)
- **SQL Bellek**: Gelişmiş, ilişkisel veritabanı (production için)
- **Kullanıcı Profilleri**: Her kullanıcı için ayrı veri
- **Arama Özellikleri**: Geçmiş konuşmalarda arama

### 🎨 Prompt Şablonları

8+ hazır kullanıma hazır şablon:

| Şablon | Kullanım Alanı |
|--------|----------------|
| `personal_assistant` | Kişisel asistan |
| `customer_service` | Müşteri hizmetleri |
| `tech_support` | Teknik destek |
| `sales_assistant` | Satış danışmanı |
| `education_tutor` | Eğitim asistanı |
| Ve daha fazlası... | |

### 📚 Bilgi Bankası

- Sık sorulan soruları (FAQ) depolayın
- Otomatik bilgi arama
- Özel bilgi bankası yükleme
- Excel/CSV import desteği

### 🛠️ Kullanıcı Araçları

Kullanıcılar doğal dille:
- Geçmiş konuşmalarını görüntüleyebilir
- Aramalar yapabilir
- Verilerini dışa aktarabilir
- Bellek yönetimi yapabilir

### 🔧 İki Kullanım Modu

**Personal (Kişisel)** 🏠
- Bireysel kullanım
- Hatırlatmalar
- Öğrenme takibi
- Kişisel notlar

**Business (Kurumsal)** 💼
- Çoklu kullanıcı desteği
- Müşteri hizmetleri
- Raporlama
- Güvenlik özellikleri

## 💼 Kullanım Senaryoları

### Müşteri Hizmetleri

```python
from mem_agent import MemAgent

agent = MemAgent(
    config_file="config.yaml",  # Müşteri hizmetleri ayarları
    use_sql=True,               # Çoklu kullanıcı için
    load_knowledge_base=True    # FAQ için
)

# Müşteri 1
agent.set_user("customer_001", name="Ali Yılmaz")
response = agent.chat("Siparişim ne zaman gelecek?")

# Müşteri 2
agent.set_user("customer_002", name="Ayşe Demir")
response = agent.chat("İade yapmak istiyorum")

# Ali tekrar arıyor - geçmişi hatırlayacak
agent.set_user("customer_001")
response = agent.chat("Siparişimi iptal edebilir miyim?")
```

### Kişisel Asistan

```python
agent = MemAgent(use_sql=False)  # Basit kullanım
agent.set_user("me")

agent.chat("Yarın saat 15:00'de diş randevum var, hatırlat")
# ... bir gün sonra ...
agent.chat("Bugün ne yapmam gerekiyor?")
# Bot: "Saat 15:00'de diş randevunuz var!"
```

## 📊 Karşılaştırma

| Özellik | Standart LLM | Mem-Agent |
|---------|--------------|-----------|
| Kullanıcı Belleği | ❌ | ✅ |
| Geçmiş Hatırlama | ❌ | ✅ |
| Bağlam Farkındalığı | Sınırlı | ✅ Gelişmiş |
| İnternet Gereksinimi | Genelde ✅ | ❌ Tamamen yerel |
| Model Boyutu | 10GB+ | 2.5GB |
| Başlatma Süresi | Yavaş | ⚡ Hızlı |
| Maliyet | Ücretli API | 💰 Ücretsiz |

## 📁 Proje Yapısı

```
Memory LLM/
├── 📦 Core Modüller
│   ├── mem_agent.py          # Ana agent sınıfı
│   ├── memory_manager.py     # JSON bellek
│   ├── memory_db.py          # SQL bellek
│   └── memory_tools.py       # Kullanıcı araçları
│
├── 📚 examples/              # Kullanım örnekleri
│   ├── example_simple.py
│   ├── example_business_mode.py
│   └── example_customer_service.py
│
├── 🧪 tests/                 # Test dosyaları
│   └── run_all_tests.py
│
└── 📖 docs/                  # Dokümantasyon
    ├── CONFIG_GUIDE.md       # Yapılandırma rehberi
    └── INDEX.md              # Tüm dokümantasyon
```

## 🛠️ Kurulum

### Gereksinimler

- Python 3.8+
- Ollama (yerel LLM sunucusu)
- 4GB+ RAM

### Adım Adım

```bash
# 1. Projeyi klonlayın
git clone https://github.com/yourusername/mem-agent.git
cd mem-agent

# 2. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 3. Config dosyası oluşturun (opsiyonel)
cp config.yaml.example config.yaml

# 4. İlk örneği çalıştırın
cd examples
python example_simple.py
```

Detaylı kurulum için: [QUICKSTART_TR.md](QUICKSTART_TR.md)

## 📖 Dokümantasyon

| Dosya | Açıklama |
|-------|----------|
| [QUICKSTART_TR.md](QUICKSTART_TR.md) | 5 dakikalık hızlı başlangıç |
| [docs/CONFIG_GUIDE.md](docs/CONFIG_GUIDE.md) | Yapılandırma rehberi |
| [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) | Entegrasyon rehberi |
| [STRUCTURE.md](STRUCTURE.md) | Proje yapısı |
| [CHANGELOG.md](CHANGELOG.md) | Değişiklik günlüğü |

## 🎓 Kullanım Örnekleri

```python
# Örnek 1: Basit Kullanım
from mem_agent import MemAgent

agent = MemAgent()
agent.set_user("user123")
response = agent.chat("Merhaba!")

# Örnek 2: Config ile
agent = MemAgent(config_file="config.yaml")

# Örnek 3: SQL Bellek ile
agent = MemAgent(use_sql=True, load_knowledge_base=True)

# Örnek 4: Metadata ile
response = agent.chat(
    "Sipariş #12345 nerede?",
    metadata={"order_id": "12345", "priority": "high"}
)

# Örnek 5: Geçmişte Arama
results = agent.search_history("laptop", user_id="user123")
```

Daha fazla örnek için: [`examples/`](examples/) klasörü

## 🧪 Testler

```bash
cd tests
python run_all_tests.py

# Veya belirli testler
python run_all_tests.py basic
python run_all_tests.py integration
```

## ⚙️ Yapılandırma

Minimal config örneği:

```yaml
# config.yaml
usage_mode: "personal"

llm:
  model: "granite4:tiny-h"
  base_url: "http://localhost:11434"

memory:
  backend: "json"
```

Detaylı yapılandırma için: [docs/CONFIG_GUIDE.md](docs/CONFIG_GUIDE.md)

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing`)
5. Pull Request açın

## 📝 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

## 🌟 Yıldız Verin!

Bu proje işinize yaradıysa, lütfen ⭐ vererek destek olun!

## 📧 İletişim

- GitHub Issues: Hata raporları ve özellik istekleri
- Discussions: Soru ve tartışmalar

## 🙏 Teşekkürler

- [Ollama](https://ollama.ai/) - Yerel LLM altyapısı
- Granite4 Model - Hafif ve güçlü model
- Topluluğa katkıda bulunan herkese 🎉

---

<div align="center">

**[⬆ Başa Dön](#-mem-agent-belleği-olan-mini-asistan)**

Made with ❤️ in Turkey

</div>

