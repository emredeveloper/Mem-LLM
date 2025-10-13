# ⚙️ Mem-Agent Configuration Guide

This guide explains step-by-step how to create and configure the `config.yaml` file.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Basic Configuration](#basic-configuration)
3. [Advanced Settings](#advanced-settings)
4. [Use Cases](#use-cases)
5. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Step 1: Create Config File

```bash
# Copy the config.yaml.example file in the main directory
cp config.yaml.example config.yaml

# Or on Windows:
copy config.yaml.example config.yaml
```

### Step 2: Edit Basic Settings

For the simplest usage, just configure these settings:

```yaml
# config.yaml

usage_mode: "personal"  # or "business"

llm:
  model: "granite4:tiny-h"
  base_url: "http://localhost:11434"

memory:
  backend: "json"
```

### Step 3: Using Config

```python
from mem_agent import MemAgent

# Create agent using config file
agent = MemAgent(config_file="config.yaml")
```

**✅ That's it! You're ready to use it.**

---

## 🔧 Basic Configuration

### 1. Usage Mode (`usage_mode`)

Determines how the agent behaves.

```yaml
usage_mode: "personal"  # or "business"
```

| Mode | Description | When to Use |
|------|-------------|-------------|
| `personal` | Personal assistant mode | Individual use, learning, reminders |
| `business` | Corporate mode | Customer service, multi-user, reporting |

### 2. LLM Settings (`llm`)

Ollama model configuration.

```yaml
llm:
  model: "granite4:tiny-h"        # Model to use
  base_url: "http://localhost:11434"  # Ollama API address
  temperature: 0.7                # Creativity (0.0-1.0)
  max_tokens: 500                 # Maximum response length
```

**Model Selection:**

| Model | Size | Speed | Recommended Usage |
|-------|------|-------|-------------------|
| `granite4:tiny-h` | Small | Very Fast | General use ⭐ |
| `llama3.2:3b` | Medium | Fast | Balanced performance |
| `mistral:7b` | Large | Slow | Advanced tasks |

**Temperature Values:**

- `0.0-0.3`: Consistent, predictable answers (customer service)
- `0.4-0.7`: Balanced (general use) ⭐
- `0.8-1.0`: Creative, diverse answers (brainstorming)

### 3. Memory System (`memory`)

Determines how conversations are stored.

```yaml
memory:
  backend: "json"           # "json" or "sql"
  json_dir: "memories"      # Folder for JSON
  db_path: "memories.db"    # Database for SQL
```

**Backend Comparison:**

| Feature | JSON | SQL |
|---------|------|-----|
| Setup | Very Easy ⭐ | Easy |
| Performance | Good | Very Good ⭐ |
| Search | Simple | Advanced ⭐ |
| Knowledge Base | ❌ | ✅ ⭐ |
| Recommended | Beginner | Production ⭐ |

### 4. Prompt Template (`prompt`)

Determines the bot's conversation style.

```yaml
prompt:
  template: "personal_assistant"  # Template to use
  variables:
    user_name: "John"
    tone: "friendly"
```

**Available Templates:**

| Template | Use Case |
|----------|----------|
| `personal_assistant` | Personal assistant ⭐ |
| `customer_service` | Customer service ⭐ |
| `tech_support` | Technical support |
| `sales_assistant` | Sales consultant |
| `education_tutor` | Education assistant |
| `health_advisor` | Health information |
| `booking_assistant` | Booking |
| `hr_assistant` | Human resources |

---

## 🎯 Advanced Settings

### Personal Mode Features

```yaml
personal:
  user_name: "John Doe"
  enable_reminders: true          # Reminder system
  enable_personal_notes: true     # Personal notes
  privacy_level: "high"           # Privacy level
  share_data: false               # Data sharing
```

### Business Mode Features

```yaml
business:
  company_name: "ABC Company"
  departments:
    - "Customer Service"
    - "Sales"
    - "Technical Support"
  enable_multi_user: true         # Multi-user
  enable_reporting: true          # Reporting
  security_level: "high"          # Security level
```

### Knowledge Base Configuration

```yaml
knowledge_base:
  enabled: true                   # Enable knowledge base
  auto_load: true                 # Auto-loading
  default_kb: "ecommerce"         # Default KB
  search_limit: 5                 # Search result limit
  min_relevance_score: 0.3        # Minimum relevance score
```

**Default KBs:**
- `ecommerce`: Ready-made information for e-commerce
- `tech_support`: Ready-made information for technical support
- `custom`: Load your own KB

### Security Settings

```yaml
security:
  filter_sensitive_data: true     # Filter sensitive data
  sensitive_keywords:
    - "credit card"
    - "password"
    - "social security"
  rate_limit:
    enabled: true
    max_requests_per_minute: 60
```

### Logging

```yaml
logging:
  enabled: true
  level: "INFO"                   # DEBUG, INFO, WARNING, ERROR
  file: "mem_agent.log"
  max_size_mb: 10
  backup_count: 5
  log_user_messages: true
  mask_sensitive: true            # Mask sensitive information
```

---

## 💼 Use Cases

### Scenario 1: Personal Assistant (Simplest)

```yaml
# config.yaml - Minimal setup

usage_mode: "personal"

llm:
  model: "granite4:tiny-h"

memory:
  backend: "json"
```

**Usage:**
```python
from mem_agent import MemAgent

agent = MemAgent(config_file="config.yaml")
agent.set_user("john123", name="John")
response = agent.chat("What should I do today?")
```

### Scenario 2: Customer Service (Recommended)

```yaml
# config.yaml - For customer service

usage_mode: "business"

llm:
  model: "granite4:tiny-h"
  temperature: 0.5              # For consistent answers

memory:
  backend: "sql"                # For advanced search
  db_path: "customer_memories.db"

prompt:
  template: "customer_service"
  variables:
    company_name: "ABC Store"
    tone: "professional and helpful"

knowledge_base:
  enabled: true
  auto_load: true
  default_kb: "ecommerce"

security:
  filter_sensitive_data: true
  rate_limit:
    enabled: true
    max_requests_per_minute: 100
```

### Scenario 3: Technical Support

```yaml
# config.yaml - For technical support

usage_mode: "business"

llm:
  model: "granite4:tiny-h"
  temperature: 0.3              # More technical, consistent

memory:
  backend: "sql"

prompt:
  template: "tech_support"
  variables:
    product_name: "XYZ Software"
    support_level: "L1 and L2"

knowledge_base:
  enabled: true
  default_kb: "tech_support"
  search_limit: 10              # More results

logging:
  level: "DEBUG"                # Detailed logging
  log_user_messages: true
```

### Scenario 4: Education Assistant

```yaml
# config.yaml - For education

usage_mode: "personal"

llm:
  model: "granite4:tiny-h"
  temperature: 0.6              # Explanatory and creative

prompt:
  template: "education_tutor"
  variables:
    subject: "Python Programming"
    level: "beginner"
    teaching_style: "step by step"

memory:
  backend: "sql"                # For learning history
```

---

## 🔍 Troubleshooting

### Error: "Config file not found"

**Solution:**
```bash
# Make sure config file is in the right place
ls config.yaml

# If not, create it
cp config.yaml.example config.yaml
```

### Error: "Ollama connection failed"

**Solution:**
```yaml
# config.yaml - Check URL
llm:
  base_url: "http://localhost:11434"  # Check port number
```

```bash
# Start Ollama service
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

### Error: "Model not found"

**Solution:**
```bash
# Download model
ollama pull granite4:tiny-h

# List available models
ollama list

# Use correct model name in config
```

### Error: "SQL database error"

**Solution:**
```yaml
# Switch to JSON (simpler)
memory:
  backend: "json"
  json_dir: "memories"
```

### Performance Issues

**Solution 1: Use smaller model**
```yaml
llm:
  model: "granite4:tiny-h"  # Fastest
```

**Solution 2: Reduce token limit**
```yaml
llm:
  max_tokens: 300  # Shorter responses
```

**Solution 3: Adjust memory limit**
```yaml
response:
  recent_conversations_limit: 3  # Less history
```

---

## 📚 Additional Resources

- **Quick Start**: [QUICKSTART.md](../QUICKSTART.md)
- **Integration Guide**: [INTEGRATION_GUIDE.md](../INTEGRATION_GUIDE.md)
- **Examples**: `examples/` folder
- **Project Structure**: [STRUCTURE.md](../STRUCTURE.md)

---

## 💡 Tips

1. **Start with JSON**: You can switch to SQL later
2. **Begin with minimal config**: Add only what you need
3. **Adjust temperature**: Optimize for your task
4. **Keep logging enabled**: Useful for debugging
5. **Don't skip security settings**: Always enable in production

---

**Last updated:** 2025-01-13  
**Version:** 2.0.0