# Mem-LLM 🧠💻

[![PyPI version](https://badge.fury.io/py/mem-llm.svg)](https://pypi.org/project/mem-llm/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/emredeveloper/Mem-LLM/blob/main/LICENSE)

**Mem-LLM** is a privacy-first, local Python framework for building memory-enabled AI assistants. By running entirely on your local machine, it combines persistent multi-user conversation history with configurable knowledge bases, robust storage backends, and seamless multi-model support.

Perfect for privacy-first, production-ready workflows!

### 🔗 Quick Links
- **GitHub Repository:** [github.com/emredeveloper/Mem-LLM](https://github.com/emredeveloper/Mem-LLM)
- **PyPI Package:** [pypi.org/project/mem-llm/](https://pypi.org/project/mem-llm/)
- **Issue Tracker:** [Report a Bug or Request a Feature](https://github.com/emredeveloper/Mem-LLM/issues)

---

## What's New in v2.5.1

Dependency fixes. Graph memory needs `pydantic` and the API server's upload endpoint needs
`python-multipart`; neither was declared, so on a clean install graph memory silently degraded
to a no-op and `pip install mem-llm[api]` could not import the API server. Both are now
declared, so a plain `pip install mem-llm` gets working graph memory.

---

## What's New in v2.5.0

This release expands local backend support and upgrades long-term memory:
- **OpenAI-Compatible Backends:** Use any `/v1/chat/completions` compatible server.
- **llama.cpp Support:** Connect directly to `llama-server` with `backend="llamacpp"`.
- **MemoryRouter:** Unified core memory, archival memory, recall, graph context, and KB retrieval.
- **Temporal Graph Memory:** Track current facts and historical facts with validity windows.
- **Cleanup:** Reduced duplicated backend alias and chat context-building logic.

---

## ✨ Core Highlights

- **Persistent Multi-User Memory:** Keep context across sessions. Supports lightweight JSON or robust SQLite databases.
- **Advanced Tool Calling:** Endow your agent with superpowers! Use built-in tools or easily create your own with the `@tool` decorator.
- **Multi-Backend Flexible Support:** Switch between **Ollama**, **LM Studio**, **OpenAI-compatible APIs**, and **llama.cpp**.
- **Long-Term Memory Routing:** Combine core memory, archival memory, recall, knowledge base, and graph context.
- **Temporal Graph Memory:** Preserve changing facts without losing history.
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
# Add semantic search (ChromaDB + local embeddings)
pip install mem-llm[vector]

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

agent = MemAgent(backend="lmstudio", model="qwen3.5-2b")
agent.set_user("bob")

print(agent.chat("Explain Python memory management in 2 sentences."))
```

### Using llama.cpp
Start `llama-server` with an OpenAI-compatible endpoint:

```powershell
llama-server.exe -m C:\path\to\model.gguf --alias local-model --host 127.0.0.1 --port 8080
```

Connect Mem-LLM:

```python
from mem_llm import MemAgent

agent = MemAgent(
    backend="llamacpp",
    model="local-model",
    base_url="http://localhost:8080",
)
agent.set_user("carol")

print(agent.chat("Remember that I prefer concise answers."))
```

---

## 🔍 Knowledge Base Search

Search is ranked by **BM25** out of the box — no extra install needed, since
SQLite ships with the FTS5 full-text index. Entries are ordered by how well
they actually match, and stemming means `refunds` finds `refund`.

```python
from mem_llm.memory_db import SQLMemoryManager

db = SQLMemoryManager(db_path="memories/kb.db")
db.add_knowledge("billing", "How do I get a refund?", "Refunds are issued within 5 business days.")

db.search_knowledge("how long do refunds take")
```

Install the `vector` extra to add semantic search on top:

```bash
pip install mem-llm[vector]
```

```python
db = SQLMemoryManager(db_path="memories/kb.db", enable_vector_search=True)

# Finds the refund entry even though they share no words.
db.search_knowledge("how do I get my money back")
```

With the extra installed, keyword and semantic results are merged using
Reciprocal Rank Fusion, so exact terms and paraphrases both work. Embeddings
run locally — nothing leaves your machine.

See [`quickstart/16_knowledge_search_demo.py`](../quickstart/16_knowledge_search_demo.py) for a runnable example.

---

## 📄 License

Mem-LLM is proudly open-source and released under the [MIT License](https://github.com/emredeveloper/Mem-LLM/blob/main/LICENSE). Build away!
