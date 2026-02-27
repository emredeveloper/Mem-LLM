# Mem-LLM

Mem-LLM is a local-first Python library for memory-enabled AI assistants with multi-backend LLM support.

## Highlights

- Persistent user memory (JSON or SQLite)
- Tool calling and built-in tools
- Multi-backend support (Ollama, LM Studio)
- Knowledge base and conversation analytics
- Streaming chat responses
- REST API and Web UI

## Default Models

- Ollama: `granite4:3b`
- LM Studio: `google/gemma-3-12b`

## Install

```bash
pip install mem-llm
```

Optional extras:

```bash
pip install mem-llm[api]
pip install mem-llm[databases]
```

## Quick Start

```python
from mem_llm import MemAgent

agent = MemAgent(backend="ollama", model="granite4:3b")
agent.set_user("alice")
print(agent.chat("My name is Alice."))
print(agent.chat("What is my name?"))
```

LM Studio:

```python
agent = MemAgent(backend="lmstudio", model="google/gemma-3-12b")
```

## Links

- PyPI: https://pypi.org/project/mem-llm/
- GitHub: https://github.com/emredeveloper/Mem-LLM
- Issues: https://github.com/emredeveloper/Mem-LLM/issues

## License

MIT
