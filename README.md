# Mem-LLM

[![PyPI version](https://badge.fury.io/py/mem-llm.svg)](https://pypi.org/project/mem-llm/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Mem-LLM is a privacy-first Python framework for building memory-enabled AI assistants that run locally.

## What's New in v2.5.0

- Added OpenAI-compatible and llama.cpp backend support.
- Added MemoryRouter for core memory, archival memory, recall, graph context, and KB retrieval.
- Added temporal graph memory with current and historical graph search.
- Simplified repeated backend and chat context-building code.

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

agent = MemAgent(backend="lmstudio", model="qwen3.5-2b")
agent.set_user("alice")
print(agent.chat("Summarize Python in one sentence."))
```

### llama.cpp

Start llama.cpp server with an OpenAI-compatible endpoint:

```powershell
llama-server.exe -m C:\path\to\model.gguf --alias local-model --host 127.0.0.1 --port 8080
```

Then connect Mem-LLM:

```python
from mem_llm import MemAgent

agent = MemAgent(
    backend="llamacpp",
    model="local-model",
    base_url="http://localhost:8080",
)
agent.set_user("alice")
print(agent.chat("Remember that I prefer concise answers."))
```

## Core Features

- Persistent memory per user (JSON or SQLite)
- Multi-backend support (Ollama, LM Studio, OpenAI-compatible APIs, llama.cpp)
- MemoryRouter with core memory, archival memory, recall, and graph context
- Temporal graph memory with current and historical lookup
- Tool calling system (`@tool`, built-in tools, validation)
- Streaming responses
- Knowledge base integration
- Conversation analytics
- REST API and Web UI

## Repository Layout

- `Memory LLM/` - main package source and release files
- `quickstart/` - step-by-step usage examples & tutorials


## Links

- PyPI: https://pypi.org/project/mem-llm/
- Documentation: [Memory LLM/README.md](Memory%20LLM/README.md)
- Changelog: [Memory LLM/CHANGELOG.md](Memory%20LLM/CHANGELOG.md)
- Issues: https://github.com/emredeveloper/Mem-LLM/issues

## License

Mem-LLM is released under the [MIT License](LICENSE).
