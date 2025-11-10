# Mem-LLM

[![PyPI version](https://badge.fury.io/py/mem-llm.svg)](https://pypi.org/project/mem-llm/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Mem-LLM is a Python framework for building privacy-first, memory-enabled AI assistants that run 100% locally. The project combines persistent multi-user conversation history with optional knowledge bases, multiple storage backends, vector search capabilities, response quality metrics, and tight integration with [Ollama](https://ollama.ai) and [LM Studio](https://lmstudio.ai) so you can experiment locally and deploy production-ready workflows with quality monitoring and semantic understanding - completely private and offline.

## 🆕 What's New in v1.3.6

- 🚫 **100% Local & Private** – Removed cloud dependency, Ollama and LM Studio only
- 🔒 **Zero External Calls** – Complete data sovereignty, no API calls to external services
- ⚡ **Streaming Response** – Real-time ChatGPT-style streaming (v1.3.3+)
- 🌐 **REST API & Web UI** – FastAPI server with modern interface (v1.3.3+)
- 🐛 **Bug Fixes** – Fixed API memory search and stats endpoints
- 📊 **Response Metrics** – Track quality, confidence, and performance (v1.3.1+)

## What's New in v1.3.2

- 📊 **Response Metrics** – Track confidence, latency, KB usage, and quality analytics
- 🔍 **Vector Search** – Semantic search with ChromaDB, cross-lingual support
- 🎯 **Quality Monitoring** – Production-ready metrics for response quality
- 🌐 **Semantic Understanding** – Understands meaning, not just keywords

[See full changelog](Memory%20LLM/CHANGELOG.md) | [Multi-Backend Guide](Memory%20LLM/MULTI_BACKEND_GUIDE.md)

## Features
- **100% Local & Private** *(v1.3.6)* – No cloud dependencies, all processing on your machine.
- **Streaming Response** *(v1.3.3+)* – Real-time ChatGPT-style streaming for Ollama and LM Studio.
- **REST API Server** *(v1.3.3+)* – FastAPI-based server with WebSocket and SSE streaming support.
- **Web UI** *(v1.3.3+)* – Modern 3-page interface (Chat, Memory Management, Metrics Dashboard).
- **Persistent Memory** – Store and recall conversation history across sessions for each user.
- **Multi-Backend Support** *(v1.3.0+)* – Choose between Ollama and LM Studio with unified API.
- **Auto-Detection** *(v1.3.0+)* – Automatically find and use available local LLM service.
- **Response Metrics** *(v1.3.1+)* – Track confidence, latency, KB usage, and quality analytics.
- **Vector Search** *(v1.3.2+)* – Semantic search with ChromaDB, cross-lingual support.
- **Flexible Storage** – Choose between lightweight JSON files or a SQLite database for production scenarios.
- **Knowledge Bases** – Load categorized Q&A content to augment model responses with authoritative answers.
- **Dynamic Prompting** – Automatically adapts prompts based on the features you enable, reducing hallucinations.
- **CLI & Tools** – Includes a command-line interface plus utilities for searching, exporting, and auditing stored memories.
- **Security Features** *(v1.1.0+)* – Prompt injection detection with risk-level assessment (opt-in).
- **High Performance** *(v1.1.0+)* – Thread-safe operations with 16K+ msg/s throughput, <1ms search latency.
- **Conversation Summarization** *(v1.2.0+)* – Automatic token compression (~40-60% reduction).
- **Multi-Database Support** *(v1.2.0+)* – Export/import to PostgreSQL, MongoDB, JSON, CSV, SQLite.

## Repository Layout
- `Memory LLM/` – Core Python package (`mem_llm`), configuration examples, packaging metadata, and detailed module-level documentation.
- `examples/` – Sample scripts that demonstrate common usage patterns.
- `LICENSE` – MIT license for the project.

> Looking for API docs or more detailed examples? Start with [`Memory LLM/README.md`](Memory%20LLM/README.md), which includes extensive usage guides, configuration options, and advanced workflows.

## Quick Start

### 1. Installation
```bash
pip install mem-llm

# Or with optional features
pip install mem-llm[databases]  # PostgreSQL + MongoDB
pip install mem-llm[postgresql]  # PostgreSQL only
pip install mem-llm[mongodb]     # MongoDB only

# Vector search support (v1.3.2+)
pip install chromadb sentence-transformers
```

### 2. Choose Your Backend

**Option A: Ollama (Local, Free)**
```bash
# Install Ollama from https://ollama.ai
ollama pull granite4:3b
ollama serve
```

**Option B: LM Studio (Local, GUI)**
```bash
# Download from https://lmstudio.ai
# Load a model and start server
```

### 3. Create and Chat

```python
from mem_llm import MemAgent

# Option A: Ollama
agent = MemAgent(backend='ollama', model="granite4:3b")

# Option B: LM Studio
agent = MemAgent(backend='lmstudio', model="local-model")

# Option C: Auto-detect
agent = MemAgent(auto_detect_backend=True)

# Use it!
agent.set_user("alice")
print(agent.chat("My name is Alice and I love Python!"))
print(agent.chat("What do I love?"))  # Agent remembers!

# NEW in v1.3.3: Streaming response
for chunk in agent.chat_stream("Tell me a story"):
    print(chunk, end="", flush=True)
```

### 4. Web UI & REST API (v1.3.3+)

```bash
# Install with API support
pip install mem-llm[api]

# Start API server (serves Web UI automatically)
python -m mem_llm.api_server

# Or use dedicated launcher
mem-llm-web

# Access Web UI at:
# http://localhost:8000          - Chat interface
# http://localhost:8000/memory   - Memory management
# http://localhost:8000/metrics  - Metrics dashboard
# http://localhost:8000/docs     - API documentation
```

### Multi-Backend Examples (v1.3.0+)
```python
from mem_llm import MemAgent

# LM Studio - Fast local inference with GUI
agent = MemAgent(
    backend='lmstudio',
    model='local-model',
    base_url='http://localhost:1234'
)

# Auto-detect - Use any available local backend
agent = MemAgent(auto_detect_backend=True)

# Advanced features still work!
agent = MemAgent(
    backend='ollama',           # NEW in v1.3.0
    model="granite4:3b",
    use_sql=True,              # Thread-safe SQLite storage
    enable_security=True       # Prompt injection protection
)
```

For advanced configuration (SQL storage, knowledge base support, business mode, etc.), copy `config.yaml.example` from the package directory and adjust it for your environment.

## Test Coverage (v1.3.6)
- ✅ **14+ tests for multi-backend support**
- ✅ Ollama and LM Studio backends (14 tests)
- ✅ Conversation Summarization (5 tests)
- ✅ Data Export/Import (11 tests - JSON, CSV, SQLite, PostgreSQL, MongoDB)
- ✅ Core MemAgent functionality (5 tests)
- ✅ Factory pattern and auto-detection (4 tests)

## Performance
- **Write Throughput**: 16,666+ records/sec
- **Search Latency**: <1ms for 500+ conversations
- **Token Compression**: 40-60% reduction with summarization (v1.2.0+)
- **Thread-Safe**: Full RLock protection on all SQLite operations
- **Multi-Database**: Seamless export/import across 5 formats (v1.2.0+)

## Contributing
Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request describing your changes. Make sure to include test coverage and follow the formatting guidelines enforced by the existing codebase.

## Links
- **PyPI**: https://pypi.org/project/mem-llm/
- **Documentation**: [Memory LLM/README.md](Memory%20LLM/README.md)
- **Changelog**: [Memory LLM/CHANGELOG.md](Memory%20LLM/CHANGELOG.md)
- **Issues**: https://github.com/emredeveloper/Mem-LLM/issues

## License
Mem-LLM is released under the [MIT License](LICENSE).
