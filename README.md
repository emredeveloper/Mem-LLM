# Mem-LLM

[![PyPI version](https://badge.fury.io/py/mem-llm.svg)](https://pypi.org/project/mem-llm/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Mem-LLM is a Python framework for building privacy-first, memory-enabled AI assistants that run entirely on local large language models. The project combines persistent multi-user conversation history with optional knowledge bases, multiple storage backends, and tight integration with [Ollama](https://ollama.ai) so you can experiment locally or deploy production-ready workflows without sending data to third-party services.

## 🆕 What's New in v1.1.0

- 🛡️ **Prompt Injection Protection** – Detects and blocks 15+ attack patterns (opt-in with `enable_security=True`)
- ⚡ **Thread-Safe Operations** – Fixed all race conditions, supports 200+ concurrent writes with zero errors
- 🔄 **Retry Logic** – Automatic exponential backoff for network errors (3 retries: 1s, 2s, 4s)
- 📝 **Structured Logging** – Production-ready logging with `MemLLMLogger`
- 💾 **SQLite WAL Mode** – Write-Ahead Logging for 16K+ writes/sec performance
- ✅ **100% Backward Compatible** – All v1.0.x code works without changes

[See full changelog](Memory%20LLM/CHANGELOG.md#110---2025-10-21)

## Features
- **Persistent Memory** – Store and recall conversation history across sessions for each user.
- **Local-Only Inference** – Use any Ollama model (Qwen3, DeepSeek, Llama3, Granite, etc.) without relying on cloud APIs.
- **Flexible Storage** – Choose between lightweight JSON files or a SQLite database for production scenarios.
- **Knowledge Bases** – Load categorized Q&A content to augment model responses with authoritative answers.
- **Dynamic Prompting** – Automatically adapts prompts based on the features you enable, reducing hallucinations.
- **CLI & Tools** – Includes a command-line interface plus utilities for searching, exporting, and auditing stored memories.
- **Security Features** *(v1.1.0+)* – Prompt injection detection with risk-level assessment (opt-in).
- **High Performance** *(v1.1.0+)* – Thread-safe operations with 16K+ msg/s throughput, <1ms search latency.

## Repository Layout
- `Memory LLM/` – Core Python package (`mem_llm`), configuration examples, packaging metadata, and detailed module-level documentation.
- `examples/` – Sample scripts that demonstrate common usage patterns.
- `LICENSE` – MIT license for the project.

> Looking for API docs or more detailed examples? Start with [`Memory LLM/README.md`](Memory%20LLM/README.md), which includes extensive usage guides, configuration options, and advanced workflows.

## Quick Start
1. Install the package:
   ```bash
   pip install mem-llm
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

### Enable Security Features (v1.1.0+)
```python
from mem_llm import MemAgent

# Enable prompt injection protection
agent = MemAgent(
    model="granite4:tiny-h",
    use_sql=True,              # Thread-safe SQLite storage
    enable_security=True       # Prompt injection protection
)

agent.set_user("alice")
response = agent.chat("Hello!")  # Protected from malicious inputs
```

For advanced configuration (SQL storage, knowledge base support, business mode, etc.), copy `config.yaml.example` from the package directory and adjust it for your environment.

## Development
This repository ships with a full automated test suite (27+ tests). After cloning the repo, install development dependencies and run the tests:

```bash
pip install -r "Memory LLM/requirements-dev.txt"
python -m pytest -c "Memory LLM/pyproject.toml"
```

You can also run the provided `tests/run_all_tests.py` script for an end-to-end verification of all features.

### Test Coverage (v1.1.0)
- ✅ Core functionality (10 tests)
- ✅ New improvements: logging, retry, WAL mode (4 tests)
- ✅ Backward compatibility (8 tests)
- ✅ Model compatibility: Qwen3:4b tested (5 tests)
- ✅ **27/27 tests passed** - 100% success rate

### Continuous Integration
All pushes and pull requests targeting `main` automatically run the same pytest command through [GitHub Actions](.github/workflows/ci.yml). Keeping the workflow green ensures that new changes respect the documented development workflow before merging.

## Performance (v1.1.0)
- **Write Throughput**: 16,666 records/sec
- **Search Latency**: <1ms for 500+ conversations
- **Concurrent Operations**: 200+ writes with zero errors
- **Thread-Safe**: Full RLock protection on all SQLite operations

## Contributing
Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request describing your changes. Make sure to include test coverage and follow the formatting guidelines enforced by the existing codebase.

## Links
- **PyPI**: https://pypi.org/project/mem-llm/
- **Documentation**: [Memory LLM/README.md](Memory%20LLM/README.md)
- **Changelog**: [Memory LLM/CHANGELOG.md](Memory%20LLM/CHANGELOG.md)
- **Issues**: https://github.com/emredeveloper/Mem-LLM/issues

## License
Mem-LLM is released under the [MIT License](LICENSE).
