```4812:5168:Memory LLM/INTEGRATION_GUIDE.md
# 🔗 Mem-Agent Entegrasyon Rehberi

Bu rehber, Mem-Agent'ı kendi sisteminize nasıl entegre edeceğinizi adım adım açıklar.

## 📋 İçindekiler

1. [Hızlı Entegrasyon](#hızlı-entegrasyon)
2. [Yapılandırma](#yapılandırma)
3. [Web API Entegrasyonu](#web-api-entegrasyonu)
4. [Database Entegrasyonu](#database-entegrasyonu)
5. [Özel Bilgi Bankası](#özel-bilgi-bankası)
6. [Özel Prompt Şablonları](#özel-prompt-şablonları)
7. [Production Deployment](#production-deployment)

---

## 🚀 Hızlı Entegrasyon

### Adım 1: Kurulum

```bash
# Gerekli paketleri yükleyin
pip install -r requirements.txt

# VEYA development modu için
pip install -e .
```

### Adım 2: Temel Kullanım

```python
from mem_agent_pro import MemAgentPro

# Agent oluştur
agent = MemAgentPro(config_file="config.yaml")

# Kullanıcı ayarla
agent.set_user("user_123", name="Ahmet")

# Sohbet et
response = agent.chat("Merhaba!")
print(response)
```

---

## ⚙️ Yapılandırma

### config.yaml Dosyası

Kendi ihtiyaçlarınıza göre düzenleyin:

```yaml
# LLM Ayarları
llm:
  model: "granite4:tiny-h"  # Modelinizi değiştirin
  base_url: "http://localhost:11434"
  temperature: 0.7
  max_tokens: 500

# Bellek Ayarları
memory:
  backend: "sql"  # "json" veya "sql"
  db_path: "my_app_memories.db"

# Prompt Şablonu
prompt:
  template: "customer_service"  # Senaryonuza uygun şablon
  variables:
    company_name: "ŞİRKETİNİZ"
    tone: "profesyonel"
```

### Ortam Değişkenleri

```bash
# .env dosyası oluşturun
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=granite4:tiny-h
DB_PATH=memories.db
LOG_LEVEL=INFO
```

Python'da kullanım:

```python
import os
from dotenv import load_dotenv

load_dotenv()

agent = MemAgentPro()
agent.llm.base_url = os.getenv("OLLAMA_URL")
```

---

## 🌐 Web API Entegrasyonu

### Flask ile REST API

```python
from flask import Flask, request, jsonify
from mem_agent_pro import MemAgentPro

app = Flask(__name__)
agent = MemAgentPro()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')
    metadata = data.get('metadata', {})
    
    if not user_id or not message:
        return jsonify({"error": "user_id ve message gerekli"}), 400
    
    try:
        response = agent.chat(message, user_id=user_id, metadata=metadata)
        return jsonify({
            "success": True,
            "response": response,
            "user_id": user_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def stats():
    return jsonify(agent.get_statistics())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### FastAPI ile Async API

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mem_agent_pro import MemAgentPro

app = FastAPI()
agent = MemAgentPro()

class ChatRequest(BaseModel):
    user_id: str
    message: str
    metadata: dict = {}

class ChatResponse(BaseModel):
    success: bool
    response: str
    user_id: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = agent.chat(
            message=request.message,
            user_id=request.user_id,
            metadata=request.metadata
        )
        return ChatResponse(
            success=True,
            response=response,
            user_id=request.user_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    return agent.get_statistics()

# Uvicorn ile çalıştırın:
# uvicorn api_server:app --host 0.0.0.0 --port 8000
```

---

## 💾 Database Entegrasyonu

### Mevcut PostgreSQL Veritabanınızla

```python
import psycopg2
from mem_agent_pro import MemAgentPro

class PostgreSQLMemoryAdapter:
    """Mevcut PostgreSQL'i Mem-Agent ile kullan"""
    
    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)
        self.agent = MemAgentPro()
    
    def sync_user_to_agent(self, user_id):
        """Kullanıcıyı kendi DB'nizden agent'a senkronize edin"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT user_id, name, email, preferences
            FROM users WHERE user_id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        if user:
            self.agent.set_user(user[0], name=user[1])
            self.agent.update_profile({
                "email": user[2],
                "preferences": user[3]
            })
    
    def chat_with_sync(self, user_id, message):
        """Sohbet et ve her iki DB'ye kaydet"""
        self.sync_user_to_agent(user_id)
        response = self.agent.chat(message, user_id=user_id)
        
        # Kendi DB'nize de kaydedin
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO chat_history (user_id, message, response, timestamp)
            VALUES (%s, %s, %s, NOW())
        """, (user_id, message, response))
        self.conn.commit()
        
        return response

# Kullanım
adapter = PostgreSQLMemoryAdapter("postgresql://user:pass@localhost/mydb")
response = adapter.chat_with_sync("user123", "Merhaba")
```

---

## 📚 Özel Bilgi Bankası

### JSON Dosyasından Yükleme

```python
# knowledge_base/my_kb.json
{
  "knowledge_base": [
    {
      "category": "ürün",
      "question": "X ürünü ne zaman stoğa girer?",
      "answer": "X ürünü önümüzdeki hafta stoklarımızda olacak.",
      "keywords": ["X ürün", "stok", "bekleme"],
      "priority": 10
    }
  ]
}
```

```python
from mem_agent_pro import MemAgentPro
from knowledge_loader import KnowledgeLoader

agent = MemAgentPro()
loader = KnowledgeLoader(agent.memory)

# JSON'dan yükle
count = loader.load_from_json("knowledge_base/my_kb.json")
print(f"{count} kayıt yüklendi")
```

### Programatik Olarak Ekleme

```python
# Toplu bilgi ekleme
knowledge_entries = [
    {
        "category": "destek",
        "question": "Canlı destek saatleri",
        "answer": "Canlı destek haftaiçi 09:00-18:00 arası hizmet vermektedir.",
        "keywords": ["destek", "saat", "canlı"],
        "priority": 8
    },
    # ... daha fazla kayıt
]

for entry in knowledge_entries:
    agent.add_knowledge(**entry)
```

### Excel'den İçe Aktarma

```python
import pandas as pd

def import_from_excel(agent, excel_file):
    """Excel'den bilgi bankası içe aktar"""
    df = pd.read_excel(excel_file)
    
    for _, row in df.iterrows():
        agent.add_knowledge(
            category=row['Kategori'],
            question=row['Soru'],
            answer=row['Cevap'],
            keywords=row['Anahtar Kelimeler'].split(','),
            priority=int(row.get('Öncelik', 0))
        )

# Kullanım
import_from_excel(agent, "bilgi_bankasi.xlsx")
```

---

## 🎨 Özel Prompt Şablonları

### Yeni Şablon Oluşturma

```python
from prompt_templates import prompt_manager

# Özel şablon ekle
prompt_manager.add_template(
    name="otel_resepsiyon",
    base_prompt="""Sen {hotel_name} otelinin resepsiyon görevlisisin.

Görevlerin:
- Misafirleri karşılamak
- Rezervasyon işlemleri
- Otel hizmetleri hakkında bilgi vermek
- Özel istekleri kaydetmek

Otel Özellikleri:
- Yıldız: {stars}
- Odalar: {room_count}
- Özel Hizmetler: {services}

İletişim tarzı: {tone}

Her misafir için:
1. Samimi karşılama
2. İhtiyaçları dinle
3. Uygun çözüm sun
4. Rezervasyon detaylarını kaydet
""",
    variables={
        "hotel_name": "Grand Hotel",
        "stars": "5 yıldız",
        "room_count": "200",
        "services": "Spa, Restaurant, Pool",
        "tone": "profesyonel ve misafirperver"
    }
)

# Kullan
agent = MemAgentPro()
agent.change_prompt_template(
    "otel_resepsiyon",
    hotel_name="İstanbul Palace Hotel"
)
```

### Runtime'da Prompt Özelleştirme

```python
def dynamic_prompt(user_type, language):
    """Kullanıcı tipine göre dinamik prompt"""
    
    if user_type == "vip":
        return f"""Sen premium müşteri danışmanısın.
        Dil: {language}
        Yaklaşım: VIP müşterilere özel, öncelikli hizmet
        Cevap Detayı: Çok detaylı
        """
    else:
        return f"""Sen müşteri hizmetleri asistanısın.
        Dil: {language}
        Yaklaşım: Standart, yardımsever
        Cevap Detayı: Normal
        """

# Kullanım
agent = MemAgentPro()
agent.system_prompt = dynamic_prompt("vip", "Türkçe")
```

---

## 🚀 Production Deployment

### Docker ile Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Ollama kurun (veya ayrı container kullanın)
RUN apt-get update && apt-get install -y curl
RUN curl https://ollama.ai/install.sh | sh

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY . .

# Model indirin
RUN ollama serve & sleep 5 && ollama pull granite4:tiny-h

EXPOSE 5000

CMD ["python", "api_server.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
  
  mem-agent:
    build: .
    depends_on:
      - ollama
    environment:
      - OLLAMA_URL=http://ollama:11434
      - DB_PATH=/data/memories.db
    volumes:
      - agent_data:/data
    ports:
      - "5000:5000"

volumes:
  ollama_data:
  agent_data:
```

### Systemd Service (Linux)

```ini
# /etc/systemd/system/mem-agent.service
[Unit]
Description=Mem-Agent Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/mem-agent
Environment="OLLAMA_URL=http://localhost:11434"
ExecStart=/usr/bin/python3 /opt/mem-agent/api_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable mem-agent
sudo systemctl start mem-agent
sudo systemctl status mem-agent
```

### Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/mem-agent
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://localhost:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 🔒 Güvenlik Best Practices

### 1. API Key Authentication

```python
from functools import wraps
from flask import request, jsonify

API_KEYS = {"your-secret-key": "client1"}

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key not in API_KEYS:
            return jsonify({"error": "Invalid API key"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/chat', methods=['POST'])
@require_api_key
def chat():
    # ... kod
```

### 2. Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    # ... kod
```

### 3. Input Validation

```python
def sanitize_input(text, max_length=1000):
    """Kullanıcı girdisini temizle"""
    # Maksimum uzunluk kontrolü
    text = text[:max_length]
    
    # Tehlikeli karakterleri temizle
    dangerous_chars = ['<script>', '</script>', '<iframe>']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()

# Kullanım
message = sanitize_input(request.json.get('message'))
```

---

## 📊 Monitoring ve Logging

### Prometheus Metrikleri

```python
from prometheus_client import Counter, Histogram, generate_latest

chat_requests = Counter('chat_requests_total', 'Total chat requests')
chat_duration = Histogram('chat_duration_seconds', 'Chat response time')

@app.route('/api/chat', methods=['POST'])
def chat():
    chat_requests.inc()
    with chat_duration.time():
        response = agent.chat(message, user_id=user_id)
    return jsonify({"response": response})

@app.route('/metrics')
def metrics():
    return generate_latest()
```

---

## 🎯 Use Case Örnekleri

### E-ticaret Chatbot

```python
# config.yaml
prompt:
  template: "sales_assistant"
  variables:
    store_name: "TechMarket"
    product_categories: "Elektronik, Bilgisayar, Telefon"

knowledge_base:
  default_kb: "ecommerce"
```

### Teknik Destek

```python
# config.yaml
prompt:
  template: "tech_support"
  variables:
    product_name: "MyApp Pro"
    user_level: "tüm seviyeler"

knowledge_base:
  default_kb: "tech_support"
  custom_kb_file: "kb/technical_faq.json"
```

---

## 🐛 Troubleshooting

### Yaygın Sorunlar

1. **"Connection refused" hatası**
   ```bash
   # Ollama'yı başlatın
   ollama serve
   ```

2. **Model bulunamadı**
   ```bash
   ollama pull granite4:tiny-h
   ```

3. **Database lock**
   ```python
   # SQLite için thread-safe kullanım
   memory = SQLMemoryManager(db_path, check_same_thread=False)
   ```

---

## 📞 Destek

- 📖 [Tam Dokümantasyon](README.md)
- 🐛 [Issue Tracker](https://github.com/yourusername/mem-agent/issues)
- 💬 [Discussions](https://github.com/yourusername/mem-agent/discussions)

---

**Başarılar!** 🎉
```

