"""
Setup script for Mem-Agent package
"""

from setuptools import setup, find_packages
from pathlib import Path

# README dosyasını oku
this_directory = Path(__file__).parent
long_description = """
# Mem-Agent: Belleği Olan Mini Asistan

Sadece 4 milyar parametreli yerel bir LLM ile çalışan, kullanıcı etkileşimlerini hatırlayan ve bağlam farkındalığı ile cevap veren yapay zeka asistanı.

## Özellikler

- 🧠 **Bellek Yönetimi**: Kullanıcı etkileşimlerini otomatik kaydeder ve hatırlar
- 🏠 **Tamamen Yerel**: Ollama ile local çalışır, veri gizliliği
- 🚀 **Hafif Model**: granite4:tiny-h (4B parametre) ile hızlı yanıt
- 💾 **JSON Tabanlı Depolama**: Basit ve taşınabilir bellek sistemi
- 🔍 **Arama & Filtreleme**: Geçmiş konuşmalarda arama yapabilme
- 📊 **İstatistikler**: Kullanıcı etkileşim analizi

## Kurulum

```bash
pip install -e .
```

## Hızlı Başlangıç

```python
from mem_agent import MemAgent

# Agent oluştur
agent = MemAgent(model="granite4:tiny-h")

# Kullanıcı ile sohbet et
agent.set_user("user123")
response = agent.chat("Merhaba, benim adım Ali")
print(response)

# Beni hatırlıyor mu?
response = agent.chat("Adımı hatırlıyor musun?")
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
    description="Belleği olan mini asistan - 4B parametreli LLM ile kullanıcı etkileşimlerini hatırlayan yapay zeka",
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

