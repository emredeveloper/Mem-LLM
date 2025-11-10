# Mem-LLM Quickstart Examples

Quick examples to get started with `mem-llm` from PyPI.

## 🚀 Installation

```bash
# Basic installation
pip install mem-llm

# With API/Web UI support
pip install mem-llm[api]

# With all optional features
pip install mem-llm[all]
```

## 📋 Prerequisites

Before running these examples, you need a local LLM backend:

### Option 1: Ollama (Recommended)
```bash
# Install Ollama from https://ollama.ai
ollama pull granite4:3b
ollama serve
```

### Option 2: LM Studio
```bash
# Download from https://lmstudio.ai
# Load a model and start the local server
```

## 📚 Examples

### 1. Basic Chat (`01_basic_chat.py`)
Simple chat with memory - remembers conversation context.

```bash
python quickstart/01_basic_chat.py
```

**Features:**
- ✅ Memory across conversations
- ✅ User context awareness
- ✅ Simple JSON storage

---

### 2. Streaming Response (`02_streaming_response.py`)
Real-time ChatGPT-style typing effect.

```bash
python quickstart/02_streaming_response.py
```

**Features:**
- ✅ Real-time streaming
- ✅ Character-by-character output
- ✅ Better UX for long responses

---

### 3. Multi-Backend Support (`03_multi_backend.py`)
Test different LLM backends (Ollama, LM Studio).

```bash
python quickstart/03_multi_backend.py
```

**Features:**
- ✅ Multiple backend support
- ✅ Auto-detection
- ✅ Fallback mechanisms

---

### 4. Web UI & REST API (`04_web_ui.py`)
Launch the full-featured web interface.

```bash
python quickstart/04_web_ui.py

# Or use the CLI command
mem-llm-web
```

**Access:**
- 🌐 Web UI: http://localhost:8000
- 🧠 Memory: http://localhost:8000/memory
- 📊 Metrics: http://localhost:8000/metrics
- 📝 API Docs: http://localhost:8000/docs

**Features:**
- ✅ Real-time chat interface
- ✅ Memory management UI
- ✅ Metrics dashboard
- ✅ REST API endpoints
- ✅ WebSocket streaming

---

### 5. Complete Demo (`05_complete_demo.py`)
Comprehensive showcase of all features.

```bash
python quickstart/05_complete_demo.py
```

**Includes:**
1. Basic chat with memory
2. SQL storage (production-ready)
3. Knowledge base integration
4. Streaming responses
5. Multi-user support

---

## 🎯 Quick Usage

```python
from mem_llm import MemAgent

# Create agent
agent = MemAgent(
    backend='ollama',
    model='granite4:3b'
)

# Set user
agent.set_user("alice")

# Chat
response = agent.chat("Hello!")
print(response)

# Streaming
for chunk in agent.chat_stream("Tell me a story"):
    print(chunk, end="", flush=True)
```

## 🔧 Configuration

### Using Ollama
```python
agent = MemAgent(
    backend='ollama',
    model='granite4:3b',
    base_url='http://localhost:11434'
)
```

### Using LM Studio
```python
agent = MemAgent(
    backend='lmstudio',
    model='local-model',
    base_url='http://localhost:1234'
)
```

### Auto-Detect Backend
```python
agent = MemAgent(auto_detect_backend=True)
```

## 📖 Documentation

- **Main Docs**: [README.md](https://github.com/emredeveloper/Mem-LLM)
- **API Reference**: Start server and visit `/docs`
- **More Examples**: [GitHub examples/](https://github.com/emredeveloper/Mem-LLM/tree/main/examples)

## 🐛 Troubleshooting

### Backend not found
```bash
# Check Ollama
curl http://localhost:11434/api/tags

# Check LM Studio
curl http://localhost:1234/v1/models
```

### Import errors
```bash
# Make sure mem-llm is installed
pip install mem-llm --upgrade

# For Web UI features
pip install mem-llm[api]
```

### Connection issues
- Ensure backend is running
- Check firewall settings
- Verify port numbers (11434 for Ollama, 1234 for LM Studio)

## 🚀 Next Steps

1. **Explore Web UI**: `mem-llm-web`
2. **Check GitHub**: More advanced examples
3. **Read Docs**: Full API documentation
4. **Join Community**: Report issues, suggest features

## 📄 License

MIT License - See [LICENSE](https://github.com/emredeveloper/Mem-LLM/blob/main/LICENSE)

---

**PyPI Package**: https://pypi.org/project/mem-llm/  
**GitHub**: https://github.com/emredeveloper/Mem-LLM

