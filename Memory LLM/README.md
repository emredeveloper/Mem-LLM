# Mem-LLM 🧠💻

[![PyPI version](https://badge.fury.io/py/mem-llm.svg)](https://pypi.org/project/mem-llm/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/emredeveloper/Mem-LLM/blob/main/LICENSE)

**Mem-LLM** is a privacy-first, local Python framework for building memory-enabled AI assistants. By running entirely on your local machine, it combines persistent multi-user conversation history with configurable knowledge bases, robust storage backends, and seamless multi-model support. 

Perfect for privacy-first, production-ready workflows!

### 🔗 Quick Links
- **GitHub Repository:** [github.com/emredeveloper/Mem-LLM](https://github.com/emredeveloper/Mem-LLM)
- **PyPI Package:** [pypi.org/project/mem-llm/](https://pypi.org/project/mem-llm/)
- **Issue Tracker:** [Report a Bug or Request a Feature](https://github.com/emredeveloper/Mem-LLM/issues)

---

## 🚀 What's New in v2.4.6?

We've supercharged Mem-LLM with core stability and performance updates:
- **Major Bug Fixes:** Resolved critical memory handling, tool parsing, and backend compatibility issues.
- **Enhanced Database Reliability:** Improved SQL ordering and thread-safety behavior for concurrent operations.
- **Missing Dependencies Resolved:** Automatically includes `psutil` and `networkx`.
- **Updated Default Models:** 
  - Ollama now defaults to `granite4:3b`
  - LM Studio now defaults to `google/gemma-3-12b`

---

## ✨ Core Highlights

- **Persistent Multi-User Memory:** Keep context across sessions. Supports lightweight JSON or robust SQLite databases.
- **Advanced Tool Calling:** Endow your agent with superpowers! Use built-in tools or easily create your own with the `@tool` decorator.
- **Multi-Backend Flexible Support:** Switch seamlessly between **Ollama** and **LM Studio**.
- **Knowledge Base (RAG) & Vector Stores:** Empower your agent with your own documents and databases organically.
- **Conversation Analytics:** Track interactions, model performance, and agent behavior systematically.
- **REST API + Web UI:** Deploy your local agent instantly with the built-in, ready-to-use API server and slick web interface.
- **Real-Time Streaming:** Stream chat responses chunk by chunk for ultra-low latency experiences.

---

## 📦 Installation

Get up and running in seconds. 

```bash
pip install mem-llm
```

**Optional Power-ups:**
```bash
# Add API server dependencies (FastAPI, Uvicorn)
pip install mem-llm[api]

# Add advanced database support
pip install mem-llm[databases]
```

---

## ⚡ Quick Start

### Using Ollama 🦙
Make sure your Ollama instance is running, then try this simple example:

```python
from mem_llm import MemAgent

# Initialize the agent
agent = MemAgent(backend="ollama", model="granite4:3b")

# Set the active user (memory will be uniquely tied to this ID)
agent.set_user("alice")

# Chat and watch it remember!
print(agent.chat("Hi! My name is Alice and I am a Software Engineer."))
print(agent.chat("What was my name and what do I do?")) 
```

### Using LM Studio 🛠️
Ensure LM Studio's local server is running on its default port:

```python
from mem_llm import MemAgent

agent = MemAgent(backend="lmstudio", model="google/gemma-3-12b")
agent.set_user("bob")

print(agent.chat("Explain Python memory management in 2 sentences."))
```

---

## 📄 License

Mem-LLM is proudly open-source and released under the [MIT License](https://github.com/emredeveloper/Mem-LLM/blob/main/LICENSE). Build away!
