# Mem-LLM Package

Mem-LLM is a local-first library for memory-enabled AI assistants with multi-backend LLM support.

## Current Defaults

- Ollama model: `granite4:3b`
- LM Studio model: `google/gemma-3-12b`

## Installation

```bash
pip install mem-llm
```

Optional extras:

```bash
pip install mem-llm[api]
pip install mem-llm[databases]
```

## Basic Usage

```python
from mem_llm import MemAgent

agent = MemAgent(backend="ollama", model="granite4:3b")
agent.set_user("user_1")
reply = agent.chat("Remember that I like Python.")
```

LM Studio:

```python
agent = MemAgent(backend="lmstudio", model="google/gemma-3-12b")
```

## Main Components

- `mem_llm/mem_agent.py` - main agent orchestration
- `mem_llm/memory_manager.py` - JSON memory backend
- `mem_llm/memory_db.py` - SQL memory backend
- `mem_llm/tool_system.py` - tool parser, registry, execution
- `mem_llm/api_server.py` - FastAPI server
- `mem_llm/multi_agent/` - multi-agent primitives

## Testing

Run tests from workspace root:

```bash
python -m pytest "Memory LLM/tests" -q
```

LM Studio-focused run (exclude Ollama-specific tests):

```bash
python -m pytest "Memory LLM/tests" -q --ignore="Memory LLM/tests/integration/test_ollama_integration.py" -k "not ollama"
```

## Release

Build artifacts:

```bash
cd "Memory LLM"
python -m build
```

Artifacts are generated in `Memory LLM/dist/`.

## License

MIT
