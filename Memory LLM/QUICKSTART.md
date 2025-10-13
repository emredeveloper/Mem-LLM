# 🚀 Quick Start Guide

Get up and running with Mem-Agent in 5 minutes!

## ⚡ Super Quick Setup

### Step 1: Install Ollama

```bash
# Download and install from: https://ollama.ai/download
# Or use command line:
curl https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve
```

### Step 2: Download Model

```bash
ollama pull granite4:tiny-h
```

### Step 3: Install Mem-Agent

```bash
pip install -r requirements.txt
```

### Step 4: First Test

```python
from mem_agent import MemAgent

# Create agent
agent = MemAgent(model="granite4:tiny-h")

# Set user
agent.set_user("test_user", name="Test User")

# Chat!
response = agent.chat("Hello, what's your name?")
print(response)

# Test memory
response = agent.chat("What did I just ask you?")
print(response)  # Should remember previous question
```

**🎉 You're ready!** The agent now remembers conversations.

---

## 🎯 Usage Modes

### Personal Mode (Simple)

```python
# Basic usage - JSON file storage
agent = MemAgent(use_sql=False)
agent.set_user("me")
agent.chat("Remember that I like pizza")
agent.chat("What food do I like?")  # "Pizza!"
```

### Business Mode (Advanced)

```python
# Advanced usage - SQL database + knowledge base
agent = MemAgent(
    use_sql=True,
    load_knowledge_base=True,
    config_file="config.yaml"
)

# Multiple users
agent.set_user("customer_001", name="John")
agent.chat("I need help with my order")

agent.set_user("customer_002", name="Jane") 
agent.chat("I want to return something")

# Switch back to John - memory preserved
agent.set_user("customer_001")
agent.chat("What was my question?")  # Remembers!
```

---

## ⚙️ Configuration (Optional)

### Step 4.5: Prepare Config File

For advanced features, create a config file:

```bash
cp config.yaml.example config.yaml
```

**Minimal config.yaml:**
```yaml
usage_mode: "personal"

llm:
  model: "granite4:tiny-h"
  base_url: "http://localhost:11434"

memory:
  backend: "json"
```

**For business use:**
```yaml
usage_mode: "business"

llm:
  model: "granite4:tiny-h"
  base_url: "http://localhost:11434"

memory:
  backend: "sql"
  max_memories_per_user: 1000

knowledge_base:
  enabled: true
  faq_file: "knowledge/faq.json"
```

See [docs/CONFIG_GUIDE.md](docs/CONFIG_GUIDE.md) for full configuration options.

---

## 🔧 Common Tasks

### Customer Service Bot

```python
agent = MemAgent(
    use_sql=True,
    load_knowledge_base=True,
    config_file="config.yaml"
)

# FAQ will be automatically loaded
agent.set_user("customer_001", name="Alice")
response = agent.chat("How do I reset my password?")
```

### Personal Assistant

```python
agent = MemAgent(use_sql=False)
agent.set_user("me")

agent.chat("Remind me to call mom at 6 PM")
# ... later ...
agent.chat("What reminders do I have?")
```

### Search History

```python
# Search through conversation history
results = agent.search_history("password", user_id="customer_001")
print(results)
```

### Export User Data

```python
# Export all data for a user
data = agent.export_user_data("customer_001")
print(data)
```

---

## 🚨 Troubleshooting

### "Model not found"
```bash
# Check if model is downloaded
ollama list

# If not found, download it
ollama pull granite4:tiny-h
```

### "Connection refused"
```bash
# Make sure Ollama is running
ollama serve

# Check if port 11434 is open
curl http://localhost:11434/api/tags
```

### "No memory"
```python
# Make sure you set user before chatting
agent.set_user("user123")
response = agent.chat("Hello")
```

### Performance Issues
```python
# Use smaller model for faster responses
agent = MemAgent(model="granite4:tiny-h")  # 2.5GB
# vs
agent = MemAgent(model="llama2:7b")  # 4GB+
```

---

## 📚 Next Steps

1. **Explore Examples**: Check [`examples/`](examples/) folder
2. **Read Config Guide**: [docs/CONFIG_GUIDE.md](docs/CONFIG_GUIDE.md)
3. **Integration**: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
4. **Run Tests**: `cd tests && python run_all_tests.py`

---

## 🆘 Need Help?

- **Documentation**: [docs/INDEX.md](docs/INDEX.md)
- **Examples**: [`examples/`](examples/) folder
- **Issues**: GitHub Issues for bugs
- **Discussions**: GitHub Discussions for questions

**Happy coding!** 🎉
