# Quickstart

Runnable examples, roughly in order of complexity. Each file is standalone:

```bash
python quickstart/02_basic_chat.py
```

## Before you start

Install the package and have a local backend running:

```bash
pip install mem-llm
```

- **Ollama** — `ollama serve`, then `ollama pull <model>` (default endpoint `http://localhost:11434`)
- **LM Studio** — start the local server from the Developer tab (default endpoint `http://localhost:1234/v1`)
- **llama.cpp** — `llama-server -m model.gguf --alias local-model --port 8080`

Examples that need a server print the error and keep going, so a missing
backend never crashes the script.

## Examples

| File | What it shows |
| --- | --- |
| `01_install_check.py` | Verify the install and print the version (no server needed) |
| `02_basic_chat.py` | Minimal chat against a local backend |
| `03_memory_recall.py` | Memory persisting across turns |
| `04_tools_demo.py` | Built-in tools (calculator) |
| `05_graph_memory_demo.py` | Graph memory and extracted triplets |
| `06_streaming_demo.py` | Chunk-by-chunk streaming |
| `07_multi_backend_demo.py` | Switching backends via `LLMClientFactory` |
| `08_custom_tool_demo.py` | Registering your own `@tool` |
| `09_security_demo.py` | Prompt injection protection |
| `10_metrics_demo.py` | Response metrics and confidence |
| `11_tool_policy_demo.py` | Tool allowlist / denylist policy (no server needed) |
| `12_workflow_async_demo.py` | Workflow engine with async steps |
| `13_hierarchical_memory_demo.py` | Hierarchical memory layers |
| `14_llamacpp_demo.py` | llama.cpp and OpenAI-compatible servers |
| `15_memory_router_demo.py` | `MemoryRouter` over core/archival/recall/graph |

## Choosing a model

Every example reads its model from the environment, so you do not have to edit
the files. Defaults are `granite4:3b` (Ollama) and `qwen3.5-2b` (LM Studio).

| Variable | Used by | Default |
| --- | --- | --- |
| `OLLAMA_MODEL` | most examples | `granite4:3b` |
| `LMSTUDIO_MODEL` | most examples | `qwen3.5-2b` |
| `BACKEND` / `MODEL` / `BASE_URL` | `12`, `13`, `15` | `ollama` / `granite4:3b` / backend default |
| `LLAMACPP_BACKEND` / `LLAMACPP_MODEL` / `LLAMACPP_BASE_URL` | `14` | `llamacpp` / `local-model` / `http://localhost:8080` |

Point them at whatever you have installed:

```bash
# PowerShell
$env:OLLAMA_MODEL="llama3.2:3b"; python quickstart/03_memory_recall.py

# bash
OLLAMA_MODEL=llama3.2:3b python quickstart/03_memory_recall.py
```

`14_llamacpp_demo.py` works against any `/v1/chat/completions` server — llama.cpp,
vLLM, or LM Studio's server:

```bash
# PowerShell — run it against LM Studio instead of llama.cpp
$env:LLAMACPP_BASE_URL="http://localhost:1234"; $env:LLAMACPP_MODEL="qwen3.5-2b"
python quickstart/14_llamacpp_demo.py
```

## Note on written data

Examples that use memory write to `memories/` next to your working directory.
Delete it to start clean.
