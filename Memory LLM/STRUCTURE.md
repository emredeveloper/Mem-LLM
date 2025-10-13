# 📁 Memory LLM Proje Yapısı

Bu dosya projenin klasör ve dosya organizasyonunu açıklar.

## 🌳 Klasör Ağacı

```
Memory LLM/
│
├── 📦 Core Modüller (Ana Klasör)
│   ├── mem_agent.py              # Ana agent sınıfı (birleşik sistem)
│   ├── memory_manager.py         # JSON bellek yöneticisi
│   ├── memory_db.py              # SQL bellek yöneticisi
│   ├── memory_tools.py           # Kullanıcı araçları sistemi
│   ├── llm_client.py             # LLM (Ollama) bağlantı istemcisi
│   ├── prompt_templates.py       # Prompt şablon sistemi
│   ├── config_manager.py         # YAML yapılandırma yöneticisi
│   ├── knowledge_loader.py       # Bilgi bankası yükleyici
│   └── __init__.py               # Paket başlatıcı
│
├── 🧪 tests/                     # Test dosyaları
│   ├── __init__.py
│   ├── test_mem_agent.py         # Ana agent testleri
│   ├── test_integration.py       # Entegrasyon testleri
│   ├── test_memory_manager.py    # Bellek yöneticisi testleri
│   ├── test_memory_tools.py      # Araçlar testleri
│   ├── test_llm_client.py        # LLM istemcisi testleri
│   └── run_all_tests.py          # Tüm testleri çalıştırma scripti
│
├── 📚 examples/                  # Örnek kullanım kodları
│   ├── __init__.py
│   ├── README.md                 # Örnekler hakkında bilgi
│   ├── example_simple.py         # Basit başlangıç örneği
│   ├── example_business_mode.py  # Kurumsal kullanım
│   ├── example_personal_mode.py  # Kişisel asistan
│   ├── example_customer_service.py # Müşteri hizmetleri
│   ├── example_memory_tools.py   # Bellek araçları
│   └── demo_user_tools.py        # Kullanıcı araçları demosu
│
├── 📖 docs/                      # Dokümantasyon klasörü
│   ├── README.md                 # Docs hakkında
│   └── INDEX.md                  # Dokümantasyon indeksi
│
├── 📄 Yapılandırma ve Metadata
│   ├── config.yaml               # Ana yapılandırma dosyası
│   ├── requirements.txt          # Python bağımlılıkları
│   ├── setup.py                  # Kurulum scripti
│   └── .gitignore                # Git ignore kuralları
│
├── 📝 Dokümantasyon (Ana Klasör)
│   ├── README_UPDATED.md         # Ana README
│   ├── QUICKSTART_TR.md          # Hızlı başlangıç kılavuzu (TR)
│   ├── INTEGRATION_GUIDE.md      # Entegrasyon rehberi
│   ├── CHANGELOG.md              # Değişiklik günlüğü
│   ├── STRUCTURE.md              # Bu dosya - proje yapısı
│   └── LICENSE                   # MIT lisansı
│
└── 💾 Veri Dosyaları
    └── memories.db               # SQLite veritabanı (runtime)
```

## 📦 Modül Açıklamaları

### Core Modüller

#### `mem_agent.py` (Ana Modül)
- **MemAgent** sınıfı - Tüm özellikleri birleştiren ana sınıf
- SQL ve JSON bellek desteği
- Prompt şablonları entegrasyonu
- Bilgi bankası yönetimi
- Business/Personal modları

#### `memory_manager.py`
- JSON tabanlı basit bellek yöneticisi
- Dosya bazlı veri saklama
- Kullanıcı profilleri
- Konuşma geçmişi

#### `memory_db.py`
- SQL tabanlı gelişmiş bellek yöneticisi
- SQLite veritabanı
- İlişkisel veri modeli
- Bilgi bankası tabloları

#### `memory_tools.py`
- Kullanıcı araçları sistemi
- Bellek sorguları
- Veri dışa aktarma
- Doğal dil komutları

#### `llm_client.py`
- Ollama API istemcisi
- Model yönetimi
- Chat fonksiyonları
- Bağlantı kontrolü

#### `prompt_templates.py`
- Jinja2 tabanlı şablon sistemi
- 8+ hazır şablon
- Değişken desteği
- Runtime şablon değiştirme

#### `config_manager.py`
- YAML yapılandırma yönetimi
- Nokta notasyonu desteği
- Varsayılan değerler

#### `knowledge_loader.py`
- Bilgi bankası yükleme
- Excel/CSV import
- Varsayılan KB şablonları

## 🎯 Kullanım Akışı

### 1. Basit Kullanım (JSON Bellek)
```python
from mem_agent import MemAgent

agent = MemAgent(use_sql=False)
agent.set_user("user123")
response = agent.chat("Merhaba!")
```

### 2. Gelişmiş Kullanım (SQL + Config)
```python
from mem_agent import MemAgent

agent = MemAgent(
    config_file="config.yaml",
    use_sql=True,
    load_knowledge_base=True
)
agent.set_user("user456", name="Ali")
response = agent.chat("Kampanya var mı?")
```

### 3. Test Çalıştırma
```bash
cd tests/
python run_all_tests.py
```

### 4. Örnekleri Deneme
```bash
cd examples/
python example_simple.py
python example_business_mode.py
```

## 📐 Tasarım Prensipleri

### 1. Modülerlik
- Her modül tek bir sorumluluğa sahip
- Bağımsız test edilebilir
- Kolay değiştirilebilir

### 2. Geriye Uyumluluk
- JSON ve SQL modları aynı arayüzü kullanır
- Config opsiyoneldir
- Varsayılan ayarlar her zaman çalışır

### 3. Kolay Kullanım
- Basit başlangıç için tek satır kod
- Gelişmiş özellikler için config desteği
- Bol örnek ve dokümantasyon

### 4. Production Ready
- Loglama sistemi
- Hata yönetimi
- Performans optimizasyonları
- Thread-safe operasyonlar

## 🔄 İmport Path'leri

### Ana klasörden import
```python
from mem_agent import MemAgent
from memory_manager import MemoryManager
from memory_db import SQLMemoryManager
from llm_client import OllamaClient
```

### tests/ klasöründen import
```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mem_agent import MemAgent
```

### examples/ klasöründen import
```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mem_agent import MemAgent
```

## 🚀 Deployment

Proje farklı şekillerde deploy edilebilir:

1. **Standalone Script**
   - Doğrudan Python scripti olarak
   - `python my_bot.py`

2. **Package Install**
   - `pip install -e .`
   - Her yerden import edilebilir

3. **Web API**
   - Flask/FastAPI wrapper ekleyerek
   - REST API servisi

4. **Docker Container**
   - Dockerfile oluşturarak
   - Containerize deployment

## 📊 Versiyon Bilgisi

- **Versiyon**: 2.0.0
- **Son Güncelleme**: 2025-10-13
- **Python Uyumluluk**: 3.8+
- **Lisans**: MIT

---

Bu yapı, hem basit kullanım hem de enterprise-level deployment için optimize edilmiştir.

