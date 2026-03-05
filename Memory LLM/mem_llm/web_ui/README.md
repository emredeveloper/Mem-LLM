# Mem-LLM Web UI

Modern web interface for Mem-LLM with streaming support, memory management, and metrics dashboards.

## Pages

1. `index.html` - Main chat interface with streaming responses
2. `memory.html` - Memory management and search
3. `metrics.html` - Metrics and statistics views

## Usage

```bash
# Install mem-llm with API support
pip install mem-llm[api]

# Launch Web UI
mem-llm-web

# Or use the launcher script
python start_web_ui.py
```

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- WebSockets

## Configuration

Configure the backend and model in the Web UI sidebar, or edit the defaults in `api_server.py`.

## More Info

- [Main README](../README.md)
- [API Docs](http://localhost:8000/docs)
- [Examples](../../examples/)

## License

MIT License
