# Mem-LLM Quickstart Examples

Quick examples to get started with `mem-llm` v2.1.3 from PyPI.

## 📦 Installation

```bash
pip install mem-llm
```

## 🚀 Quick Structure

```
quickstart/
├── simple/         # 🟢 Simple Examples (5 files)
│   ├── 01_hello.py              # Basic chat
│   ├── 02_streaming.py          # Live streaming
│   ├── 03_memory.py             # Multi-user memory
│   ├── 04_backends.py           # Ollama/LM Studio
│   └── 05_config.py             # YAML config
│
└── advanced/       # 🔴 Advanced Examples (4 files)
    ├── 01_tools.py              # All tool examples (ONE FILE!)
    ├── 02_async.py              # Async tools
    ├── 03_validation.py         # Input validation
    └── 04_knowledge_base.py     # Vector search & RAG
```

---

## 🟢 SIMPLE EXAMPLES

### 1️⃣ Hello World - `simple/01_hello.py`
Most basic usage - chat and memory

```python
from mem_llm import MemAgent

agent = MemAgent(backend='ollama', model='llama3.2:3b', use_sql=False)
agent.set_user("john")

response = agent.chat("Hello!")
print(response)
```

**Run:**
```bash
cd simple
python 01_hello.py
```

---

### 2️⃣ Streaming - `simple/02_streaming.py`
Real-time streaming responses

```python
for chunk in agent.chat_stream("What is Python?"):
    print(chunk, end="", flush=True)
```

---

### 3️⃣ Memory - `simple/03_memory.py`
Multi-user memory management

```python
agent.set_user("alice")
agent.chat("My name is Alice, I'm a software engineer")

agent.set_user("bob")
agent.chat("I'm Bob, I'm a doctor")

agent.set_user("alice")
agent.chat("What's my profession?")  # Remembers "software engineer"
```

---

### 4️⃣ Backends - `simple/04_backends.py`
Different LLM backends

```python
# Ollama
agent = MemAgent(backend='ollama', model='llama3.2:3b')

# LM Studio
agent = MemAgent(backend='lmstudio', model='any-model')

# Auto-detect
agent = MemAgent(backend='auto', model='llama3.2:3b')
```

---

### 5️⃣ YAML Config - `simple/05_config.py`
Load configuration from YAML file

```yaml
# config.yaml
backend: ollama
model: llama3.2:3b
use_sql: false
memory_dir: memories
```

```python
import yaml
with open("config.yaml") as f:
    config = yaml.safe_load(f)
    
agent = MemAgent(**config)
```

---

## 🔴 ADVANCED EXAMPLES

### 1️⃣ Tools (Function Calling) - `advanced/01_tools.py` ⭐
**ALL TOOL EXAMPLES IN ONE FILE!**

This single file includes:
- ✅ Built-in tools (18 ready-to-use tools)
- ✅ Custom tools (your own tools)
- ✅ Tool chaining (sequential execution)
- ✅ Memory tools (memory-aware)
- ✅ Workspace management

```python
from mem_llm import MemAgent, tool

# Tools enabled agent
agent = MemAgent(backend='ollama', model='llama3.2:3b', enable_tools=True)

# Use built-in tools
agent.chat("Calculate: (25 * 4) + 100")
agent.chat("Create file 'test.txt' with content 'Hello!'")

# Custom tool
@tool(name="greet", description="Greet someone")
def greet(name: str) -> str:
    return f"Hello, {name}!"

agent.tool_registry.register_tool(greet)
agent.chat("Use greet tool with name 'Alice'")
```

**Run:**
```bash
cd advanced
python 01_tools.py
```

---

### 2️⃣ Async Tools - `advanced/02_async.py`
Asynchronous tools (non-blocking)

```python
@tool(name="async_task", description="Async operation")
async def async_task(duration: float) -> str:
    await asyncio.sleep(duration)
    return f"Completed after {duration}s"
```

---

### 3️⃣ Validation - `advanced/03_validation.py`
Input validation (min/max, pattern, choices)

```python
@tool(
    name="validate_age",
    description="Validate age",
    min_value={"age": 18},
    max_value={"age": 120}
)
def validate_age(age: int) -> str:
    return f"Age {age} is valid!"
```

---

### 4️⃣ Knowledge Base - `advanced/04_knowledge_base.py`
Vector search & RAG

```python
agent = MemAgent(enable_kb=True)

# Add documents
agent.add_document("Python is a programming language...")

# Semantic search
results = agent.search_documents("programming", limit=3)

# RAG (automatic)
agent.chat("What do you know about Python?")
```

---

## 🎯 Recommended Learning Path

### Beginner:
1. `simple/01_hello.py` - Basic usage
2. `simple/02_streaming.py` - Streaming
3. `simple/03_memory.py` - Memory

### Intermediate:
4. `simple/04_backends.py` - Different LLMs
5. `simple/05_config.py` - Config files
6. `advanced/01_tools.py` - Function calling

### Advanced:
7. `advanced/02_async.py` - Async operations
8. `advanced/03_validation.py` - Input validation
9. `advanced/04_knowledge_base.py` - Vector search

---

## 🆕 What's New in v2.1.3

- ✅ **Smart tool call parser** - Natural language support
- ✅ **Tool workspace** - Organized file management (21 tools)
- ✅ **3 new workspace tools** - list, stats, cleanup
- 🐛 **Bug fixes** - create_json, search_memory, get_tool()

---

## 📚 Resources

- **PyPI**: https://pypi.org/project/mem-llm/
- **GitHub**: https://github.com/emredeveloper/Mem-LLM
- **Full Docs**: See `examples/` directory

---

## 💡 Tips

1. **Start simple** - Begin with `simple/01_hello.py`
2. **One file = one concept** - Each example focuses on ONE feature
3. **Tools = ONE file** - All tool examples in `advanced/01_tools.py`
4. **Copy & modify** - Use examples as templates
5. **Check logs** - Enable logging for debugging

**Need help?** Open an issue on GitHub! 🚀

