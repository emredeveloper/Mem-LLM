# 🧠 LLM'S - Memory-Enabled AI Assistant Collection

**A collection of memory-enabled AI assistants that remember conversations using local LLMs**

## 📦 Projects

### [Memory LLM](Memory%20LLM/) - Main Package
**Python library for memory-enabled AI assistants**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/mem-llm?label=PyPI)](https://pypi.org/project/mem-llm/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Memory-enabled AI assistant that remembers user interactions and provides context-aware responses using local LLMs.**

✨ **Key Features:**
- 🧠 **Persistent Memory**: Remembers conversations across sessions
- 💬 **Context Awareness**: Uses conversation history for relevant responses
- 🏠 **Local & Private**: Runs entirely on your machine
- 🚀 **Lightweight**: Works with small local models (~2.5GB)
- 🎯 **Multi-Backend**: JSON and SQL memory storage options
- 📚 **Knowledge Base**: Config-free document integration
- 🌍 **Turkish Support**: Native Turkish language processing

**Quick Start:**
```bash
pip install mem-llm==1.0.7
```

```python
from mem_llm import MemAgent

agent = MemAgent()
agent.set_user("user123")
agent.chat("Hello, my name is Alice")
agent.chat("What's my name?")  # → "Your name is Alice"
```

[📖 Full Documentation →](Memory%20LLM/README.md)

---

## 🎯 What is this?

This repository contains AI assistant projects that add **persistent memory** to local LLM chatbots. Each user gets their own conversation history that the AI remembers across sessions.

**Perfect for:**
- 💬 Customer service chatbots
- 🤖 Personal AI assistants
- 📝 Context-aware applications
- 🏢 Business automation

## 🚀 Quick Start

### 1. Install Ollama
```bash
# Visit https://ollama.ai/download for installation
ollama serve
```

### 2. Download Model
```bash
ollama pull granite4:tiny-h
```

### 3. Use Memory LLM
```python
from mem_llm import MemAgent

# Create agent (one line!)
agent = MemAgent()

# Set user
agent.set_user("john")

# Chat - it remembers!
agent.chat("My name is John")
agent.chat("What's my name?")  # → "Your name is John"
```

## 💡 Features

| Feature | Description |
|---------|-------------|
| 🧠 **Memory** | Remembers each user's conversation history |
| 👥 **Multi-user** | Separate memory for each user |
| 🔒 **Privacy** | 100% local, no cloud/API needed |
| ⚡ **Fast** | Lightweight SQLite/JSON storage |
| 🎯 **Simple** | 3 lines of code to get started |
| 📚 **Knowledge Base** | Config-free document integration |
| 🌍 **Turkish Support** | Native Turkish language processing |
| 🛠️ **Tools** | Extensible tool system for agents |

## 📚 Usage Examples

### Basic Chat
```python
from mem_llm import MemAgent

agent = MemAgent()
agent.set_user("alice")

# First conversation
agent.chat("I love pizza")

# Later...
agent.chat("What's my favorite food?")
# → "Your favorite food is pizza"
```

### Turkish Language Support
```python
# Works seamlessly with Turkish
agent.set_user("ahmet")
agent.chat("Benim adım Ahmet ve pizza seviyorum")
agent.chat("Adımı hatırlıyor musun?")
# → "Tabii ki Ahmet! Sizin pizza sevdiğinizi hatırlıyorum"
```

### Customer Service Bot
```python
agent = MemAgent()

# Customer 1
agent.set_user("customer_001")
agent.chat("My order #12345 is delayed")

# Customer 2 (different memory!)
agent.set_user("customer_002")
agent.chat("I want to return item #67890")
```

## 🔧 Project Structure

```
LLM'S/
├── Memory LLM/              # Main Python package
│   ├── mem_llm/            # Core library
│   ├── examples/           # Usage examples
│   ├── tests/              # Test suite
│   ├── docs/               # Documentation
│   └── README.md           # Package docs
├── advanced_customer_service.py  # Advanced example
├── company_knowledge.txt        # Knowledge base
└── README.md               # This file
```

## 📖 Documentation

- **[Memory LLM Documentation](Memory%20LLM/README.md)** - Complete guide for the main package
- **[Examples](Memory%20LLM/examples/)** - Various usage examples
- **[API Reference](Memory%20LLM/README.md#api-reference)** - Detailed API documentation

## 🛠️ Development

### Setup Development Environment
```bash
cd "Memory LLM"
pip install -e .
pip install -r requirements.txt
```

### Run Tests
```bash
cd "Memory LLM"
python -m pytest tests/
```

### Build Package
```bash
cd "Memory LLM"
python setup.py sdist bdist_wheel
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details.

## 🌟 Support

- **Issues**: Open an issue for questions or problems
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: Check the docs folder for detailed guides

---

<div align="center">
Made with ❤️ by <a href="https://github.com/emredeveloper">C. Emre Karataş</a>
</div>

