# Mem-LLM Quickstart Examples

Quick examples to get started with `mem-llm` v2.1.3 from PyPI.

## 🆕 What's New in v2.1.3
- 🚀 **Smart Parser** - Tools execute even with natural language format
- ✅ **Better Reliability** - More forgiving tool call detection
- 🎯 **Clearer Instructions** - Improved system prompts with examples

## What's New in v2.1.0
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

### 6. ⭐ Async Tools (`06_async_tools_demo.py`) - NEW in v2.1.0
Non-blocking I/O operations with async tools.

```bash
python quickstart/06_async_tools_demo.py
```

**Features:**
- ✅ Built-in async HTTP tools (`fetch_url`, `post_json`)
- ✅ Async file operations
- ✅ Custom async tools
- ✅ Parallel async operations
- ✅ Automatic async/sync detection

---

### 7. ⭐ Input Validation (`07_validation_demo.py`) - NEW in v2.1.0
Comprehensive input validation for safer tool execution.

```bash
python quickstart/07_validation_demo.py
```

**Features:**
- ✅ Pattern validation (regex for emails, URLs)
- ✅ Range validation (min/max for numbers)
- ✅ Length validation (min/max for strings)
- ✅ Choice validation (enum-like)
- ✅ Custom validators
- ✅ Combined multi-parameter validation

---

### 8. ⭐ Tool Chaining (`08_tool_chaining_demo.py`) - NEW in v2.1.0
Multi-step tool workflows automated by the LLM.

```bash
python quickstart/08_tool_chaining_demo.py
```

**Features:**
- ✅ Sequential tool chains (A → B → C)
- ✅ File operation pipelines
- ✅ Data processing workflows
- ✅ Memory + tools integration
- ✅ Conditional chains (if-then logic)
- ✅ Mixed async/sync chains

---

### 9. ⭐ Memory-Aware Tools (`09_memory_tools_demo.py`) - NEW in v2.1.0
Self-aware agents that search their own conversation history.

```bash
python quickstart/09_memory_tools_demo.py
```

**Features:**
- ✅ `search_memory` - Find past conversations
- ✅ `get_user_info` - Get complete user profile
- ✅ `list_conversations` - List all chat history
- ✅ Memory + calculation chains
- ✅ Custom memory analysis tools
- ✅ Multi-user memory isolation

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

