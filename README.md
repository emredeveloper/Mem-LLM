# 🧠 Mem-LLM - Memory-Enabled AI Assistant

**Memory-enabled AI assistant that remembers conversations using local LLMs**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/mem-llm?label=PyPI)](https://pypi.org/project/mem-llm/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 What is it?

A lightweight Python library that adds **persistent memory** to local LLM chatbots. Each user gets their own conversation history that the AI remembers across sessions.

**Perfect for:**

- 💬 Customer service chatbots
- 🤖 Personal AI assistants
- 📝 Context-aware applications
- 🏢 Business automation

---

## ⚡ Quick Start

### 1. Install

```bash
pip install mem-llm
```

### 2. Setup Ollama (one-time)

```bash
# Install from: https://ollama.ai/download
ollama serve

# Download model (only 2.5GB)
ollama pull granite4:tiny-h
```

### 3. Use in Python

```python
from mem_llm import MemAgent

# Create agent
agent = MemAgent()
agent.set_user("john")

# Chat - it remembers!
agent.chat("My name is John")
agent.chat("What's my name?")  # → "Your name is John"
```

### 4. Or Use CLI

```bash
# Interactive chat
mem-llm chat --user john

# Check system status
mem-llm check

# View statistics
mem-llm stats
```

---

## ✨ Key Features

- 🧠 **Persistent Memory**: Remembers conversations across sessions
- 💬 **Context Awareness**: Uses conversation history for relevant responses
- 🏠 **Local & Private**: Runs entirely on your machine
- 🚀 **Lightweight**: Works with small local models (~2.5GB)
- 🎯 **Multi-Backend**: JSON and SQL memory storage options
- 📚 **Knowledge Base**: Config-free document integration
- 🌍 **Multi-language**: Works with any language
- 🖥️ **CLI Tool**: Built-in command-line interface

---

## 🔄 Memory Backend Comparison

| Feature | JSON Mode | SQL Mode |
|---------|-----------|----------|
| **Setup** | ✅ Zero config | ⚙️ Minimal config |
| **Conversation Memory** | ✅ Yes | ✅ Yes |
| **User Profiles** | ✅ Yes | ✅ Yes |
| **Knowledge Base** | ❌ No | ✅ Yes |
| **Advanced Search** | ❌ No | ✅ Yes |
| **Performance** | ⭐⭐ Good | ⭐⭐⭐ Excellent |
| **Best For** | 🏠 Personal use | 🏢 Business use |

---

## 📚 Documentation

- [📖 Full Documentation](Memory%20LLM/README.md)
- [🚀 Quick Start Guide](Memory%20LLM/QUICKSTART.md)
- [🔗 Integration Guide](Memory%20LLM/INTEGRATION_GUIDE.md)
- [📝 Changelog](Memory%20LLM/CHANGELOG.md)

---

## 🛠️ Development

### Setup Development Environment

```bash
cd "Memory LLM"
pip install -r requirements-dev.txt
```

### Run Tests

```bash
pytest tests/
```

---

## 📄 License

MIT License - feel free to use in personal and commercial projects!

---

## 🔗 Links

- **PyPI**: <https://pypi.org/project/mem-llm/>
- **GitHub**: <https://github.com/emredeveloper/Mem-LLM>
- **Ollama**: <https://ollama.ai/>

---

## 🌟 Star us on GitHub

If you find this useful, give us a ⭐ on [GitHub](https://github.com/emredeveloper/Mem-LLM)

---

Made with ❤️ by [C. Emre Karataş](https://github.com/emredeveloper)
