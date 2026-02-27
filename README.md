# Mem-LLM

[![PyPI version](https://badge.fury.io/py/mem-llm.svg)](https://pypi.org/project/mem-llm/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Mem-LLM is a privacy-first Python framework for building memory-enabled AI assistants that run locally.

## What's New in v2.4.4

- Fixed critical memory, tool parsing, and backend compatibility issues.
- Improved SQL ordering and thread-safety behavior.
- Added missing runtime dependencies (`psutil`, `networkx`).
- Updated backend defaults:
  - Ollama: `granite4:3b`
  - LM Studio: `google/gemma-3-12b`

## Quick Start

### Install

```bash
pip install mem-llm
```

### Ollama

```python
from mem_llm import MemAgent

agent = MemAgent(backend="ollama", model="granite4:3b")
agent.set_user("alice")
print(agent.chat("My name is Alice."))
print(agent.chat("What is my name?"))
```

### LM Studio

```python
from mem_llm import MemAgent

agent = MemAgent(backend="lmstudio", model="google/gemma-3-12b")
agent.set_user("alice")
print(agent.chat("Summarize Python in one sentence."))
```

## Core Features

- Persistent memory per user (JSON or SQLite)
- Multi-backend support (Ollama, LM Studio)
- Tool calling system (`@tool`, built-in tools, validation)
- Streaming responses
- Knowledge base integration
- Conversation analytics
- REST API and Web UI

## Repository Layout

- `Memory LLM/` - main package source and release files
- `demos/` - usage examples
- `quickstart/` - quick scripts

## Links

- PyPI: https://pypi.org/project/mem-llm/
- Documentation: [Memory LLM/README.md](Memory%20LLM/README.md)
- Changelog: [Memory LLM/CHANGELOG.md](Memory%20LLM/CHANGELOG.md)
- Issues: https://github.com/emredeveloper/Mem-LLM/issues

## License

Mem-LLM is released under the [MIT License](LICENSE).
