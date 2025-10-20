# 🧠 mem-llm# 🧠 mem-llm# 🧠 mem-llm# 🧠 mem-llm



**Memory-enabled AI assistant that remembers conversations using local LLMs**



[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)**Memory-enabled AI assistant that remembers conversations using local LLMs**

[![PyPI](https://img.shields.io/pypi/v/mem-llm?label=PyPI)](https://pypi.org/project/mem-llm/)

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)



---[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)**Memory-enabled AI assistant that remembers conversations using local LLMs****Memory-enabled AI assistant that remembers conversations using local LLMs**



## 🎯 What is mem-llm?[![PyPI](https://img.shields.io/pypi/v/mem-llm?label=PyPI)](https://pypi.org/project/mem-llm/)



`mem-llm` is a lightweight Python library that adds **persistent memory** to your local LLM chatbots. Each user gets their own conversation history that persists across sessions.[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)



**Use Cases:**

- 💬 Customer service bots

- 🤖 Personal assistants---[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

- 📝 Context-aware applications

- 🏢 Business automation solutions



---## 🎯 What is mem-llm?[![PyPI](https://img.shields.io/pypi/v/mem-llm?label=PyPI)](https://pypi.org/project/mem-llm/)[![PyPI](https://img.shields.io/pypi/v/mem-llm?label=PyPI)](https://pypi.org/project/mem-llm/)



## ⚡ Quick Start



### 1. Install the package`mem-llm` is a lightweight Python library that adds **persistent memory** to your local LLM chatbots. Each user gets their own conversation history that persists across sessions.[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)



```bash

pip install mem-llm

```**Use Cases:**



### 2. Start Ollama and download a model (one-time setup)- 💬 Customer service bots



```bash- 🤖 Personal assistants------

# Start Ollama service

ollama serve- 📝 Context-aware applications



# Download lightweight model (~2.5GB)- 🏢 Business automation solutions

ollama pull granite4:tiny-h

```



> 💡 Keep `ollama serve` running in one terminal, run your Python code in another.---## 🎯 What is mem-llm?## 📚 İçindekiler



### 3. Create your first agent



```python## ⚡ Quick Start

from mem_llm import MemAgent



# Create agent in one line

agent = MemAgent()### 1. Install the package`mem-llm` is a lightweight Python library that adds **persistent memory** to your local LLM chatbots. Each user gets their own conversation history that persists across sessions.- [🎯 mem-llm nedir?](#-mem-llm-nedir)



# Set user (each user gets separate memory)

agent.set_user("john")

```bash- [⚡ Hızlı başlangıç](#-hızlı-başlangıç)

# Chat with memory!

response = agent.chat("My name is John")pip install mem-llm

print(response)

```**Use Cases:**- [🧑‍🏫 Tutorial](#-tutorial)

response = agent.chat("What's my name?")

print(response)  # Output: "Your name is John"

```

### 2. Start Ollama and download a model (one-time setup)- 💬 Customer service bots- [💡 Özellikler](#-özellikler)

### 4. Verify your setup (optional)



```bash

# Using CLI```bash- 🤖 Personal assistants- [📖 Kullanım örnekleri](#-kullanım-örnekleri)

mem-llm check

# Start Ollama service

# Or in Python

agent.check_setup()ollama serve- 📝 Context-aware applications- [🔧 Yapılandırma seçenekleri](#-yapılandırma-seçenekleri)

```



---

# Download lightweight model (~2.5GB)- 🏢 Business automation solutions- [🗂 Bilgi tabanı ve dokümanlardan yapılandırma](#-bilgi-tabanı-ve-dokümanlardan-yapılandırma)

## 💡 Features

ollama pull granite4:tiny-h

| Feature | Description |

|---------|-------------|```- [🔥 Desteklenen modeller](#-desteklenen-modeller)

| 🧠 **Memory** | Remembers each user's conversation history |

| 👥 **Multi-user** | Separate memory for each user |

| 🔒 **Privacy** | 100% local, no cloud/API needed |

| ⚡ **Fast** | Lightweight SQLite/JSON storage |> 💡 Keep `ollama serve` running in one terminal, run your Python code in another.---- [📦 Gereksinimler](#-gereksinimler)

| 🎯 **Simple** | 3 lines of code to get started |

| 📚 **Knowledge Base** | Config-free document integration |

| 🌍 **Multi-language** | Works with any language |

| 🛠️ **CLI Tool** | Built-in command-line interface |### 3. Create your first agent- [🐛 Sık karşılaşılan problemler](#-sık-karşılaşılan-problemler)



---



## 🔄 Memory Backend Comparison```python## ⚡ Quick Start



Choose the right backend for your needs:from mem_llm import MemAgent



| Feature | JSON Mode | SQL Mode |---

|---------|-----------|----------|

| **Setup** | ✅ Zero config | ⚙️ Minimal config |# Create agent in one line

| **Conversation Memory** | ✅ Yes | ✅ Yes |

| **User Profiles** | ✅ Yes | ✅ Yes |agent = MemAgent()### 1. Install the package

| **Knowledge Base** | ❌ No | ✅ Yes |

| **Advanced Search** | ❌ No | ✅ Yes |

| **Multi-user Performance** | ⭐⭐ Good | ⭐⭐⭐ Excellent |

| **Data Queries** | ❌ Limited | ✅ Full SQL |# Set user (each user gets separate memory)## 🎯 mem-llm nedir?

| **Best For** | 🏠 Personal use | 🏢 Business use |

agent.set_user("john")

**Recommendation:**

- **JSON Mode**: Perfect for personal assistants and quick prototypes```bash

- **SQL Mode**: Ideal for customer service, multi-user apps, and production

# Chat with memory!

---

response = agent.chat("My name is John")pip install mem-llm`mem-llm`, yerel bir LLM ile çalışan sohbet botlarınıza **kalıcı hafıza** kazandıran hafif bir Python kütüphanesidir. Her kullanıcı için ayrı bir konuşma geçmişi tutulur ve yapay zeka bu geçmişi bir sonraki oturumda otomatik olarak kullanır.

## 📖 Usage Examples

print(response)

### Example 1: Basic Conversation with Memory

```

```python

from mem_llm import MemAgentresponse = agent.chat("What's my name?")



# Create agentprint(response)  # Output: "Your name is John"**Nerelerde kullanılabilir?**

agent = MemAgent()

agent.set_user("alice")```



# First conversation### 2. Start Ollama and download a model (one-time setup)- 💬 Müşteri hizmetleri botları

response1 = agent.chat("I love pizza")

print(response1)### 4. Verify your setup (optional)



# Memory test - bot remembers!- 🤖 Kişisel asistanlar

response2 = agent.chat("What's my favorite food?")

print(response2)  # Output: "Your favorite food is pizza!"```bash

```

# Using CLI```bash- 📝 Bağlama duyarlı uygulamalar

### Example 2: Multi-User Support

mem-llm check

```python

from mem_llm import MemAgent# Start Ollama service- 🏢 İş süreçlerini otomatikleştiren çözümler



agent = MemAgent()# Or in Python



# Customer 1agent.check_setup()ollama serve

agent.set_user("customer_john")

agent.chat("My order #12345 is delayed")```



# Customer 2 - SEPARATE MEMORY!---

agent.set_user("customer_sarah")

agent.chat("I want to return item #67890")---



# Back to Customer 1 - remembers previous conversation!# Download lightweight model (~2.5GB)

agent.set_user("customer_john")

response = agent.chat("What was my order number?")## 💡 Features

print(response)  # Output: "Your order number is #12345"

```ollama pull granite4:tiny-h## ⚡ Hızlı başlangıç



### Example 3: Multi-language Support| Feature | Description |



```python|---------|-------------|```

from mem_llm import MemAgent

| 🧠 **Memory** | Remembers each user's conversation history |

agent = MemAgent()

agent.set_user("ahmet")| 👥 **Multi-user** | Separate memory for each user |### 0. Gereksinimleri kontrol edin



# Turkish conversation| 🔒 **Privacy** | 100% local, no cloud/API needed |

agent.chat("Benim adım Ahmet ve İstanbul'da yaşıyorum")

agent.chat("Nerede yaşıyorum?")  # → "İstanbul'da yaşıyorsunuz"| ⚡ **Fast** | Lightweight SQLite/JSON storage |> 💡 Keep `ollama serve` running in one terminal, run your Python code in another.

agent.chat("Adımı hatırlıyor musun?")  # → "Evet, adınız Ahmet!"

```| 🎯 **Simple** | 3 lines of code to get started |



### Example 4: User Profile Extraction| 📚 **Knowledge Base** | Config-free document integration |- Python 3.8 veya üzeri



```python| 🌍 **Multi-language** | Works with any language |

from mem_llm import MemAgent

| 🛠️ **CLI Tool** | Built-in command-line interface |### 3. Create your first agent- [Ollama](https://ollama.ai/) kurulu ve çalışır durumda

agent = MemAgent()

agent.set_user("alice")



# Have natural conversations---- En az 4GB RAM ve 5GB disk alanı

agent.chat("My name is Alice and I'm 28 years old")

agent.chat("I live in New York City")

agent.chat("I work as a software engineer")

agent.chat("My favorite food is pizza")## 🔄 Memory Backend Comparison```python



# Extract profile automatically

profile = agent.get_user_profile()

print(profile)Choose the right backend for your needs:from mem_llm import MemAgent### 1. Paketi yükleyin

# Output: {'name': 'Alice', 'age': 28, 'location': 'NYC', ...}

```



---| Feature | JSON Mode | SQL Mode |



## 🔧 Configuration Options|---------|-----------|----------|



### JSON Memory (Simple, Default)| **Setup** | ✅ Zero config | ⚙️ Minimal config |# Create agent in one line```bash



```python| **Conversation Memory** | ✅ Yes | ✅ Yes |

agent = MemAgent(

    model="granite4:tiny-h",| **User Profiles** | ✅ Yes | ✅ Yes |agent = MemAgent()pip install mem-llm==1.0.7

    use_sql=False,  # JSON file-based memory

    memory_dir="memories"| **Knowledge Base** | ❌ No | ✅ Yes |

)

```| **Advanced Search** | ❌ No | ✅ Yes |```



### SQL Memory (Advanced, Recommended for Production)| **Multi-user Performance** | ⭐⭐ Good | ⭐⭐⭐ Excellent |



```python| **Data Queries** | ❌ Limited | ✅ Full SQL |# Set user (each user gets separate memory)

agent = MemAgent(

    model="granite4:tiny-h",| **Best For** | 🏠 Personal use | 🏢 Business use |

    use_sql=True,  # SQLite-based memory

    memory_dir="memories.db"agent.set_user("john")### 2. Ollama'yı başlatın ve modeli indirin (tek seferlik)

)

```**Recommendation:**



### Custom Configuration- **JSON Mode**: Perfect for personal assistants and quick prototypes



```python- **SQL Mode**: Ideal for customer service, multi-user apps, and production

agent = MemAgent(

    model="llama2",  # Any Ollama model# Chat with memory!```bash

    ollama_url="http://localhost:11434",

    check_connection=True  # Verify setup on startup---

)

```response = agent.chat("My name is John")# Ollama servisini başlatın



---## 📖 Usage Examples



## 🛠️ Command Line Interfaceprint(response)ollama serve



```bash### Example 1: Basic Conversation with Memory

# Start interactive chat

mem-llm chat --user john



# Check system status```python

mem-llm check

from mem_llm import MemAgentresponse = agent.chat("What's my name?")# Yaklaşık 2.5GB'lık hafif modeli indirin

# View statistics

mem-llm stats



# Export user data# Create agentprint(response)  # Output: "Your name is John"ollama pull granite4:tiny-h

mem-llm export john --format json

agent = MemAgent()

# Clear user data

mem-llm clear johnagent.set_user("alice")``````



# Get help

mem-llm --help

```# First conversation



**Available CLI Commands:**response1 = agent.chat("I love pizza")



| Command | Description | Example |print(response1)### 4. Verify your setup (optional)> 💡 Ollama `serve` komutu terminalde açık kalmalıdır. Yeni bir terminal sekmesinde Python kodunu çalıştırabilirsiniz.

|---------|-------------|---------|

| `chat` | Interactive chat session | `mem-llm chat --user alice` |

| `check` | Verify system setup | `mem-llm check` |

| `stats` | Show statistics | `mem-llm stats --user john` |# Memory test - bot remembers!

| `export` | Export user data | `mem-llm export john` |

| `clear` | Delete user data | `mem-llm clear john` |response2 = agent.chat("What's my favorite food?")



---print(response2)  # Output: "Your favorite food is pizza!"```bash### 3. İlk ajanınızı çalıştırın



## 📚 API Reference```



### MemAgent Class# Using CLI



```python### Example 2: Multi-User Support

# Initialize

agent = MemAgent(mem-llm check```python

    model="granite4:tiny-h",

    use_sql=True,```python

    memory_dir=None,

    ollama_url="http://localhost:11434",from mem_llm import MemAgentfrom mem_llm import MemAgent

    check_connection=False

)



# Set active useragent = MemAgent()# Or in Python

agent.set_user(user_id: str, name: Optional[str] = None)



# Chat (returns response string)

response = agent.chat(message: str, metadata: Optional[Dict] = None) -> str# Customer 1agent.check_setup()# Tek satırda ajan oluşturun



# Get user profile (auto-extracted from conversations)agent.set_user("customer_john")

profile = agent.get_user_profile(user_id: Optional[str] = None) -> Dict

agent.chat("My order #12345 is delayed")```agent = MemAgent()

# System check

status = agent.check_setup() -> Dict

```

# Customer 2 - SEPARATE MEMORY!

---

agent.set_user("customer_sarah")

## 🔥 Supported Models

agent.chat("I want to return item #67890")---# Kullanıcıyı belirleyin (her kullanıcı için ayrı hafıza tutulur)

Works with any [Ollama](https://ollama.ai/) model. Recommended models:



| Model | Size | Speed | Quality | Best For |

|-------|------|-------|---------|----------|# Back to Customer 1 - remembers previous conversation!agent.set_user("john")

| `granite4:tiny-h` | 2.5GB | ⚡⚡⚡ | ⭐⭐ | Quick testing |

| `llama2` | 4GB | ⚡⚡ | ⭐⭐⭐ | General use |agent.set_user("customer_john")

| `mistral` | 4GB | ⚡⚡ | ⭐⭐⭐⭐ | Balanced |

| `llama3` | 5GB | ⚡ | ⭐⭐⭐⭐⭐ | Best quality |response = agent.chat("What was my order number?")## 💡 Features



```bashprint(response)  # Output: "Your order number is #12345"

# Download a model

ollama pull <model-name>```# Sohbet edin - hafıza devrede!



# List installed models

ollama list

```### Example 3: Multi-language Support| Feature | Description |agent.chat("My name is John")



---



## 📦 Requirements```python|---------|-------------|agent.chat("What's my name?")  # → "Your name is John"



- Python 3.8+from mem_llm import MemAgent

- [Ollama](https://ollama.ai/) (for LLM)

- Minimum 4GB RAM| 🧠 **Memory** | Remembers each user's conversation history |```

- 5GB disk space

agent = MemAgent()

**Python Dependencies (auto-installed):**

- `requests >= 2.31.0`agent.set_user("ahmet")| 👥 **Multi-user** | Separate memory for each user |

- `pyyaml >= 6.0.1`

- `click >= 8.1.0`



---# Turkish conversation| 🔒 **Privacy** | 100% local, no cloud/API needed |### 4. Kurulumunuzu doğrulayın (isteğe bağlı)



## 🐛 Troubleshootingagent.chat("Benim adım Ahmet ve İstanbul'da yaşıyorum")



### Ollama not running?agent.chat("Nerede yaşıyorum?")  # → "İstanbul'da yaşıyorsunuz"| ⚡ **Fast** | Lightweight SQLite/JSON storage |



```bashagent.chat("Adımı hatırlıyor musun?")  # → "Evet, adınız Ahmet!"

ollama serve

``````| 🎯 **Simple** | 3 lines of code to get started |```python



### Model not found error?



```bash### Example 4: User Profile Extraction| 📚 **Knowledge Base** | Load information from documents |agent.check_setup()

# Download the model

ollama pull granite4:tiny-h



# Check installed models```python| 🌍 **Multi-language** | Works with any language (Turkish, English, etc.) |# {'ollama': 'running', 'model': 'granite4:tiny-h', 'memory_backend': 'sql', ...}

ollama list

```from mem_llm import MemAgent



### Connection error?| 🛠️ **CLI Tool** | Built-in command-line interface |```



```bashagent = MemAgent()

# Check if Ollama is running

curl http://localhost:11434agent.set_user("alice")



# Restart Ollama

ollama serve

```# Have natural conversations---<<<<<<< HEAD



### Import error?agent.chat("My name is Alice and I'm 28 years old")



```bashagent.chat("I live in New York City")| Feature | Description |

# Upgrade to latest version

pip install --upgrade mem-llmagent.chat("I work as a software engineer")

```

agent.chat("My favorite food is pizza")## 📖 Usage Examples|---------|-------------|

> If issues persist, run `mem-llm check` or `agent.check_setup()` and share the output when opening an issue.



---

# Extract profile automatically| 🧠 **Memory** | Remembers each user's conversation history |

## 📄 License

profile = agent.get_user_profile()

MIT License - Free to use in personal and commercial projects.

print(profile)### Example 1: Basic Conversation with Memory| 👥 **Multi-user** | Separate memory for each user |

---

# Output: {'name': 'Alice', 'age': 28, 'location': 'NYC', ...}

## 🔗 Links

```| 🔒 **Privacy** | 100% local, no cloud/API needed |

- **PyPI:** https://pypi.org/project/mem-llm/

- **GitHub:** https://github.com/emredeveloper/Mem-LLM

- **Ollama:** https://ollama.ai/

- **Documentation:** [GitHub Wiki](https://github.com/emredeveloper/Mem-LLM/wiki)---```python| ⚡ **Fast** | Lightweight SQLite/JSON storage |



---



## 🌟 Support Us## 🔧 Configuration Optionsfrom mem_llm import MemAgent| 🎯 **Simple** | 3 lines of code to get started |



If you find this project useful, please ⭐ [star it on GitHub](https://github.com/emredeveloper/Mem-LLM)!



---### JSON Memory (Simple, Default)| 📚 **Knowledge Base** | Config-free document integration |



## 🤝 Contributing



Contributions are welcome! Please feel free to submit a Pull Request.```python# Create agent| 🌍 **Multi-language** | Works with any language |



1. Fork the repositoryagent = MemAgent(

2. Create your feature branch (`git checkout -b feature/AmazingFeature`)

3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)    model="granite4:tiny-h",print("🤖 Creating AI agent...")| 🛠️ **CLI Tool** | Built-in command-line interface |

4. Push to the branch (`git push origin feature/AmazingFeature`)

5. Open a Pull Request    use_sql=False,  # JSON file-based memory



---    memory_dir="memories"agent = MemAgent()



<div align="center">)

Made with ❤️ by <a href="https://github.com/emredeveloper">C. Emre Karataş</a>

</div>```---




### SQL Memory (Advanced, Recommended for Production)# Set user



```pythonprint("👤 Setting user: alice\n")## 🔄 Memory Backend Comparison

agent = MemAgent(

    model="granite4:tiny-h",agent.set_user("alice")

    use_sql=True,  # SQLite-based memory

    memory_dir="memories.db"Choose the right backend for your needs:

)

```# First conversation



### Custom Configurationprint("💬 User: I love pizza")| Feature | JSON Mode | SQL Mode |



```pythonresponse1 = agent.chat("I love pizza")|---------|-----------|----------|

agent = MemAgent(

    model="llama2",  # Any Ollama modelprint(f"🤖 Bot: {response1}\n")| **Setup** | ✅ Zero config | ⚙️ Minimal config |

    ollama_url="http://localhost:11434",

    check_connection=True  # Verify setup on startup| **Conversation Memory** | ✅ Yes | ✅ Yes |

)

```# Memory test - bot remembers!| **User Profiles** | ✅ Yes | ✅ Yes |



---print("💬 User: What's my favorite food?")| **Knowledge Base** | ❌ No | ✅ Yes |



## 🛠️ Command Line Interfaceresponse2 = agent.chat("What's my favorite food?")| **Advanced Search** | ❌ No | ✅ Yes |



```bashprint(f"🤖 Bot: {response2}")| **Multi-user Performance** | ⭐⭐ Good | ⭐⭐⭐ Excellent |

# Start interactive chat

mem-llm chat --user john```| **Data Queries** | ❌ Limited | ✅ Full SQL |



# Check system status| **Best For** | 🏠 Personal use | 🏢 Business use |

mem-llm check

**Output:**

# View statistics

mem-llm stats```**Recommendation:**



# Export user data🤖 Creating AI agent...- **JSON Mode**: Perfect for personal assistants and quick prototypes

mem-llm export john --format json

👤 Setting user: alice- **SQL Mode**: Ideal for customer service, multi-user apps, and production

# Clear user data

mem-llm clear john=======



# Get help💬 User: I love pizzaKurulum sırasında sorun yaşarsanız [🐛 Sık karşılaşılan problemler](#-sık-karşılaşılan-problemler) bölümüne göz atın.

mem-llm --help

```🤖 Bot: That's great! Pizza is a popular choice...>>>>>>> f002396c8c531e4cde33d19ac6a755494b1b30cd



**Available CLI Commands:**



| Command | Description | Example |💬 User: What's my favorite food?---

|---------|-------------|---------|

| `chat` | Interactive chat session | `mem-llm chat --user alice` |🤖 Bot: Based on our conversation, your favorite food is pizza!

| `check` | Verify system setup | `mem-llm check` |

| `stats` | Show statistics | `mem-llm stats --user john` |```## 💡 Özellikler

| `export` | Export user data | `mem-llm export john` |

| `clear` | Delete user data | `mem-llm clear john` |



------<<<<<<< HEAD



## 📚 API Reference### Command Line Interface (CLI)



### MemAgent Class### Example 2: Multi-User Support



```pythonThe easiest way to get started:

# Initialize

agent = MemAgent(```python

    model="granite4:tiny-h",

    use_sql=True,from mem_llm import MemAgent```bash

    memory_dir=None,

    ollama_url="http://localhost:11434",# Install with CLI support

    check_connection=False

)agent = MemAgent()pip install mem-llm



# Set active user

agent.set_user(user_id: str, name: Optional[str] = None)

# Customer 1# Start interactive chat

# Chat (returns response string)

response = agent.chat(message: str, metadata: Optional[Dict] = None) -> strprint("=" * 60)mem-llm chat --user john



# Get user profile (auto-extracted from conversations)print("👤 Customer 1: John")

profile = agent.get_user_profile(user_id: Optional[str] = None) -> Dict

print("=" * 60)# Check system status

# System check

status = agent.check_setup() -> Dictagent.set_user("customer_john")mem-llm check

```



---

print("💬 John: My order #12345 is delayed")# View statistics

## 🔥 Supported Models

response = agent.chat("My order #12345 is delayed")mem-llm stats

Works with any [Ollama](https://ollama.ai/) model. Recommended models:

print(f"🤖 Bot: {response}\n")

| Model | Size | Speed | Quality | Best For |

|-------|------|-------|---------|----------|# Export user data

| `granite4:tiny-h` | 2.5GB | ⚡⚡⚡ | ⭐⭐ | Quick testing |

| `llama2` | 4GB | ⚡⚡ | ⭐⭐⭐ | General use |# Customer 2 - SEPARATE MEMORY!mem-llm export john --format json --output data.json

| `mistral` | 4GB | ⚡⚡ | ⭐⭐⭐⭐ | Balanced |

| `llama3` | 5GB | ⚡ | ⭐⭐⭐⭐⭐ | Best quality |print("=" * 60)



```bashprint("👤 Customer 2: Sarah")# Get help

# Download a model

ollama pull <model-name>print("=" * 60)mem-llm --help



# List installed modelsagent.set_user("customer_sarah")```

ollama list

```



---print("💬 Sarah: I want to return item #67890")**Available CLI Commands:**



## 📦 Requirementsresponse = agent.chat("I want to return item #67890")



- Python 3.8+print(f"🤖 Bot: {response}\n")| Command | Description | Example |

- [Ollama](https://ollama.ai/) (for LLM)

- Minimum 4GB RAM|---------|-------------|---------|

- 5GB disk space

# Back to Customer 1 - remembers previous conversation!| `chat` | Interactive chat session | `mem-llm chat --user alice` |

**Python Dependencies (auto-installed):**

- `requests >= 2.31.0`print("=" * 60)| `check` | Verify system setup | `mem-llm check` |

- `pyyaml >= 6.0.1`

- `click >= 8.1.0`print("👤 Back to Customer 1: John")| `stats` | Show statistics | `mem-llm stats --user john` |



---print("=" * 60)| `export` | Export user data | `mem-llm export john` |



## 🐛 Troubleshootingagent.set_user("customer_john")| `clear` | Delete user data | `mem-llm clear john` |



### Ollama not running?



```bashprint("💬 John: What was my order number?")### Basic Chat

ollama serve

```response = agent.chat("What was my order number?")=======



### Model not found error?print(f"🤖 Bot: {response}")| Özellik | Açıklama |



```bash```|---------|----------|

# Download the model

ollama pull granite4:tiny-h| 🧠 **Kalıcı hafıza** | Her kullanıcının sohbet geçmişi saklanır |



# Check installed models**Output:**| 👥 **Çoklu kullanıcı** | Her kullanıcı için ayrı hafıza yönetimi |

ollama list

``````| 🔒 **Gizlilik** | Tamamen yerel çalışır, buluta veri göndermez |



### Connection error?============================================================| ⚡ **Hızlı** | Hafif SQLite veya JSON depolama seçenekleri |



```bash👤 Customer 1: John| 🎯 **Kolay kullanım** | Üç satırda çalışan örnek |

# Check if Ollama is running

curl http://localhost:11434============================================================| 📚 **Bilgi tabanı** | Ek yapılandırma olmadan dökümanlardan bilgi yükleme |



# Restart Ollama💬 John: My order #12345 is delayed| 🌍 **Türkçe desteği** | Türkçe diyaloglarda doğal sonuçlar |

ollama serve

```🤖 Bot: I'll help you check your order status...| 🛠️ **Araç entegrasyonu** | Gelişmiş araç sistemi ile genişletilebilir |



### Import error?



```bash============================================================---

# Upgrade to latest version

pip install --upgrade mem-llm👤 Customer 2: Sarah

```

============================================================## 🧑‍🏫 Tutorial

> If issues persist, run `mem-llm check` or `agent.check_setup()` and share the output when opening an issue.

💬 Sarah: I want to return item #67890

---

🤖 Bot: I can help you with the return process...Tamamlanmış örnekleri adım adım incelemek için [examples](examples) klasöründeki rehberleri izleyebilirsiniz. Bu dizinde hem temel kullanım senaryoları hem de ileri seviye entegrasyonlar yer alır. Öne çıkan içerikler:

## 📄 License



MIT License - Free to use in personal and commercial projects.

============================================================- [Basic usage walkthrough](examples/basic_usage.py) – ilk hafızalı ajanın nasıl oluşturulacağını gösterir.

---

👤 Back to Customer 1: John- [Customer support workflow](examples/customer_support.py) – çok kullanıcılı müşteri destek senaryosu.

## 🔗 Links

============================================================- [Knowledge base ingestion](examples/knowledge_base.py) – dokümanlardan bilgi yükleme.

- **PyPI:** https://pypi.org/project/mem-llm/

- **GitHub:** https://github.com/emredeveloper/Mem-LLM💬 John: What was my order number?

- **Ollama:** https://ollama.ai/

- **Documentation:** [GitHub Wiki](https://github.com/emredeveloper/Mem-LLM/wiki)🤖 Bot: Your order number is #12345, which you mentioned was delayed.Her dosyada kodun yanında açıklamalar bulunur; komutları kopyalayıp çalıştırarak sonuçları deneyimleyebilirsiniz.



---```



## 🌟 Support Us## 📖 Kullanım örnekleri



If you find this project useful, please ⭐ [star it on GitHub](https://github.com/emredeveloper/Mem-LLM)!---



---### Basic conversation



## 🤝 Contributing### Example 3: Turkish Language Support>>>>>>> f002396c8c531e4cde33d19ac6a755494b1b30cd



Contributions are welcome! Please feel free to submit a Pull Request.



1. Fork the repository```python```python

2. Create your feature branch (`git checkout -b feature/AmazingFeature`)

3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)from mem_llm import MemAgentfrom mem_llm import MemAgent

4. Push to the branch (`git push origin feature/AmazingFeature`)

5. Open a Pull Request



---agent = MemAgent()agent = MemAgent()



<div align="center">agent.set_user("alice")

Made with ❤️ by <a href="https://github.com/emredeveloper">C. Emre Karataş</a>

</div>print("🇹🇷 Türkçe Konuşma Örneği")


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
