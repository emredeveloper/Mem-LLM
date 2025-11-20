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
| `11_lmstudio_example.py` | Using LM Studio backend. |
| `13_multi_backend_comparison.py` | Comparing different LLM backends. |
| `14_auto_detect_backend.py` | Auto-detecting available LLM services. |
| `15_response_metrics.py` | Response quality metrics and analytics (v1.3.1+). |
| `16_vector_search.py` | Semantic/vector search with ChromaDB (v1.3.2+). |
| `17_streaming_example.py` | Real-time streaming responses (v1.3.3+). |
| `18_function_calling.py` | **NEW!** Function calling / Tools (v2.0.0+). |
| `19_memory_tools_demo.py` | **NEW!** Memory-aware tools (v2.0.0+). |
| `20_async_and_validation.py` | **NEW!** Async tools & validation (v2.1.0+). |
| `21_analytics_and_presets.py` | **NEW!** Analytics & Config Presets (v2.1.4+). |

## 💡 Tips
- Start with `01_hello_world.py`, then move to the scenario you need.
- Use JSON mode for quick experiments; switch to SQL for multi-user setups.
- Knowledge base features require SQL mode (`use_sql=True`).

## 🆘 Troubleshooting
- **Ollama not running?** `ollama serve`
- **Model missing?** `ollama pull granite4:tiny-h`
- **Import error?** `pip install mem-llm --upgrade`

**Happy coding!** 🎉
