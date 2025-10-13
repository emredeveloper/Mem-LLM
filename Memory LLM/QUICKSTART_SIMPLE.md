# 🚀 Mem-LLM - 5 Dakikada Başlangıç

## 1️⃣ Kurulum

```bash
pip install mem-llm
```

## 2️⃣ Ollama'yı Çalıştırın

```bash
ollama serve
ollama pull llama2  # veya granite4:tiny-h
```

## 3️⃣ İlk Kodunuz

```python
from mem_llm import MemAgent

# Agent oluştur
agent = MemAgent(model="llama2")

# Kullanıcı seç
agent.set_user("john123")

# İlk sohbet
response = agent.chat("Hello! My name is John.")
print(response)

# İkinci sohbet - Hatırlıyor!
response = agent.chat("What's my name?")
print(response)  # "Your name is John!"
```

## 4️⃣ Parametreler

```python
agent = MemAgent(
    model="llama2",                      # Ollama model adı
    use_sql=False,                       # JSON kullan (basit)
    memory_dir="my_memories",            # Hafıza klasörü
    ollama_url="http://localhost:11434" # Ollama URL
)
```

## 5️⃣ Kullanışlı Metodlar

```python
# Sistem kontrolü
status = agent.check_setup()
if status['status'] == 'ready':
    print("✅ Hazır!")

# Kullanıcı değiştir
agent.set_user("alice456", name="Alice")

# Sohbet
response = agent.chat("How can you help me?")

# Metadata ekle
response = agent.chat(
    "My order #12345 is delayed",
    metadata={"order_id": "#12345", "issue": "delay"}
)

# Hafızayı kontrol et
memories = agent.memory.load_memory("john123")
print(f"John'un {len(memories['conversations'])} konuşması var")
```

## 6️⃣ SQL Veritabanı (İleri Seviye)

```python
agent = MemAgent(
    model="llama2",
    use_sql=True,  # SQL kullan
    memory_dir="memories"
)
```

## 🎯 Örnek Senaryolar

### Müşteri Hizmetleri

```python
from mem_llm import MemAgent

agent = MemAgent(model="llama2")

# Müşteri 1
agent.set_user("customer_001")
agent.chat("My product hasn't arrived yet")

# Müşteri 2 - Farklı hafıza
agent.set_user("customer_002")
agent.chat("I want to return my order")
```

### Kişisel Asistan

```python
agent = MemAgent(model="llama2")
agent.set_user("emre")

agent.chat("Remind me to call John tomorrow")
agent.chat("What's my schedule for tomorrow?")
```

## 📚 Daha Fazla

- [Full Documentation](./README.md)
- [API Reference](./docs/CONFIG_GUIDE.md)
- [Examples](./examples/)

## 🐛 Sorun Çözme

### Ollama bağlanamıyor?
```bash
ollama serve  # Terminalde çalıştırın
```

### Model yok?
```bash
ollama list  # Mevcut modelleri listele
ollama pull llama2  # Model indir
```

### Hafıza çalışmıyor?
```python
# JSON modu (basit)
agent = MemAgent(use_sql=False)

# Hafızayı kontrol et
memories = agent.memory.load_memory("user_id")
print(memories)
```

---

**Hızlı linkler:**
- 🌐 PyPI: https://pypi.org/project/mem-llm/
- 📦 GitHub: https://github.com/emredeveloper/Mem-LLM
- 🐛 Issues: https://github.com/emredeveloper/Mem-LLM/issues

