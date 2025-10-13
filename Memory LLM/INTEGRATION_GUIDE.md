# 🔗 Mem-Agent Integration Guide

This guide explains step-by-step how to integrate Mem-Agent into your own system.

## 📋 Table of Contents

1. [Quick Integration](#quick-integration)
2. [Configuration](#configuration)
3. [Web API Integration](#web-api-integration)
4. [Database Integration](#database-integration)
5. [Custom Knowledge Base](#custom-knowledge-base)
6. [Custom Prompt Templates](#custom-prompt-templates)
7. [Production Deployment](#production-deployment)

---

## 🚀 Quick Integration

### Step 1: Installation

```bash
# Install required packages
pip install -r requirements.txt

# OR for development mode
pip install -e .
```

### Step 2: Basic Usage

```python
from mem_agent import MemAgent

# Create agent
agent = MemAgent(config_file="config.yaml")

# Set user
agent.set_user("user_123", name="John")

# Chat
response = agent.chat("Hello!")
print(response)
```

---

## ⚙️ Configuration

### config.yaml File

Create a configuration file to customize Mem-Agent:

```yaml
# config.yaml

usage_mode: "business"  # or "personal"

llm:
  model: "granite4:tiny-h"
  base_url: "http://localhost:11434"
  temperature: 0.7

memory:
  backend: "sql"  # or "json"
  db_path: "memories.db"

prompt:
  template: "customer_service"
  variables:
    company_name: "Your Company"

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

### Environment Variables

You can also use environment variables:

```bash
export MEM_AGENT_MODEL="granite4:tiny-h"
export MEM_AGENT_BASE_URL="http://localhost:11434"
export MEM_AGENT_DB_PATH="memories.db"
```

---

## 🌐 Web API Integration

### Flask Example

```python
from flask import Flask, request, jsonify
from mem_agent import MemAgent

app = Flask(__name__)
agent = MemAgent(config_file="config.yaml")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')
    
    # Set user
    agent.set_user(user_id)
    
    # Get response
    response = agent.chat(message)
    
    return jsonify({
        'response': response,
        'user_id': user_id
    })

@app.route('/history/<user_id>')
def get_history(user_id):
    agent.set_user(user_id)
    history = agent.get_conversation_history()
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True)
```

### FastAPI Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mem_agent import MemAgent

app = FastAPI()
agent = MemAgent(config_file="config.yaml")

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    user_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        agent.set_user(request.user_id)
        response = agent.chat(request.message)
        
        return ChatResponse(
            response=response,
            user_id=request.user_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{user_id}")
async def get_history(user_id: str):
    try:
        agent.set_user(user_id)
        history = agent.get_conversation_history()
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## 🗄️ Database Integration

### SQL Database Setup

```python
from mem_agent import MemAgent

# Agent with SQL backend
agent = MemAgent(
    use_sql=True,
    config_file="config.yaml"
)

# The agent will automatically create tables:
# - users
# - conversations
# - memories
# - knowledge_base
```

### Custom Database Connection

```python
import sqlite3
from mem_agent import MemAgent

# Custom database path
config = {
    'memory': {
        'backend': 'sql',
        'db_path': '/custom/path/memories.db'
    }
}

agent = MemAgent(config_dict=config)
```

### Database Queries

```python
# Get all users
users = agent.memory_manager.get_all_users()

# Get user conversation count
count = agent.memory_manager.get_conversation_count("user_123")

# Search across all conversations
results = agent.search_history("keyword", user_id=None)
```

---

## 📚 Custom Knowledge Base

### Creating Knowledge Base

```python
# knowledge_base.json
{
    "faq": [
        {
            "question": "How do I reset my password?",
            "answer": "Go to the login page and click 'Forgot Password'",
            "category": "account"
        },
        {
            "question": "What is your return policy?",
            "answer": "We accept returns within 30 days of purchase",
            "category": "returns"
        }
    ],
    "policies": [
        {
            "title": "Privacy Policy",
            "content": "We protect your data...",
            "category": "legal"
        }
    ]
}
```

### Loading Custom Knowledge Base

```yaml
# config.yaml
knowledge_base:
  enabled: true
  auto_load: true
  custom_kb_file: "knowledge_base.json"
  search_limit: 5
  min_relevance_score: 0.3
```

```python
from mem_agent import MemAgent

agent = MemAgent(config_file="config.yaml")

# Knowledge base is automatically loaded
# You can also manually load
agent.load_knowledge_base("custom_kb.json")
```

### Excel/CSV Import

```python
import pandas as pd
from mem_agent import MemAgent

# Load from Excel
df = pd.read_excel("faq.xlsx")
knowledge_data = df.to_dict('records')

# Create knowledge base
kb_data = {
    "faq": knowledge_data
}

# Save as JSON
import json
with open("knowledge_base.json", "w") as f:
    json.dump(kb_data, f, indent=2)

# Load into agent
agent = MemAgent(config_file="config.yaml")
```

---

## 🎨 Custom Prompt Templates

### Creating Custom Template

```python
# custom_templates.py
from prompt_templates import PromptManager

# Add custom template
custom_template = """
You are a helpful assistant for {company_name}.
Your role is {role}.
Always be {tone}.

User: {user_message}
Assistant: 
"""

# Register template
prompt_manager = PromptManager()
prompt_manager.add_template(
    "custom_assistant",
    custom_template,
    variables=["company_name", "role", "tone"]
)
```

### Using Custom Template

```yaml
# config.yaml
prompt:
  template: "custom_assistant"
  variables:
    company_name: "TechCorp"
    role: "technical support specialist"
    tone: "professional and patient"
```

```python
from mem_agent import MemAgent

agent = MemAgent(config_file="config.yaml")
# Custom template will be used automatically
```

---

## 🚀 Production Deployment

### Docker Setup

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  mem-agent:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./memories.db:/app/memories.db
      - ./config.yaml:/app/config.yaml
    environment:
      - MEM_AGENT_MODEL=granite4:tiny-h
```

### Nginx Configuration

```nginx
# nginx.conf
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Environment Variables

```bash
# .env
MEM_AGENT_MODEL=granite4:tiny-h
MEM_AGENT_BASE_URL=http://localhost:11434
MEM_AGENT_DB_PATH=/app/data/memories.db
MEM_AGENT_LOG_LEVEL=INFO
```

### Health Check

```python
from flask import Flask, jsonify
from mem_agent import MemAgent

app = Flask(__name__)
agent = MemAgent(config_file="config.yaml")

@app.route('/health')
def health_check():
    try:
        # Test agent functionality
        agent.set_user("health_check")
        response = agent.chat("test")
        
        return jsonify({
            'status': 'healthy',
            'agent': 'working',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500
```

---

## 🔧 Advanced Integration

### Multi-Agent System

```python
from mem_agent import MemAgent

# Create multiple specialized agents
customer_service_agent = MemAgent(
    config_file="config_customer_service.yaml"
)

technical_support_agent = MemAgent(
    config_file="config_technical_support.yaml"
)

sales_agent = MemAgent(
    config_file="config_sales.yaml"
)

def route_message(user_id, message, intent):
    if intent == "customer_service":
        agent = customer_service_agent
    elif intent == "technical":
        agent = technical_support_agent
    elif intent == "sales":
        agent = sales_agent
    else:
        agent = customer_service_agent  # default
    
    agent.set_user(user_id)
    return agent.chat(message)
```

### Integration with External APIs

```python
import requests
from mem_agent import MemAgent

agent = MemAgent(config_file="config.yaml")

def enhanced_chat(user_id, message):
    # Get response from Mem-Agent
    agent.set_user(user_id)
    response = agent.chat(message)
    
    # Check if external API call is needed
    if "weather" in message.lower():
        weather_data = get_weather_data()
        response += f"\n\nCurrent weather: {weather_data}"
    
    return response

def get_weather_data():
    # External API call
    response = requests.get("https://api.weather.com/current")
    return response.json()['temperature']
```

---

## 📊 Monitoring and Analytics

### Logging Setup

```python
import logging
from mem_agent import MemAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mem_agent.log'),
        logging.StreamHandler()
    ]
)

agent = MemAgent(config_file="config.yaml")
```

### Usage Analytics

```python
from mem_agent import MemAgent
import json

agent = MemAgent(config_file="config.yaml")

def track_usage(user_id, message, response):
    # Log usage data
    usage_data = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'message_length': len(message),
        'response_length': len(response),
        'has_knowledge_base_hit': 'knowledge_base' in response.lower()
    }
    
    with open('usage_analytics.json', 'a') as f:
        f.write(json.dumps(usage_data) + '\n')
```

---

## 🔒 Security Best Practices

### Input Validation

```python
from flask import request, jsonify
import re

def validate_input(message):
    # Remove potentially harmful content
    message = re.sub(r'<script.*?</script>', '', message, flags=re.DOTALL)
    message = re.sub(r'javascript:', '', message, flags=re.IGNORECASE)
    
    # Check message length
    if len(message) > 1000:
        raise ValueError("Message too long")
    
    return message

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = validate_input(data.get('message'))
    
    # Continue with normal processing
    response = agent.chat(message)
    return jsonify({'response': response})
```

### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)

@app.route('/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    # Chat endpoint with rate limiting
    pass
```

---

## 🆘 Troubleshooting

### Common Issues

1. **"Ollama connection failed"**
   ```bash
   # Check if Ollama is running
   ollama serve
   
   # Test connection
   curl http://localhost:11434/api/tags
   ```

2. **"Model not found"**
   ```bash
   # Download model
   ollama pull granite4:tiny-h
   ```

3. **"Database locked"**
   ```python
   # Use connection pooling or restart service
   ```

### Performance Optimization

```python
# Use connection pooling
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'sqlite:///memories.db',
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

---

## 📚 Additional Resources

- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Configuration Guide**: [docs/CONFIG_GUIDE.md](docs/CONFIG_GUIDE.md)
- **Examples**: `examples/` folder
- **API Reference**: Generated from docstrings

---

**Last updated:** 2025-01-13  
**Version:** 2.0.0