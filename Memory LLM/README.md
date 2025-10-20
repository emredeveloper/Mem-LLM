# 🧠 mem-llm

**Memory-enabled AI assistant that remembers conversations using local LLMs**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/mem-llm?label=PyPI)](https://pypi.org/project/mem-llm/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📚 İçindekiler

- [🎯 mem-llm nedir?](#-mem-llm-nedir)
- [⚡ Hızlı başlangıç](#-hızlı-başlangıç)
- [🧑‍🏫 Tutorial](#-tutorial)
- [💡 Özellikler](#-özellikler)
- [📖 Kullanım örnekleri](#-kullanım-örnekleri)
- [🔧 Yapılandırma seçenekleri](#-yapılandırma-seçenekleri)
- [🗂 Bilgi tabanı ve dokümanlardan yapılandırma](#-bilgi-tabanı-ve-dokümanlardan-yapılandırma)
- [🔥 Desteklenen modeller](#-desteklenen-modeller)
- [📦 Gereksinimler](#-gereksinimler)
- [🐛 Sık karşılaşılan problemler](#-sık-karşılaşılan-problemler)

---

## 🎯 mem-llm nedir?

`mem-llm`, yerel bir LLM ile çalışan sohbet botlarınıza **kalıcı hafıza** kazandıran hafif bir Python kütüphanesidir. Her kullanıcı için ayrı bir konuşma geçmişi tutulur ve yapay zeka bu geçmişi bir sonraki oturumda otomatik olarak kullanır.

**Nerelerde kullanılabilir?**
- 💬 Müşteri hizmetleri botları
- 🤖 Kişisel asistanlar
- 📝 Bağlama duyarlı uygulamalar
- 🏢 İş süreçlerini otomatikleştiren çözümler

---

## ⚡ Hızlı başlangıç

### 0. Gereksinimleri kontrol edin

- Python 3.8 veya üzeri
- [Ollama](https://ollama.ai/) kurulu ve çalışır durumda
- En az 4GB RAM ve 5GB disk alanı

### 1. Paketi yükleyin

```bash
pip install mem-llm==1.0.7
```

### 2. Ollama'yı başlatın ve modeli indirin (tek seferlik)

```bash
# Ollama servisini başlatın
ollama serve

# Yaklaşık 2.5GB'lık hafif modeli indirin
ollama pull granite4:tiny-h
```

> 💡 Ollama `serve` komutu terminalde açık kalmalıdır. Yeni bir terminal sekmesinde Python kodunu çalıştırabilirsiniz.

### 3. İlk ajanınızı çalıştırın

```python
from mem_llm import MemAgent

# Tek satırda ajan oluşturun
agent = MemAgent()

# Kullanıcıyı belirleyin (her kullanıcı için ayrı hafıza tutulur)
agent.set_user("john")

# Sohbet edin - hafıza devrede!
agent.chat("My name is John")
agent.chat("What's my name?")  # → "Your name is John"
```

### 4. Kurulumunuzu doğrulayın (isteğe bağlı)

```python
agent.check_setup()
# {'ollama': 'running', 'model': 'granite4:tiny-h', 'memory_backend': 'sql', ...}
```

<<<<<<< HEAD
| Feature | Description |
|---------|-------------|
| 🧠 **Memory** | Remembers each user's conversation history |
| 👥 **Multi-user** | Separate memory for each user |
| 🔒 **Privacy** | 100% local, no cloud/API needed |
| ⚡ **Fast** | Lightweight SQLite/JSON storage |
| 🎯 **Simple** | 3 lines of code to get started |
| 📚 **Knowledge Base** | Config-free document integration |
| 🌍 **Multi-language** | Works with any language |
| 🛠️ **CLI Tool** | Built-in command-line interface |

---

## 🔄 Memory Backend Comparison

Choose the right backend for your needs:

| Feature | JSON Mode | SQL Mode |
|---------|-----------|----------|
| **Setup** | ✅ Zero config | ⚙️ Minimal config |
| **Conversation Memory** | ✅ Yes | ✅ Yes |
| **User Profiles** | ✅ Yes | ✅ Yes |
| **Knowledge Base** | ❌ No | ✅ Yes |
| **Advanced Search** | ❌ No | ✅ Yes |
| **Multi-user Performance** | ⭐⭐ Good | ⭐⭐⭐ Excellent |
| **Data Queries** | ❌ Limited | ✅ Full SQL |
| **Best For** | 🏠 Personal use | 🏢 Business use |

**Recommendation:**
- **JSON Mode**: Perfect for personal assistants and quick prototypes
- **SQL Mode**: Ideal for customer service, multi-user apps, and production
=======
Kurulum sırasında sorun yaşarsanız [🐛 Sık karşılaşılan problemler](#-sık-karşılaşılan-problemler) bölümüne göz atın.
>>>>>>> f002396c8c531e4cde33d19ac6a755494b1b30cd

---

## 💡 Özellikler

<<<<<<< HEAD
### Command Line Interface (CLI)

The easiest way to get started:

```bash
# Install with CLI support
pip install mem-llm

# Start interactive chat
mem-llm chat --user john

# Check system status
mem-llm check

# View statistics
mem-llm stats

# Export user data
mem-llm export john --format json --output data.json

# Get help
mem-llm --help
```

**Available CLI Commands:**

| Command | Description | Example |
|---------|-------------|---------|
| `chat` | Interactive chat session | `mem-llm chat --user alice` |
| `check` | Verify system setup | `mem-llm check` |
| `stats` | Show statistics | `mem-llm stats --user john` |
| `export` | Export user data | `mem-llm export john` |
| `clear` | Delete user data | `mem-llm clear john` |

### Basic Chat
=======
| Özellik | Açıklama |
|---------|----------|
| 🧠 **Kalıcı hafıza** | Her kullanıcının sohbet geçmişi saklanır |
| 👥 **Çoklu kullanıcı** | Her kullanıcı için ayrı hafıza yönetimi |
| 🔒 **Gizlilik** | Tamamen yerel çalışır, buluta veri göndermez |
| ⚡ **Hızlı** | Hafif SQLite veya JSON depolama seçenekleri |
| 🎯 **Kolay kullanım** | Üç satırda çalışan örnek |
| 📚 **Bilgi tabanı** | Ek yapılandırma olmadan dökümanlardan bilgi yükleme |
| 🌍 **Türkçe desteği** | Türkçe diyaloglarda doğal sonuçlar |
| 🛠️ **Araç entegrasyonu** | Gelişmiş araç sistemi ile genişletilebilir |

---

## 🧑‍🏫 Tutorial

Tamamlanmış örnekleri adım adım incelemek için [examples](examples) klasöründeki rehberleri izleyebilirsiniz. Bu dizinde hem temel kullanım senaryoları hem de ileri seviye entegrasyonlar yer alır. Öne çıkan içerikler:

- [Basic usage walkthrough](examples/basic_usage.py) – ilk hafızalı ajanın nasıl oluşturulacağını gösterir.
- [Customer support workflow](examples/customer_support.py) – çok kullanıcılı müşteri destek senaryosu.
- [Knowledge base ingestion](examples/knowledge_base.py) – dokümanlardan bilgi yükleme.

Her dosyada kodun yanında açıklamalar bulunur; komutları kopyalayıp çalıştırarak sonuçları deneyimleyebilirsiniz.

## 📖 Kullanım örnekleri

### Basic conversation
>>>>>>> f002396c8c531e4cde33d19ac6a755494b1b30cd

```python
from mem_llm import MemAgent

agent = MemAgent()
agent.set_user("alice")

# İlk konuşma
agent.chat("I love pizza")

# Later on...
agent.chat("What's my favorite food?")
# → "Your favorite food is pizza"
```

<<<<<<< HEAD
### Multi-language Support

```python
# Works with any language
=======
### Turkish language support

```python
# Handles Turkish dialogue naturally
>>>>>>> f002396c8c531e4cde33d19ac6a755494b1b30cd
agent.set_user("ahmet")
agent.chat("Benim adım Ahmet ve pizza seviyorum")
agent.chat("Adımı hatırlıyor musun?")
# → "Evet, adınız Ahmet!"
```

### Customer service scenario

```python
agent = MemAgent()

# Müşteri 1
agent.set_user("customer_001")
agent.chat("My order #12345 is delayed")

# Customer 2 (separate memory!)
agent.set_user("customer_002")
agent.chat("I want to return item #67890")
```

### Inspecting the user profile

```python
# Retrieve automatically extracted user information
profile = agent.get_user_profile()
# {'name': 'Alice', 'favorite_food': 'pizza', 'location': 'NYC'}
```

---

## 🔧 Yapılandırma seçenekleri

### JSON hafıza (varsayılan ve basit)

```python
agent = MemAgent(
    model="granite4:tiny-h",
    use_sql=False,  # JSON dosyaları ile hafıza
    memory_dir="memories"
)
```

### SQL hafıza (gelişmiş ve hızlı)

```python
agent = MemAgent(
    model="granite4:tiny-h",
    use_sql=True,  # SQLite tabanlı hafıza
    memory_dir="memories.db"
)
```

### Diğer özelleştirmeler

```python
agent = MemAgent(
    model="llama2",  # Herhangi bir Ollama modeli
    ollama_url="http://localhost:11434"
)
```

---

## 📚 API referansı

### `MemAgent`

```python
# Initialize
agent = MemAgent(model="granite4:tiny-h", use_sql=False)

# Set active user
agent.set_user(user_id: str, name: Optional[str] = None)

# Chat
response = agent.chat(message: str, metadata: Optional[Dict] = None) -> str

# Get profile
profile = agent.get_user_profile(user_id: Optional[str] = None) -> Dict

# System check
status = agent.check_setup() -> Dict
```

---

## 🗂 Bilgi tabanı ve dokümanlardan yapılandırma

Kurumsal dokümanlarınızdan otomatik `config.yaml` üretin:

```python
from mem_llm import create_config_from_document

# PDF'den config.yaml üretin
create_config_from_document(
    doc_path="company_info.pdf",
    output_path="config.yaml",
    company_name="Acme Corp"
)

# Oluşan yapılandırmayı kullanın
agent = MemAgent(config_file="config.yaml")
```

---

## 🔥 Desteklenen modeller

[Ollama](https://ollama.ai/) üzerindeki tüm modellerle çalışır. Tavsiye edilen modeller:

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| `granite4:tiny-h` | 2.5GB | ⚡⚡⚡ | ⭐⭐ |
| `llama2` | 4GB | ⚡⚡ | ⭐⭐⭐ |
| `mistral` | 4GB | ⚡⚡ | ⭐⭐⭐⭐ |
| `llama3` | 5GB | ⚡ | ⭐⭐⭐⭐⭐ |

```bash
ollama pull <model-name>
```

---

## 📦 Gereksinimler

- Python 3.8+
- Ollama (LLM için)
- Minimum 4GB RAM
- 5GB disk alanı

**Kurulum ile gelen bağımlılıklar:**
- `requests >= 2.31.0`
- `pyyaml >= 6.0.1`
- `sqlite3` (Python ile birlikte gelir)

---

## 🐛 Sık karşılaşılan problemler

### Ollama çalışmıyor mu?

```bash
ollama serve
```

### Model bulunamadı hatası mı alıyorsunuz?

```bash
ollama pull granite4:tiny-h
```

### ImportError veya bağlantı hatası mı var?

```bash
pip install --upgrade mem-llm
```

> Hâlâ sorun yaşıyorsanız `agent.check_setup()` çıktısını ve hata mesajını issue açarken paylaşın.

---

## 📄 Lisans

MIT Lisansı — kişisel veya ticari projelerinizde özgürce kullanabilirsiniz.

---

## 🔗 Faydalı bağlantılar

- **PyPI:** https://pypi.org/project/mem-llm/
- **GitHub:** https://github.com/emredeveloper/Mem-LLM
- **Ollama:** https://ollama.ai/

---

## 🌟 Bize destek olun

Proje işinize yaradıysa [GitHub](https://github.com/emredeveloper/Mem-LLM) üzerinden ⭐ vermeyi unutmayın!

---

<div align="center">
Sevgiyle geliştirildi — <a href="https://github.com/emredeveloper">C. Emre Karataş</a>
</div>
