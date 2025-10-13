"""
Setup script for Mem-Agent package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
this_directory = Path(__file__).parent
long_description = """
# Mem-Agent: Memory-Enabled Mini Assistant

An AI assistant that works with a local 4-billion parameter LLM, remembers user interactions and responds with context awareness.

## Features

- 🧠 **Memory Management**: Automatically saves and remembers user interactions
- 🏠 **Fully Local**: Works locally with Ollama, data privacy
- 🚀 **Lightweight Model**: Fast response with granite4:tiny-h (4B parameters)
- 💾 **JSON-Based Storage**: Simple and portable memory system
- 🔍 **Search & Filter**: Search through conversation history
- 📊 **Statistics**: User interaction analysis

## Kurulum

```bash
pip install -e .
```

## Quick Start

```python
from mem_agent import MemAgent

# Create agent
agent = MemAgent(model="granite4:tiny-h")

# Chat with user
agent.set_user("user123")
response = agent.chat("Hello, my name is Ali")
print(response)

# Does it remember me?
response = agent.chat("Do you remember my name?")
print(response)
```

## Gereksinimler

- Python 3.8+
- Ollama (yerel LLM sunucusu)
- granite4:tiny-h modeli

## Lisans

MIT License
"""

setup(
    name="mem-agent",
    version="1.0.0",
    author="Emre",
    description="Memory-enabled mini assistant - AI that remembers user interactions with 4B parameter LLM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mem-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mem-agent-demo=example_simple:main",
            "mem-agent-customer=example_customer_service:simulate_customer_service",
        ],
    },
    include_package_data=True,
    keywords="llm ai memory agent chatbot ollama local",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/mem-agent/issues",
        "Source": "https://github.com/yourusername/mem-agent",
    },
)

