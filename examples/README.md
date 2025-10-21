# 📚 Mem-LLM Examples

Quick, ready-to-run scripts that show how to get the most out of Mem-LLM.

## 🚀 Quick Start
1. Install the package: `pip install mem-llm`
2. Launch Ollama: `ollama serve`
3. Download a model: `ollama pull granite4:tiny-h`
4. Run an example: `python 01_hello_world.py`

## 📂 Example Guide
| File | What it shows |
| --- | --- |
| `01_hello_world.py` | Five-line hello world introduction. |
| `02_basic_memory.py` | JSON memory mode and profile recall. |
| `03_multi_user.py` | Separate memories for multiple users. |
| `04_customer_service.py` | Returning customer support workflow. |
| `05_knowledge_base.py` | FAQ answers backed by the knowledge base (SQL mode). |
| `06_cli_demo.py` | CLI commands for chat, stats, and export. |
| `07_document_config.py` | Loading configuration from documents. |
| `08_conversation_summarization.py` | Summarizing long conversations. |
| `09_data_export_import.py` | Exporting and importing stored memories. |
| `10_database_connection_test.py` | Verifying SQL connectivity. |

## 💡 Tips
- Start with `01_hello_world.py`, then move to the scenario you need.
- Use JSON mode for quick experiments; switch to SQL for multi-user setups.
- Knowledge base features require SQL mode (`use_sql=True`).

## 🆘 Troubleshooting
- **Ollama not running?** `ollama serve`
- **Model missing?** `ollama pull granite4:tiny-h`
- **Import error?** `pip install mem-llm --upgrade`

## 📚 More Resources
- Main docs: `Memory LLM/README.md`
- Configuration guide: `Memory LLM/docs/CONFIG_GUIDE.md`
- Integration guide: `Memory LLM/INTEGRATION_GUIDE.md`
- Changelog: `Memory LLM/CHANGELOG.md`

**Happy coding!** 🎉
