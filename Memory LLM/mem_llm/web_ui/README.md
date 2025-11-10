# Mem-LLM Web UI

Modern web interface for Mem-LLM with streaming support, memory management, and metrics dashboard.

## 📄 Pages

1. **💬 Chat (index.html)** - Main chat interface with real-time streaming
2. **🧠 Memory (memory.html)** - Memory management and search
3. **📊 Metrics (metrics.html)** - System metrics and statistics

## 🚀 Usage

```bash
# Install mem-llm with API support
pip install mem-llm[api]

# Launch Web UI (recommended)
mem-llm-web

# Or use launcher script
python start_web_ui.py
```

## 📋 Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- WebSockets

## 🔧 Configuration

Configure backend and model in the Web UI sidebar, or edit `api_server.py` defaults.

## 📚 More Info

- [Main README](../README.md)
- [API Docs](http://localhost:8000/docs)
- [Examples](../../examples/)

## 📄 License

MIT License

