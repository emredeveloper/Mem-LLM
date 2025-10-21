# Mem-LLM

[![PyPI version](https://badge.fury.io/py/mem-llm.svg)](https://pypi.org/project/mem-llm/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Mem-LLM is a Python framework for building privacy-first, memory-enabled AI assistants that run entirely on local large language models. The project combines persistent multi-user conversation history with optional knowledge bases, multiple storage backends, and tight integration with [Ollama](https://ollama.ai) so you can experiment locally or deploy production-ready workflows without sending data to third-party services.

## 🆕 What's New in v1.2.0

- � **Conversation Summarization** – Automatic conversation compression (~40-60% token reduction)
- 📤 **Data Export/Import** – JSON, CSV, SQLite, PostgreSQL, MongoDB support
- 🗄️ **Multi-Database** – Enterprise-ready PostgreSQL & MongoDB integration
- �️ **In-Memory DB** – Use `:memory:` for temporary operations
- � **Cleaner Logs** – Default WARNING level for production-ready output
- � **Bug Fixes** – Database path handling, organized SQLite files

[See full changelog](Memory%20LLM/CHANGELOG.md#120---2025-10-21)

## Features
- **Persistent Memory** – Store and recall conversation history across sessions for each user.
- **Local-Only Inference** – Use any Ollama model (Qwen3, DeepSeek, Llama3, Granite, etc.) without relying on cloud APIs.
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
1. Install the package:
   ```bash
   pip install mem-llm
   
   # Or with optional database support
   pip install mem-llm[databases]  # PostgreSQL + MongoDB
   pip install mem-llm[postgresql]  # PostgreSQL only
   pip install mem-llm[mongodb]     # MongoDB only
   ```
2. Install and start Ollama, then pull a model:
   ```bash
   ollama pull granite4:tiny-h
   ollama serve
   ```
3. Create and chat with an agent:
   ```python
   from mem_llm import MemAgent

   agent = MemAgent(model="granite4:tiny-h")
   agent.set_user("alice")
   print(agent.chat("My name is Alice and I love Python!"))
   print(agent.chat("What do I love?"))  # Agent remembers!
   ```

### Enable Advanced Features
```python
from mem_llm import MemAgent, ConversationSummarizer, DataExporter

# Security + Summarization
agent = MemAgent(
    model="granite4:tiny-h",
    use_sql=True,              # Thread-safe SQLite storage
    enable_security=True       # Prompt injection protection (v1.1.0+)
)

agent.set_user("alice")
response = agent.chat("Hello!")

# Summarize conversations to save tokens (v1.2.0+)
summarizer = ConversationSummarizer(agent.llm)
conversations = agent.memory.get_recent_conversations("alice", 10)
summary = summarizer.summarize_conversations(conversations, user_id="alice")

# Export data to multiple formats (v1.2.0+)
exporter = DataExporter(agent.memory)
exporter.export_to_json("alice", "backup.json")
exporter.export_to_postgresql("alice", "postgresql://localhost/db")
```

For advanced configuration (SQL storage, knowledge base support, business mode, etc.), copy `config.yaml.example` from the package directory and adjust it for your environment.

## Test Coverage (v1.2.0)
- ✅ **16/16 tests passed** - 100% success rate
- ✅ Conversation Summarization (5 tests)
- ✅ Data Export/Import (11 tests - JSON, CSV, SQLite, PostgreSQL, MongoDB)
- ✅ Core MemAgent functionality (5 tests)
- ✅ All v1.2.0 features validated

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
