# 🧠 Mem-Agent v2.0: Production-Ready Belleği Olan Mini Asistan

**Sadece 4 milyar parametreli** yerel bir LLM ile çalışan, **SQL veritabanı**, **özelleştirilebilir prompt şablonları** ve **bilgi bankası** desteği ile production-ready yapay zeka asistanı.

## 🆕 Yeni Özellikler (v2.0)

| Özellik | Açıklama |
|---------|----------|
| 💾 **SQL Desteği** | SQLite ile kalıcı, ölçeklenebilir bellek sistemi |
| 🎨 **Prompt Şablonları** | 8+ hazır senaryo şablonu (müşteri hizmetleri, teknik destek, satış vb.) |
| 📚 **Bilgi Bankası** | Önceden tanımlı problem/çözüm veritabanı |
| ⚙️ **YAML Config** | Kolayca yapılandırılabilir ayarlar |
| 🔌 **API Entegrasyonu** | Flask/FastAPI örnekleri hazır |
| 🐳 **Docker Desteği** | Production deployment rehberi |
| 📊 **Analytics** | Detaylı istatistikler ve raporlama |

## 🎯 Ne Yapıyor?

Küçük bir LLM modeli (4B parametre) kullanarak:
- ✅ Kullanıcı etkileşimlerini **SQL veritabanında** saklar
- ✅ Geçmiş konuşmaları hatırlar ve bağlam oluşturur
- ✅ **Bilgi bankasından** otomatik cevap arar
- ✅ Senaryoya göre **özelleştirilebilir** davranır
- ✅ Tamamen **local** çalışır (veri gizliliği)

## 📦 Kurulum

### 1. Gereksinimler

```bash
# Ollama kurulumu
# Windows: https://ollama.ai/download/windows
# Mac: brew install ollama
# Linux: curl https://ollama.ai/install.sh | sh

# Ollama başlat
ollama serve

# Model indir (yeni terminalde)
ollama pull granite4:tiny-h
```

### 2. Python Paketleri

```bash
cd "Memory LLM"
pip install -r requirements.txt
```

## 🚀 Hızlı Başlangıç

### Basit Kullanım (JSON Bellek)

```python
from mem_agent import MemAgent

agent = MemAgent(model="granite4:tiny-h")
agent.set_user("user123")

response = agent.chat("Merhaba, benim adım Ali")
print(response)

# Beni hatırlıyor!
response = agent.chat("Adımı hatırlıyor musun?")
print(response)  # "Evet, adınız Ali"
```

### Production Kullanım (SQL + Config + KB)

```python
from mem_agent_pro import MemAgentPro

# config.yaml'dan ayarları oku
agent = MemAgentPro()

# Sistem kontrolü
status = agent.check_setup()
print(status)

# Kullanıcı sohbeti
agent.set_user("ahmet123", name="Ahmet")
response = agent.chat(
    "Siparişim nerede?",
    metadata={"order": "#12345"}
)
print(response)
```

## ⚙️ Yapılandırma (config.yaml)

```yaml
# Model ayarları
llm:
  model: "granite4:tiny-h"
  temperature: 0.7

# Bellek: SQL veya JSON
memory:
  backend: "sql"  # "json" veya "sql"
  db_path: "memories.db"

# Prompt şablonu seç
prompt:
  template: "customer_service"  # 8+ şablon mevcut
  variables:
    company_name: "ŞİRKETİNİZ"
    tone: "profesyonel"

# Bilgi bankası
knowledge_base:
  enabled: true
  default_kb: "ecommerce"  # veya "tech_support"
  custom_kb_file: "my_knowledge.json"  # Kendi KB'nizi ekleyin
```

## 📚 Mevcut Prompt Şablonları

1. **customer_service** - Müşteri hizmetleri
2. **tech_support** - Teknik destek
3. **sales_assistant** - Satış danışmanı
4. **education_tutor** - Eğitim asistanı
5. **health_advisor** - Sağlık bilgilendirme
6. **personal_assistant** - Kişisel asistan
7. **booking_assistant** - Rezervasyon sistemi
8. **hr_assistant** - İK asistanı

Kullanım:

```python
agent = MemAgentPro()

# Şablon değiştir
agent.change_prompt_template(
    "tech_support",
    product_name="MyApp",
    user_level="ileri"
)
```

## 💾 Bilgi Bankası

### Hazır Bilgi Bankaları

```python
# E-ticaret (kargo, iade, ödeme vb.)
agent = MemAgentPro()  # config.yaml'da default_kb: "ecommerce"

# Teknik destek
# config.yaml'da default_kb: "tech_support"
```

### Kendi Bilginizi Ekleyin

```python
# Programatik olarak
agent.add_knowledge(
    category="promosyon",
    question="Hangi kampanyalar var?",
    answer="%20 indirim kampanyamız devam ediyor.",
    keywords=["kampanya", "indirim"],
    priority=10
)

# JSON dosyasından
from knowledge_loader import KnowledgeLoader

loader = KnowledgeLoader(agent.memory)
loader.load_from_json("my_knowledge.json")
```

JSON Format:

```json
{
  "knowledge_base": [
    {
      "category": "kargo",
      "question": "Kargo ne zaman gelir?",
      "answer": "3-5 iş günü içinde teslim edilir.",
      "keywords": ["kargo", "teslimat"],
      "priority": 10
    }
  ]
}
```

## 🔌 API Entegrasyonu

### Flask REST API

```python
from flask import Flask, request, jsonify
from mem_agent_pro import MemAgentPro

app = Flask(__name__)
agent = MemAgentPro()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    response = agent.chat(
        message=data['message'],
        user_id=data['user_id']
    )
    return jsonify({"response": response})

app.run(port=5000)
```

Kullanım:

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "123", "message": "Merhaba"}'
```

## 🏗️ Proje Yapısı

```
Memory LLM/
├── Core (Basit Versiyon)
│   ├── mem_agent.py          # Basit agent (JSON bellek)
│   ├── memory_manager.py     # JSON bellek yöneticisi
│   └── llm_client.py          # Ollama istemcisi
│
├── Pro (Production)
│   ├── mem_agent_pro.py       # Gelişmiş agent
│   ├── memory_db.py           # SQL bellek yöneticisi
│   ├── prompt_templates.py    # 8+ prompt şablonu
│   ├── knowledge_loader.py    # Bilgi bankası yükleyici
│   └── config_manager.py      # YAML config yönetimi
│
├── Örnekler
│   ├── example_simple.py      # Basit örnek
│   ├── example_customer_service.py
│   └── example_pro_usage.py   # Pro özellikler
│
├── Config & Docs
│   ├── config.yaml            # Ana yapılandırma
│   ├── README.md              # Ana dokümantasyon
│   ├── INTEGRATION_GUIDE.md   # Entegrasyon rehberi
│   └── QUICKSTART_TR.md       # Hızlı başlangıç
│
└── Package
    ├── setup.py               # PyPI kurulum
    ├── requirements.txt       # Bağımlılıklar
    └── __init__.py            # Paket init
```

## 🎯 Kullanım Senaryoları

### 1. E-ticaret Müşteri Hizmetleri

```yaml
# config.yaml
prompt:
  template: "customer_service"
  variables:
    company_name: "TechStore"
knowledge_base:
  default_kb: "ecommerce"
```

### 2. SaaS Teknik Destek

```yaml
# config.yaml
prompt:
  template: "tech_support"
  variables:
    product_name: "MyApp Pro"
knowledge_base:
  default_kb: "tech_support"
  custom_kb_file: "technical_faq.json"
```

### 3. Otel Rezervasyon

```yaml
# config.yaml
prompt:
  template: "booking_assistant"
  variables:
    business_name: "Grand Hotel"
```

## 📊 SQL Veritabanı Şeması

```sql
-- Kullanıcılar
users (user_id, name, first_seen, last_interaction, preferences, summary)

-- Konuşmalar
conversations (id, user_id, timestamp, user_message, bot_response, metadata, resolved)

-- Bilgi Bankası
knowledge_base (id, category, question, answer, keywords, priority, active)

-- Senaryo Şablonları
scenario_templates (id, name, description, system_prompt, example_interactions)
```

## 🐳 Production Deployment

### Docker Compose

```yaml
version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
  
  mem-agent:
    build: .
    depends_on:
      - ollama
    environment:
      - OLLAMA_URL=http://ollama:11434
    ports:
      - "5000:5000"
```

### Systemd Service

```bash
sudo systemctl enable mem-agent
sudo systemctl start mem-agent
```

Detaylar için: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)

## 📈 Performans

| Metrik | Değer |
|--------|-------|
| Model Boyutu | ~2.5 GB |
| Yanıt Süresi | 1-3 saniye |
| RAM Kullanımı | 4-6 GB |
| Eş Zamanlı Kullanıcı | 10-50+ |
| Disk/Kullanıcı | 10-50 KB |

## 🔒 Güvenlik ve Gizlilik

- ✅ Tamamen yerel (internet gerektirmez)
- ✅ Veriler bilgisayarınızda
- ✅ Üçüncü parti servis yok
- ✅ KVKK uyumlu
- ✅ Hassas veri filtreleme (config.yaml)

## 🏠/🏢 Çift Mod Sistemi: Personal & Business

Mem-Agent artık hem bireysel kullanıcılar hem de şirketler için optimize edilmiş **iki farklı kullanım modu** sunuyor!

### 🎯 Kullanım Modları

| Mod | Hedef Kitle | Özellikler | Örnek Kullanım |
|-----|-------------|-----------|----------------|
| **Personal** 🏠 | Bireysel kullanıcılar | Kişisel asistan, öğrenme, finans | Günlük hayat yönetimi |
| **Business** 🏢 | Şirketler & Kurumlar | Kurumsal destek, SLA, güvenlik | Müşteri hizmetleri, iç iletişim |

### ⚙️ Yapılandırma

**config.yaml dosyasında modu seçin:**

```yaml
# Personal mod için
usage_mode: "personal"
personal:
  user_name: "Ahmet Yılmaz"
  enable_reminders: true
  privacy_level: "high"

# Business mod için
usage_mode: "business"
business:
  company_name: "TechCorp"
  enable_multi_user: true
  security_level: "high"
```

### 📋 Personal Mod Özellikleri

| Özellik | Açıklama |
|---------|----------|
| **Kişisel Asistan** | Günlük planlama ve hatırlatıcılar |
| **Öğrenme Asistanı** | Kişiselleştirilmiş öğrenme önerileri |
| **Finans Asistanı** | Bütçe ve yatırım danışmanlığı |
| **Sağlık Takibi** | Wellness ve sağlık hatırlatmaları |
| **Özel Notlar** | Kişisel anı ve bilgi saklama |

**Kullanım Örneği:**
```python
from mem_agent import MemAgent

agent = MemAgent(
    config_file="config.yaml",  # usage_mode: "personal"
    use_sql=True
)

agent.set_user("ahmet", name="Ahmet Yılmaz")
response = agent.chat("Yarın için bir hatırlatma ayarla")
```

### 🏢 Business Mod Özellikleri

| Özellik | Açıklama |
|---------|----------|
| **Kurumsal Destek** | SLA tabanlı müşteri hizmetleri |
| **Teknik Destek** | 7/24 sistem desteği |
| **İç İletişim** | Çalışan duyuru ve koordinasyon |
| **Çoklu Kanal** | Slack, Teams entegrasyonu |
| **Raporlama** | Kullanım analitiği ve raporlar |
| **Güvenlik** | Kurumsal güvenlik standartları |

**Kullanım Örneği:**
```python
from mem_agent import MemAgent

agent = MemAgent(
    config_file="config.yaml",  # usage_mode: "business"
    use_sql=True,
    load_knowledge_base=True
)

agent.set_user("customer_123", name="Şirket Müşterisi")
response = agent.chat("Şirketimiz için SLA süreniz nedir?")
```

## 🛠️ Kullanıcı Araçları Sistemi

Mem-Agent artık kullanıcıların kendi verilerini yönetebilmesi için güçlü araçlar sunuyor!

### Kullanılabilir Araçlar

| Araç | Açıklama | Örnek Kullanım |
|------|----------|----------------|
| **list_memories** | Geçmiş konuşmaları listeler | "Geçmiş konuşmalarımı göster" |
| **search_memories** | Konuşmalarda arama yapar | "laptop kelimesi geçen konuşmalarımı ara" |
| **show_user_info** | Kullanıcı bilgilerini gösterir | "Hakkımda ne biliyorsun?" |
| **export_memories** | Verileri dışa aktarır | "Verilerimi dışa aktar" |
| **clear_all_memories** | Tüm verileri siler | "Tüm verilerimi sil" |
| **delete_memory** | Belirli konuşmayı siler | "Şu konuşmayı sil" |

### Kullanım Örneği

```python
from mem_agent import MemAgent

agent = MemAgent()
agent.set_user("ahmet123")

# Kullanıcı araç komutu verebilir
response = agent.chat("Geçmiş konuşmalarımı göster")
print(response)  # Tüm konuşmaları listeler

response = agent.chat("laptop hakkında ne konuşmuştuk?")
print(response)  # İlgili konuşmaları bulur

response = agent.chat("Tüm verilerimi sil")
print(response)  # Güvenlik onayı ister
```

### Güvenlik Özellikleri

- ✅ Tüm silme işlemleri onay gerektirir
- ✅ Hassas veriler filtrelenir
- ✅ İşlem logları tutulur
- ✅ Kullanıcı doğrulaması yapılır

## 📚 Dokümantasyon

- 📖 [Tam Dokümantasyon](README.md) - Bu dosya
- ⚡ [Hızlı Başlangıç](QUICKSTART_TR.md) - 5 dakikada başlayın
- 🔌 [Entegrasyon Rehberi](INTEGRATION_GUIDE.md) - API, Docker, DB entegrasyonu
- 🛠️ [Araçlar Örneği](example_memory_tools.py) - Kullanıcı araçları demo
- 💻 [Örnek Kodlar](examples/) - Çalışan örnekler

## 🆚 Versiyon Karşılaştırması

| Özellik | Basic (v1) | Pro (v2) |
|---------|------------|----------|
| Bellek | JSON | JSON + SQL |
| Prompt | Sabit | 8+ Şablon |
| Bilgi Bankası | ❌ | ✅ |
| Config Dosyası | ❌ | ✅ YAML |
| API Örnekleri | ❌ | ✅ |
| Production Ready | ❌ | ✅ |

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch: `git checkout -b feature/amazing`
3. Commit: `git commit -m 'feat: Add feature'`
4. Push: `git push origin feature/amazing`
5. Pull Request açın

## 📝 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

- [Ollama](https://ollama.ai/) - Yerel LLM
- [IBM Granite](https://www.ibm.com/granite) - Model

## 📞 Destek

- 🐛 [Issues](https://github.com/yourusername/mem-agent/issues)
- 💬 [Discussions](https://github.com/yourusername/mem-agent/discussions)

---

**⭐ Beğendiyseniz yıldız vermeyi unutmayın!**

Made with ❤️ by C. Emre Karataş

