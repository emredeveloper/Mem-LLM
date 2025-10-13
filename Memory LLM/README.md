# 🧠 Mem-Agent: Memory-Enabled Mini Assistant

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Ollama](https://img.shields.io/badge/Ollama-Compatible-orange.svg)](https://ollama.ai/)

**A local AI assistant that remembers user interactions and responds with context awareness using a lightweight 4-billion parameter LLM.**

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Examples](#-usage-examples)

</div>

---

## 🎯 Why Mem-Agent?

Most Large Language Models (LLMs) treat every conversation as "new" and don't remember past interactions. **Mem-Agent** uses a small locally-running model to:

- ✅ **Remember user history** - Separate memory for each customer/user
- ✅ **Context awareness** - Responds based on previous conversations
- ✅ **Fully local** - No internet connection required
- ✅ **Lightweight & fast** - Only 2.5 GB model size
- ✅ **Easy integration** - Get started with 3 lines of code

## 🚀 Quick Start

### 1. Install Ollama

```bash
# Windows/Mac/Linux: https://ollama.ai/download
curl https://ollama.ai/install.sh | sh

# Start the service
ollama serve
```

### 2. Download Model

```bash
ollama pull granite4:tiny-h
```

### 3. Use Memory-LLM

```python
from memory_llm import MemAgent

# Create agent
agent = MemAgent(model="granite4:tiny-h")

# Set user
agent.set_user("user123", name="John")

# Start chatting
response = agent.chat("Hello, where is my order?")
print(response)

# Bot will remember history
response = agent.chat("When will it arrive?")
print(response)  # Responds remembering the previous conversation
```

**That's it!** ✨

## ⭐ Features

### 🧠 Memory System

- **JSON Memory**: Simple, file-based memory (for beginners)
- **SQL Memory**: Advanced, relational database (for production)
- **User Profiles**: Separate data for each user
- **Search Features**: Search through conversation history

### 🎨 Prompt Templates

8+ ready-to-use templates:

| Template | Use Case |
|----------|----------|
| `personal_assistant` | Personal assistant |
| `customer_service` | Customer service |
| `tech_support` | Technical support |
| `sales_assistant` | Sales consultant |
| `education_tutor` | Education assistant |
| And more... | |

### 📚 Knowledge Base

- Store frequently asked questions (FAQ)
- Automatic knowledge search
- Custom knowledge base loading
- Excel/CSV import support

### 🛠️ User Tools

Users can with natural language:
- View conversation history
- Perform searches
- Export their data
- Manage memory

### 🔧 Two Usage Modes

**Personal** 🏠
- Individual use
- Reminders
- Learning tracking
- Personal notes

**Business** 💼
- Multi-user support
- Customer service
- Reporting
- Security features

## 💼 Use Cases

### Customer Service

```python
from memory_llm import MemAgent

agent = MemAgent(
    config_file="config.yaml",  # Customer service settings
    use_sql=True,               # For multi-user
    load_knowledge_base=True    # For FAQ
)

# Customer 1
agent.set_user("customer_001", name="John Doe")
response = agent.chat("When will my order arrive?")

# Customer 2
agent.set_user("customer_002", name="Jane Smith")
response = agent.chat("I want to return an item")

# John calls again - will remember history
agent.set_user("customer_001")
response = agent.chat("Can I cancel my order?")
```

### Personal Assistant

```python
agent = MemAgent(use_sql=False)  # Simple usage
agent.set_user("me")

agent.chat("Remind me about my dentist appointment tomorrow at 3 PM")
# ... next day ...
agent.chat("What do I need to do today?")
# Bot: "You have a dentist appointment at 3 PM!"
```

## 📊 Comparison

| Feature | Standard LLM | Mem-Agent |
|---------|--------------|-----------|
| User Memory | ❌ | ✅ |
| History Recall | ❌ | ✅ |
| Context Awareness | Limited | ✅ Advanced |
| Internet Required | Usually ✅ | ❌ Fully local |
| Model Size | 10GB+ | 2.5GB |
| Startup Time | Slow | ⚡ Fast |
| Cost | Paid API | 💰 Free |

## 📁 Project Structure

```
Memory LLM/
├── 📦 Core Modules
│   ├── mem_agent.py          # Main agent class
│   ├── memory_manager.py     # JSON memory
│   ├── memory_db.py          # SQL memory
│   └── memory_tools.py       # User tools
│
├── 📚 examples/              # Usage examples
│   ├── example_simple.py
│   ├── example_business_mode.py
│   └── example_customer_service.py
│
├── 🧪 tests/                 # Test files
│   └── run_all_tests.py
│
└── 📖 docs/                  # Documentation
    ├── CONFIG_GUIDE.md       # Configuration guide
    └── INDEX.md              # All documentation
```

## 🛠️ Installation

### Requirements

- Python 3.8+
- Ollama (local LLM server)
- 4GB+ RAM

### From PyPI (Recommended)

```bash
# Install the package
pip install memory-llm

# Download model
ollama pull granite4:tiny-h

# Start using
python -c "from memory_llm import MemAgent; agent = MemAgent(); print('✅ Ready!')"
```

### From Source (Development)

```bash
# 1. Clone the project
git clone https://github.com/yourusername/memory-llm.git
cd memory-llm

# 2. Install in development mode
pip install -e .

# 3. Create config file (optional)
cp memory_llm/config.yaml.example config.yaml

# 4. Run first example
python -m memory_llm.examples.example_simple
```

For detailed installation: [QUICKSTART_TR.md](QUICKSTART_TR.md)

## 📖 Documentation

| File | Description |
|------|-------------|
| [QUICKSTART_TR.md](QUICKSTART_TR.md) | 5-minute quick start |
| [docs/CONFIG_GUIDE.md](docs/CONFIG_GUIDE.md) | Configuration guide |
| [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) | Integration guide |
| [STRUCTURE.md](STRUCTURE.md) | Project structure |
| [CHANGELOG.md](CHANGELOG.md) | Changelog |

## 🎓 Usage Examples

```python
# Example 1: Simple Usage
from memory_llm import MemAgent

agent = MemAgent()
agent.set_user("user123")
response = agent.chat("Hello!")

# Example 2: With Config
agent = MemAgent(config_file="config.yaml")

# Example 3: With SQL Memory
agent = MemAgent(use_sql=True, load_knowledge_base=True)

# Example 4: With Metadata
response = agent.chat(
    "Where is order #12345?",
    metadata={"order_id": "12345", "priority": "high"}
)

# Example 5: Search History
results = agent.search_history("laptop", user_id="user123")
```

More examples in: [`examples/`](examples/) folder

## 🧪 Tests

```bash
cd tests
python run_all_tests.py

# Or specific tests
python run_all_tests.py basic
python run_all_tests.py integration
```

## ⚙️ Configuration

Minimal config example:

```yaml
# config.yaml
usage_mode: "personal"

llm:
  model: "granite4:tiny-h"
  base_url: "http://localhost:11434"

memory:
  backend: "json"
```

For detailed configuration: [docs/CONFIG_GUIDE.md](docs/CONFIG_GUIDE.md)

## 🤝 Contributing

We welcome your contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 🌟 Give it a Star!

If this project helped you, please give it a ⭐!

## 📧 Contact

- GitHub Issues: Bug reports and feature requests
- Discussions: Questions and discussions

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - Local LLM infrastructure
- Granite4 Model - Lightweight and powerful model
- Everyone who contributed to the community 🎉

---

<div align="center">

**[⬆ Back to Top](#-mem-agent-memory-enabled-mini-assistant)**

Made with ❤️ in Turkey

</div>

