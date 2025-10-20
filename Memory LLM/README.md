# 🧠 mem-llm# 🧠 mem-llm



**Memory-enabled AI assistant that remembers conversations using local LLMs****Memory-enabled AI assistant that remembers conversations using local LLMs**



[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

[![PyPI](https://img.shields.io/pypi/v/mem-llm?label=PyPI)](https://pypi.org/project/mem-llm/)[![PyPI](https://img.shields.io/pypi/v/mem-llm?label=PyPI)](https://pypi.org/project/mem-llm/)

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)



------



## 🎯 What is mem-llm?## 📚 İçindekiler



`mem-llm` is a lightweight Python library that adds **persistent memory** to your local LLM chatbots. Each user gets their own conversation history that persists across sessions.- [🎯 mem-llm nedir?](#-mem-llm-nedir)

- [⚡ Hızlı başlangıç](#-hızlı-başlangıç)

**Use Cases:**- [🧑‍🏫 Tutorial](#-tutorial)

- 💬 Customer service bots- [💡 Özellikler](#-özellikler)

- 🤖 Personal assistants- [📖 Kullanım örnekleri](#-kullanım-örnekleri)

- 📝 Context-aware applications- [🔧 Yapılandırma seçenekleri](#-yapılandırma-seçenekleri)

- 🏢 Business automation solutions- [🗂 Bilgi tabanı ve dokümanlardan yapılandırma](#-bilgi-tabanı-ve-dokümanlardan-yapılandırma)

- [🔥 Desteklenen modeller](#-desteklenen-modeller)

---- [📦 Gereksinimler](#-gereksinimler)

- [🐛 Sık karşılaşılan problemler](#-sık-karşılaşılan-problemler)

## ⚡ Quick Start

---

### 1. Install the package

## 🎯 mem-llm nedir?

```bash

pip install mem-llm`mem-llm`, yerel bir LLM ile çalışan sohbet botlarınıza **kalıcı hafıza** kazandıran hafif bir Python kütüphanesidir. Her kullanıcı için ayrı bir konuşma geçmişi tutulur ve yapay zeka bu geçmişi bir sonraki oturumda otomatik olarak kullanır.

```

**Nerelerde kullanılabilir?**

### 2. Start Ollama and download a model (one-time setup)- 💬 Müşteri hizmetleri botları

- 🤖 Kişisel asistanlar

```bash- 📝 Bağlama duyarlı uygulamalar

# Start Ollama service- 🏢 İş süreçlerini otomatikleştiren çözümler

ollama serve

---

# Download lightweight model (~2.5GB)

ollama pull granite4:tiny-h## ⚡ Hızlı başlangıç

```

### 0. Gereksinimleri kontrol edin

> 💡 Keep `ollama serve` running in one terminal, run your Python code in another.

- Python 3.8 veya üzeri

### 3. Create your first agent- [Ollama](https://ollama.ai/) kurulu ve çalışır durumda

- En az 4GB RAM ve 5GB disk alanı

```python

from mem_llm import MemAgent### 1. Paketi yükleyin



# Create agent in one line```bash

agent = MemAgent()pip install mem-llm==1.0.7

```

# Set user (each user gets separate memory)

agent.set_user("john")### 2. Ollama'yı başlatın ve modeli indirin (tek seferlik)



# Chat with memory!```bash

response = agent.chat("My name is John")# Ollama servisini başlatın

print(response)ollama serve



response = agent.chat("What's my name?")# Yaklaşık 2.5GB'lık hafif modeli indirin

print(response)  # Output: "Your name is John"ollama pull granite4:tiny-h

``````



### 4. Verify your setup (optional)> 💡 Ollama `serve` komutu terminalde açık kalmalıdır. Yeni bir terminal sekmesinde Python kodunu çalıştırabilirsiniz.



```bash### 3. İlk ajanınızı çalıştırın

# Using CLI

mem-llm check```python

from mem_llm import MemAgent

# Or in Python

agent.check_setup()# Tek satırda ajan oluşturun

```agent = MemAgent()



---# Kullanıcıyı belirleyin (her kullanıcı için ayrı hafıza tutulur)

agent.set_user("john")

## 💡 Features

# Sohbet edin - hafıza devrede!

| Feature | Description |agent.chat("My name is John")

|---------|-------------|agent.chat("What's my name?")  # → "Your name is John"

| 🧠 **Memory** | Remembers each user's conversation history |```

| 👥 **Multi-user** | Separate memory for each user |

| 🔒 **Privacy** | 100% local, no cloud/API needed |### 4. Kurulumunuzu doğrulayın (isteğe bağlı)

| ⚡ **Fast** | Lightweight SQLite/JSON storage |

| 🎯 **Simple** | 3 lines of code to get started |```python

| 📚 **Knowledge Base** | Load information from documents |agent.check_setup()

| 🌍 **Multi-language** | Works with any language (Turkish, English, etc.) |# {'ollama': 'running', 'model': 'granite4:tiny-h', 'memory_backend': 'sql', ...}

| 🛠️ **CLI Tool** | Built-in command-line interface |```



---<<<<<<< HEAD

| Feature | Description |

## 📖 Usage Examples|---------|-------------|

| 🧠 **Memory** | Remembers each user's conversation history |

### Example 1: Basic Conversation with Memory| 👥 **Multi-user** | Separate memory for each user |

| 🔒 **Privacy** | 100% local, no cloud/API needed |

```python| ⚡ **Fast** | Lightweight SQLite/JSON storage |

from mem_llm import MemAgent| 🎯 **Simple** | 3 lines of code to get started |

| 📚 **Knowledge Base** | Config-free document integration |

# Create agent| 🌍 **Multi-language** | Works with any language |

print("🤖 Creating AI agent...")| 🛠️ **CLI Tool** | Built-in command-line interface |

agent = MemAgent()

---

# Set user

print("👤 Setting user: alice\n")## 🔄 Memory Backend Comparison

agent.set_user("alice")

Choose the right backend for your needs:

# First conversation

print("💬 User: I love pizza")| Feature | JSON Mode | SQL Mode |

response1 = agent.chat("I love pizza")|---------|-----------|----------|

print(f"🤖 Bot: {response1}\n")| **Setup** | ✅ Zero config | ⚙️ Minimal config |

| **Conversation Memory** | ✅ Yes | ✅ Yes |

# Memory test - bot remembers!| **User Profiles** | ✅ Yes | ✅ Yes |

print("💬 User: What's my favorite food?")| **Knowledge Base** | ❌ No | ✅ Yes |

response2 = agent.chat("What's my favorite food?")| **Advanced Search** | ❌ No | ✅ Yes |

print(f"🤖 Bot: {response2}")| **Multi-user Performance** | ⭐⭐ Good | ⭐⭐⭐ Excellent |

```| **Data Queries** | ❌ Limited | ✅ Full SQL |

| **Best For** | 🏠 Personal use | 🏢 Business use |

**Output:**

```**Recommendation:**

🤖 Creating AI agent...- **JSON Mode**: Perfect for personal assistants and quick prototypes

👤 Setting user: alice- **SQL Mode**: Ideal for customer service, multi-user apps, and production

=======

💬 User: I love pizzaKurulum sırasında sorun yaşarsanız [🐛 Sık karşılaşılan problemler](#-sık-karşılaşılan-problemler) bölümüne göz atın.

🤖 Bot: That's great! Pizza is a popular choice...>>>>>>> f002396c8c531e4cde33d19ac6a755494b1b30cd



💬 User: What's my favorite food?---

🤖 Bot: Based on our conversation, your favorite food is pizza!

```## 💡 Özellikler



---<<<<<<< HEAD

### Command Line Interface (CLI)

### Example 2: Multi-User Support

The easiest way to get started:

```python

from mem_llm import MemAgent```bash

# Install with CLI support

agent = MemAgent()pip install mem-llm



# Customer 1# Start interactive chat

print("=" * 60)mem-llm chat --user john

print("👤 Customer 1: John")

print("=" * 60)# Check system status

agent.set_user("customer_john")mem-llm check



print("💬 John: My order #12345 is delayed")# View statistics

response = agent.chat("My order #12345 is delayed")mem-llm stats

print(f"🤖 Bot: {response}\n")

# Export user data

# Customer 2 - SEPARATE MEMORY!mem-llm export john --format json --output data.json

print("=" * 60)

print("👤 Customer 2: Sarah")# Get help

print("=" * 60)mem-llm --help

agent.set_user("customer_sarah")```



print("💬 Sarah: I want to return item #67890")**Available CLI Commands:**

response = agent.chat("I want to return item #67890")

print(f"🤖 Bot: {response}\n")| Command | Description | Example |

|---------|-------------|---------|

# Back to Customer 1 - remembers previous conversation!| `chat` | Interactive chat session | `mem-llm chat --user alice` |

print("=" * 60)| `check` | Verify system setup | `mem-llm check` |

print("👤 Back to Customer 1: John")| `stats` | Show statistics | `mem-llm stats --user john` |

print("=" * 60)| `export` | Export user data | `mem-llm export john` |

agent.set_user("customer_john")| `clear` | Delete user data | `mem-llm clear john` |



print("💬 John: What was my order number?")### Basic Chat

response = agent.chat("What was my order number?")=======

print(f"🤖 Bot: {response}")| Özellik | Açıklama |

```|---------|----------|

| 🧠 **Kalıcı hafıza** | Her kullanıcının sohbet geçmişi saklanır |

**Output:**| 👥 **Çoklu kullanıcı** | Her kullanıcı için ayrı hafıza yönetimi |

```| 🔒 **Gizlilik** | Tamamen yerel çalışır, buluta veri göndermez |

============================================================| ⚡ **Hızlı** | Hafif SQLite veya JSON depolama seçenekleri |

👤 Customer 1: John| 🎯 **Kolay kullanım** | Üç satırda çalışan örnek |

============================================================| 📚 **Bilgi tabanı** | Ek yapılandırma olmadan dökümanlardan bilgi yükleme |

💬 John: My order #12345 is delayed| 🌍 **Türkçe desteği** | Türkçe diyaloglarda doğal sonuçlar |

🤖 Bot: I'll help you check your order status...| 🛠️ **Araç entegrasyonu** | Gelişmiş araç sistemi ile genişletilebilir |



============================================================---

👤 Customer 2: Sarah

============================================================## 🧑‍🏫 Tutorial

💬 Sarah: I want to return item #67890

🤖 Bot: I can help you with the return process...Tamamlanmış örnekleri adım adım incelemek için [examples](examples) klasöründeki rehberleri izleyebilirsiniz. Bu dizinde hem temel kullanım senaryoları hem de ileri seviye entegrasyonlar yer alır. Öne çıkan içerikler:



============================================================- [Basic usage walkthrough](examples/basic_usage.py) – ilk hafızalı ajanın nasıl oluşturulacağını gösterir.

👤 Back to Customer 1: John- [Customer support workflow](examples/customer_support.py) – çok kullanıcılı müşteri destek senaryosu.

============================================================- [Knowledge base ingestion](examples/knowledge_base.py) – dokümanlardan bilgi yükleme.

💬 John: What was my order number?

🤖 Bot: Your order number is #12345, which you mentioned was delayed.Her dosyada kodun yanında açıklamalar bulunur; komutları kopyalayıp çalıştırarak sonuçları deneyimleyebilirsiniz.

```

## 📖 Kullanım örnekleri

---

### Basic conversation

### Example 3: Turkish Language Support>>>>>>> f002396c8c531e4cde33d19ac6a755494b1b30cd



```python```python

from mem_llm import MemAgentfrom mem_llm import MemAgent



agent = MemAgent()agent = MemAgent()

agent.set_user("alice")

print("🇹🇷 Türkçe Konuşma Örneği")

print("=" * 60)# İlk konuşma

agent.chat("I love pizza")

agent.set_user("ahmet")

# Later on...

print("💬 Kullanıcı: Benim adım Ahmet ve İstanbul'da yaşıyorum")agent.chat("What's my favorite food?")

response = agent.chat("Benim adım Ahmet ve İstanbul'da yaşıyorum")# → "Your favorite food is pizza"

print(f"🤖 Bot: {response}\n")```



print("💬 Kullanıcı: Nerede yaşıyorum?")<<<<<<< HEAD

response = agent.chat("Nerede yaşıyorum?")### Multi-language Support

print(f"🤖 Bot: {response}\n")

```python

print("💬 Kullanıcı: Adımı hatırlıyor musun?")# Works with any language

response = agent.chat("Adımı hatırlıyor musun?")=======

print(f"🤖 Bot: {response}")### Turkish language support

```

```python

**Output:**# Handles Turkish dialogue naturally

```>>>>>>> f002396c8c531e4cde33d19ac6a755494b1b30cd

🇹🇷 Türkçe Konuşma Örneğiagent.set_user("ahmet")

============================================================agent.chat("Benim adım Ahmet ve pizza seviyorum")

💬 Kullanıcı: Benim adım Ahmet ve İstanbul'da yaşıyorumagent.chat("Adımı hatırlıyor musun?")

🤖 Bot: Memnun oldum Ahmet! İstanbul güzel bir şehir...# → "Evet, adınız Ahmet!"

```

💬 Kullanıcı: Nerede yaşıyorum?

🤖 Bot: İstanbul'da yaşıyorsunuz.### Customer service scenario



💬 Kullanıcı: Adımı hatırlıyor musun?```python

🤖 Bot: Evet, adınız Ahmet!agent = MemAgent()

```

# Müşteri 1

---agent.set_user("customer_001")

agent.chat("My order #12345 is delayed")

### Example 4: User Profile Extraction

# Customer 2 (separate memory!)

```pythonagent.set_user("customer_002")

from mem_llm import MemAgentagent.chat("I want to return item #67890")

```

agent = MemAgent()

agent.set_user("alice")### Inspecting the user profile



print("📝 Building user profile...")```python

print("=" * 60)# Retrieve automatically extracted user information

profile = agent.get_user_profile()

# Have natural conversations# {'name': 'Alice', 'favorite_food': 'pizza', 'location': 'NYC'}

conversations = [```

    "My name is Alice and I'm 28 years old",

    "I live in New York City",---

    "I work as a software engineer",

    "My favorite food is pizza"## 🔧 Yapılandırma seçenekleri

]

### JSON hafıza (varsayılan ve basit)

for msg in conversations:

    print(f"💬 User: {msg}")```python

    response = agent.chat(msg)agent = MemAgent(

    print(f"🤖 Bot: {response}\n")    model="granite4:tiny-h",

    use_sql=False,  # JSON dosyaları ile hafıza

# Extract profile automatically    memory_dir="memories"

print("=" * 60))

print("📊 Extracted User Profile:")```

print("=" * 60)

profile = agent.get_user_profile()### SQL hafıza (gelişmiş ve hızlı)



for key, value in profile.items():```python

    print(f"   {key}: {value}")agent = MemAgent(

```    model="granite4:tiny-h",

    use_sql=True,  # SQLite tabanlı hafıza

**Output:**    memory_dir="memories.db"

```)

📝 Building user profile...```

============================================================

💬 User: My name is Alice and I'm 28 years old### Diğer özelleştirmeler

🤖 Bot: Nice to meet you, Alice!...

```python

💬 User: I live in New York Cityagent = MemAgent(

🤖 Bot: New York City is a vibrant place...    model="llama2",  # Herhangi bir Ollama modeli

    ollama_url="http://localhost:11434"

💬 User: I work as a software engineer)

🤖 Bot: That's an interesting career...```



💬 User: My favorite food is pizza---

🤖 Bot: Pizza is delicious!...

## 📚 API referansı

============================================================

📊 Extracted User Profile:### `MemAgent`

============================================================

   name: Alice```python

   age: 28# Initialize

   location: New York Cityagent = MemAgent(model="granite4:tiny-h", use_sql=False)

   occupation: Software Engineer

   favorite_food: Pizza# Set active user

```agent.set_user(user_id: str, name: Optional[str] = None)



---# Chat

response = agent.chat(message: str, metadata: Optional[Dict] = None) -> str

### Example 5: Complete Customer Service Workflow

# Get profile

```pythonprofile = agent.get_user_profile(user_id: Optional[str] = None) -> Dict

from mem_llm import MemAgent

# System check

# Initialize customer service agentstatus = agent.check_setup() -> Dict

print("🏢 Customer Service Bot Initializing...")```

agent = MemAgent(use_sql=True)  # SQL for better performance

---

# Simulate customer support session

def handle_customer(customer_id, customer_name):## 🗂 Bilgi tabanı ve dokümanlardan yapılandırma

    print("\n" + "=" * 70)

    print(f"📞 New Customer Session: {customer_name} (ID: {customer_id})")Kurumsal dokümanlarınızdan otomatik `config.yaml` üretin:

    print("=" * 70)

    ```python

    agent.set_user(customer_id, name=customer_name)from mem_llm import create_config_from_document

    

    # Customer introduces issue# PDF'den config.yaml üretin

    print(f"\n💬 {customer_name}: Hi, my order hasn't arrived yet")create_config_from_document(

    response = agent.chat("Hi, my order hasn't arrived yet")    doc_path="company_info.pdf",

    print(f"🤖 Support: {response}")    output_path="config.yaml",

        company_name="Acme Corp"

    # Ask for details)

    print(f"\n💬 {customer_name}: My order number is #45678")

    response = agent.chat("My order number is #45678")# Oluşan yapılandırmayı kullanın

    print(f"🤖 Support: {response}")agent = MemAgent(config_file="config.yaml")

    ```

    # Follow up later in conversation

    print(f"\n💬 {customer_name}: Can you remind me what we were discussing?")---

    response = agent.chat("Can you remind me what we were discussing?")

    print(f"🤖 Support: {response}")## 🔥 Desteklenen modeller



# Handle multiple customers[Ollama](https://ollama.ai/) üzerindeki tüm modellerle çalışır. Tavsiye edilen modeller:

handle_customer("cust_001", "Emma")

handle_customer("cust_002", "Michael")| Model | Size | Speed | Quality |

|-------|------|-------|---------|

# Return to first customer - memory persists!| `granite4:tiny-h` | 2.5GB | ⚡⚡⚡ | ⭐⭐ |

print("\n" + "=" * 70)| `llama2` | 4GB | ⚡⚡ | ⭐⭐⭐ |

print("📞 Returning Customer: Emma (ID: cust_001)")| `mistral` | 4GB | ⚡⚡ | ⭐⭐⭐⭐ |

print("=" * 70)| `llama3` | 5GB | ⚡ | ⭐⭐⭐⭐⭐ |

agent.set_user("cust_001")

```bash

print("\n💬 Emma: What was my order number again?")ollama pull <model-name>

response = agent.chat("What was my order number again?")```

print(f"🤖 Support: {response}")

# Output: "Your order number is #45678"---

```

## 📦 Gereksinimler

**Output:**

```- Python 3.8+

🏢 Customer Service Bot Initializing...- Ollama (LLM için)

- Minimum 4GB RAM

======================================================================- 5GB disk alanı

📞 New Customer Session: Emma (ID: cust_001)

======================================================================**Kurulum ile gelen bağımlılıklar:**

- `requests >= 2.31.0`

💬 Emma: Hi, my order hasn't arrived yet- `pyyaml >= 6.0.1`

🤖 Support: I'm sorry to hear that. I'll help you track your order...- `sqlite3` (Python ile birlikte gelir)



💬 Emma: My order number is #45678---

🤖 Support: Thank you for providing order #45678. Let me check...

## 🐛 Sık karşılaşılan problemler

💬 Emma: Can you remind me what we were discussing?

🤖 Support: We're discussing your order #45678 that hasn't arrived yet...### Ollama çalışmıyor mu?



======================================================================```bash

📞 New Customer Session: Michael (ID: cust_002)ollama serve

======================================================================```



💬 Michael: Hi, my order hasn't arrived yet### Model bulunamadı hatası mı alıyorsunuz?

🤖 Support: I'm sorry to hear that. I'll help you track your order...

```bash

💬 Michael: My order number is #78901ollama pull granite4:tiny-h

🤖 Support: Thank you for providing order #78901...```



======================================================================### ImportError veya bağlantı hatası mı var?

📞 Returning Customer: Emma (ID: cust_001)

======================================================================```bash

pip install --upgrade mem-llm

💬 Emma: What was my order number again?```

🤖 Support: Your order number is #45678.

```> Hâlâ sorun yaşıyorsanız `agent.check_setup()` çıktısını ve hata mesajını issue açarken paylaşın.



------



## 🔧 Configuration Options## 📄 Lisans



### JSON Memory (Simple, Default)MIT Lisansı — kişisel veya ticari projelerinizde özgürce kullanabilirsiniz.



```python---

agent = MemAgent(

    model="granite4:tiny-h",## 🔗 Faydalı bağlantılar

    use_sql=False,  # JSON file-based memory

    memory_dir="memories"- **PyPI:** https://pypi.org/project/mem-llm/

)- **GitHub:** https://github.com/emredeveloper/Mem-LLM

```- **Ollama:** https://ollama.ai/



### SQL Memory (Advanced, Recommended for Production)---



```python## 🌟 Bize destek olun

agent = MemAgent(

    model="granite4:tiny-h",Proje işinize yaradıysa [GitHub](https://github.com/emredeveloper/Mem-LLM) üzerinden ⭐ vermeyi unutmayın!

    use_sql=True,  # SQLite-based memory

    memory_dir="memories.db"---

)

```<div align="center">

Sevgiyle geliştirildi — <a href="https://github.com/emredeveloper">C. Emre Karataş</a>

### Custom Configuration</div>


```python
agent = MemAgent(
    model="llama2",  # Any Ollama model
    ollama_url="http://localhost:11434",
    check_connection=True  # Verify setup on startup
)
```

---

## 🛠️ Command Line Interface

```bash
# Start interactive chat
mem-llm chat --user john

# Check system status
mem-llm check

# View statistics
mem-llm stats

# Export user data
mem-llm export john --format json

# Clear user data
mem-llm clear john

# Get help
mem-llm --help
```

---

## 🔄 Memory Backend Comparison

| Feature | JSON Mode | SQL Mode |
|---------|-----------|----------|
| **Setup** | ✅ Zero config | ⚙️ Minimal config |
| **Conversation Memory** | ✅ Yes | ✅ Yes |
| **User Profiles** | ✅ Yes | ✅ Yes |
| **Knowledge Base** | ❌ No | ✅ Yes |
| **Advanced Search** | ❌ No | ✅ Yes |
| **Multi-user Performance** | ⭐⭐ Good | ⭐⭐⭐ Excellent |
| **Best For** | 🏠 Personal use | 🏢 Business use |

**Recommendation:**
- **JSON Mode**: Perfect for personal assistants and quick prototypes
- **SQL Mode**: Ideal for customer service, multi-user apps, and production

---

## 📚 API Reference

### MemAgent Class

```python
# Initialize
agent = MemAgent(
    model="granite4:tiny-h",
    use_sql=True,
    memory_dir=None,
    ollama_url="http://localhost:11434",
    check_connection=False
)

# Set active user
agent.set_user(user_id: str, name: Optional[str] = None)

# Chat (returns response string)
response = agent.chat(message: str, metadata: Optional[Dict] = None) -> str

# Get user profile (auto-extracted from conversations)
profile = agent.get_user_profile(user_id: Optional[str] = None) -> Dict

# System check
status = agent.check_setup() -> Dict
```

---

## 🔥 Supported Models

Works with any [Ollama](https://ollama.ai/) model. Recommended models:

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `granite4:tiny-h` | 2.5GB | ⚡⚡⚡ | ⭐⭐ | Quick testing |
| `llama2` | 4GB | ⚡⚡ | ⭐⭐⭐ | General use |
| `mistral` | 4GB | ⚡⚡ | ⭐⭐⭐⭐ | Balanced |
| `llama3` | 5GB | ⚡ | ⭐⭐⭐⭐⭐ | Best quality |

```bash
# Download a model
ollama pull <model-name>

# List installed models
ollama list
```

---

## 📦 Requirements

- Python 3.8+
- [Ollama](https://ollama.ai/) (for LLM)
- Minimum 4GB RAM
- 5GB disk space

**Python Dependencies (auto-installed):**
- `requests >= 2.31.0`
- `pyyaml >= 6.0.1`
- `click >= 8.1.0`

---

## 🐛 Troubleshooting

### Ollama not running?

```bash
ollama serve
```

### Model not found error?

```bash
# Download the model
ollama pull granite4:tiny-h

# Check installed models
ollama list
```

### Connection error?

```bash
# Check if Ollama is running
curl http://localhost:11434

# Restart Ollama
ollama serve
```

### Import error?

```bash
# Upgrade to latest version
pip install --upgrade mem-llm
```

> If issues persist, run `mem-llm check` or `agent.check_setup()` and share the output when opening an issue.

---

## 📄 License

MIT License - Free to use in personal and commercial projects.

---

## 🔗 Links

- **PyPI:** https://pypi.org/project/mem-llm/
- **GitHub:** https://github.com/emredeveloper/Mem-LLM
- **Ollama:** https://ollama.ai/
- **Documentation:** [GitHub Wiki](https://github.com/emredeveloper/Mem-LLM/wiki)

---

## 🌟 Support Us

If you find this project useful, please ⭐ [star it on GitHub](https://github.com/emredeveloper/Mem-LLM)!

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

<div align="center">
Made with ❤️ by <a href="https://github.com/emredeveloper">C. Emre Karataş</a>
</div>
