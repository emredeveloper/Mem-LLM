# 🧠 Mem-Agent: Memory-Enabled Mini Assistant

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Ollama](https://img.shields.io/badge/Ollama-Compatible-orange.svg)](https://ollama.ai/)

**A local AI assistant that remembers user interactions and responds with context awareness using a lightweight 4-billion parameter LLM.**

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Examples](#-usage-examples)

</div>

---

## 🎯 Why Mem-Agent?

Most Large Language Models (LLMs) treat every conversation as "new" and don't remember past interactions. **Mem-Agent** uses a small locally-running model to:

- ✅ **Remember user history** - Separate memory for each customer/user
- ✅ **Context awareness** - Responds based on previous conversations
- ✅ **Fully local** - No internet connection required
- ✅ **Lightweight & fast** - Only 2.5 GB model size
- ✅ **Easy integration** - Get started with 3 lines of code

## 🚀 Quick Start

### 1. Install Ollama

```bash
# Windows/Mac/Linux: https://ollama.ai/download
curl https://ollama.ai/install.sh | sh

# Start the service
ollama serve
```

### 2. Download Model

```bash
ollama pull granite4:tiny-h
```

### 3. Use Mem-Agent

```python
from memory_llm import MemAgent

# Create agent
agent = MemAgent(model="granite4:tiny-h")

# System check
status = agent.check_setup()
if status['status'] == 'ready':
    print("✅ System ready!")
else:
    print("❌ Error:", status)

# Set user
agent.set_user("user123")

# First conversation
response = agent.chat("Hello, my name is Ali")
print(response)

# Second conversation - It remembers me!
response = agent.chat("Do you remember my name?")
print(response)
```

## 📚 Example Scripts

### 1. Simple Test

```bash
python examples/example_simple.py
```

### 2. Customer Service Simulation

```bash
python examples/example_customer_service.py
```

## 🏗️ Project Structure

```
Memory LLM/
├── memory_llm/              # Main package
│   ├── __init__.py          # Package initialization
│   ├── mem_agent.py         # Main assistant class
│   ├── memory_manager.py    # Memory management
│   ├── memory_db.py         # SQL database support
│   ├── llm_client.py        # Ollama integration
│   ├── memory_tools.py      # User tools
│   ├── knowledge_loader.py  # Knowledge base loader
│   ├── prompt_templates.py  # Prompt templates
│   └── config_manager.py    # Configuration manager
├── examples/                # Example scripts
├── tests/                   # Test files
├── setup.py                 # Installation script
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## 🔧 API Usage

### MemAgent Class

```python
from memory_llm import MemAgent

agent = MemAgent(
    model="granite4:tiny-h",           # Ollama model name
    memory_dir="memories",             # Memory directory
    ollama_url="http://localhost:11434" # Ollama API URL
)
```

#### Basic Methods

```python
# Set user
agent.set_user("user_id")

# Chat
response = agent.chat(
    message="Hello",
    user_id="optional_user_id",  # If set_user not used
    metadata={"key": "value"}     # Additional information
)

# Get memory summary
summary = agent.memory_manager.get_summary("user_id")

# Search in history
results = agent.search_user_history("keyword", "user_id")

# Update profile
agent.update_user_info({
    "name": "Ali",
    "preferences": {"language": "en"}
})

# Get statistics
stats = agent.get_statistics()

# Export memory
json_data = agent.export_memory("user_id")

# Clear memory (WARNING!)
agent.clear_user_memory("user_id", confirm=True)
```

### MemoryManager Class

```python
from memory_llm import MemoryManager

memory = MemoryManager(memory_dir="memories")

# Load memory
data = memory.load_memory("user_id")

# Add interaction
memory.add_interaction(
    user_id="user_id",
    user_message="Hello",
    bot_response="Hello! How can I help you?",
    metadata={"timestamp": "2025-01-13"}
)

# Get recent conversations
recent = memory.get_recent_conversations("user_id", limit=5)

# Search
results = memory.search_memory("user_id", "order")
```

### OllamaClient Class

```python
from memory_llm import OllamaClient

client = OllamaClient(model="granite4:tiny-h")

# Simple generation
response = client.generate("Hello world!")

# Chat format
response = client.chat([
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello"}
])

# Connection check
is_ready = client.check_connection()

# Model list
models = client.list_models()
```

## 💡 Usage Scenarios

### 1. Customer Service Bot
- Remembers customer history
- Knows previous issues
- Makes personalized recommendations

### 2. Personal Assistant
- Tracks daily activities
- Learns preferences
- Makes reminders

### 3. Education Assistant
- Tracks student progress
- Adjusts difficulty level
- Remembers past mistakes

### 4. Support Ticket System
- Stores ticket history
- Finds related old tickets
- Provides solution suggestions

## 📊 Memory Format

Memories are stored in JSON format:

```json
{
  "conversations": [
    {
      "timestamp": "2025-01-13T10:30:00",
      "user_message": "Hello",
      "bot_response": "Hello! How can I help you?",
      "metadata": {
        "topic": "greeting"
      }
    }
  ],
  "profile": {
    "user_id": "user123",
    "first_seen": "2025-01-13T10:30:00",
    "preferences": {},
    "summary": {}
  },
  "last_updated": "2025-01-13T10:35:00"
}
```

## 🔒 Privacy and Security

- ✅ Works completely locally (no internet connection required)
- ✅ Data stored on your computer
- ✅ No data sent to third-party services
- ✅ Memories in JSON format, easily deletable

## 🛠️ Development

### Test Mode

```python
# Simple chat without memory (for testing)
response = agent.simple_chat("Test message")
```

### Using Your Own Model

```python
# Different Ollama model
agent = MemAgent(model="llama2:7b")

# Or another LLM API
# Customize llm_client.py file
```

## 🐛 Troubleshooting

### Ollama Connection Error

```bash
# Start Ollama service
ollama serve

# Port check
netstat -an | findstr "11434"
```

### Model Not Found

```bash
# Check model list
ollama list

# Download model
ollama pull granite4:tiny-h
```

### Memory Issues

```python
# Check memory directory
import os
os.path.exists("memories")

# List memory files
os.listdir("memories")
```

## 📈 Performance

- **Model Size**: ~2.5 GB
- **Response Time**: ~1-3 seconds (depends on CPU)
- **Memory Usage**: ~4-6 GB RAM
- **Disk Usage**: ~10-50 KB per user

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

MIT License - See LICENSE file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - Local LLM server
- [Granite](https://www.ibm.com/granite) - IBM Granite models

## 📞 Contact

You can open an issue for your questions.

---

**Note**: This project is for educational and research purposes. Please perform comprehensive testing before using in production environment.