# Mem-LLM Quickstart Examples

Quick examples to get started with `mem-llm` v2.1.0 from PyPI.

## 🆕 What's New in v2.1.0
- 🚀 **Async Tool Support** - Non-blocking I/O operations
- ✅ **Input Validation** - Pattern, range, and custom validators
- 🌐 **Built-in Async Tools** - HTTP requests, file operations
- 🛡️ **Safer Execution** - Pre-validation prevents errors

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

### Basic Chat
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

### Function Calling (v2.0.0+)
```python
from mem_llm import MemAgent, tool

# Enable tools
agent = MemAgent(enable_tools=True)
agent.set_user("alice")

# Use built-in tools
agent.chat("Calculate (25 * 4) + 10")
agent.chat("Search my memory for 'Python'")

# Create custom tool
@tool(name="greet", description="Greet user")
def greet(name: str) -> str:
    return f"Hello, {name}!"

agent = MemAgent(enable_tools=True, tools=[greet])
agent.chat("Greet Alice")
```

### Tool Validation (v2.1.0+)
```python
from mem_llm import tool

# Email validation
@tool(
    name="send_email",
    pattern={"email": r'^[\w\.-]+@[\w\.-]+\.\w+$'},
    min_length={"email": 5},
    max_length={"email": 254}
)
def send_email(email: str) -> str:
    return f"Email sent to {email}"

# Range validation
@tool(
    name="set_volume",
    min_value={"volume": 0},
    max_value={"volume": 100}
)
def set_volume(volume: int) -> str:
    return f"Volume: {volume}"

# Choice validation
@tool(
    name="set_lang",
    choices={"lang": ["python", "javascript", "rust"]}
)
def set_lang(lang: str) -> str:
    return f"Language: {lang}"
```

### Async Tools (v2.1.0+)
```python
from mem_llm import tool
import asyncio

# Async tool
@tool(name="wait", description="Wait N seconds")
async def wait(seconds: float) -> str:
    await asyncio.sleep(seconds)
    return f"Waited {seconds}s"

# Agent handles async automatically
agent = MemAgent(enable_tools=True, tools=[wait])
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

