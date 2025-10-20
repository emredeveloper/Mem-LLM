# Mem-LLM

Mem-LLM is a Python framework for building privacy-first, memory-enabled AI assistants that run entirely on local large language models. The project combines persistent multi-user conversation history with optional knowledge bases, multiple storage backends, and tight integration with [Ollama](https://ollama.ai) so you can experiment locally or deploy production-ready workflows without sending data to third-party services.

## Features
- **Persistent Memory** – Store and recall conversation history across sessions for each user.
- **Local-Only Inference** – Use any Ollama model (Qwen3, DeepSeek, Llama3, Granite, etc.) without relying on cloud APIs.
- **Flexible Storage** – Choose between lightweight JSON files or a SQLite database for production scenarios.
- **Knowledge Bases** – Load categorized Q&A content to augment model responses with authoritative answers.
- **Dynamic Prompting** – Automatically adapts prompts based on the features you enable, reducing hallucinations.
- **CLI & Tools** – Includes a command-line interface plus utilities for searching, exporting, and auditing stored memories.

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
   print(agent.chat("What do I love?"))
   ```

For advanced configuration (SQL storage, knowledge base support, business mode, etc.), copy `config.yaml.example` from the package directory and adjust it for your environment.

## Development
This repository ships with a full automated test suite. After cloning the repo, install development dependencies and run the tests:

```bash
pip install -r "Memory LLM/requirements-dev.txt"
python -m pytest -c "Memory LLM/pyproject.toml"
```

You can also run the provided `tests/run_all_tests.py` script for an end-to-end verification of all features.

## Contributing
Contributions, bug reports, and feature requests are welcome! Please open an issue or submit a pull request describing your changes. Make sure to include test coverage and follow the formatting guidelines enforced by the existing codebase.

## License
Mem-LLM is released under the [MIT License](LICENSE).
