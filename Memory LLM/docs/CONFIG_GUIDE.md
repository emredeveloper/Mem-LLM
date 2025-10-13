# ⚙️ Mem-Agent Yapılandırma Rehberi

Bu rehber, `config.yaml` dosyasının nasıl oluşturulacağını ve yapılandırılacağını adım adım açıklar.

## 📋 İçindekiler

1. [Hızlı Başlangıç](#hızlı-başlangıç)
2. [Temel Yapılandırma](#temel-yapılandırma)
3. [Gelişmiş Ayarlar](#gelişmiş-ayarlar)
4. [Kullanım Senaryoları](#kullanım-senaryoları)
5. [Sorun Giderme](#sorun-giderme)

---

## 🚀 Hızlı Başlangıç

### Adım 1: Config Dosyası Oluşturma

```bash
# Ana klasörde config.yaml.example dosyasını kopyalayın
cp config.yaml.example config.yaml

# Veya Windows'ta:
copy config.yaml.example config.yaml
```

### Adım 2: Temel Ayarları Düzenleme

En basit kullanım için sadece şu ayarları yapın:

```yaml
# config.yaml

usage_mode: "personal"  # veya "business"

llm:
  model: "granite4:tiny-h"
  base_url: "http://localhost:11434"

memory:
  backend: "json"
```

### Adım 3: Config'i Kullanma

```python
from mem_agent import MemAgent

# Config dosyasını kullanarak agent oluştur
agent = MemAgent(config_file="config.yaml")
```

**✅ Bu kadar! Artık kullanıma hazırsınız.**

---

## 🔧 Temel Yapılandırma

### 1. Kullanım Modu (`usage_mode`)

Agent'ın nasıl davranacağını belirler.

```yaml
usage_mode: "personal"  # veya "business"
```

| Mod | Açıklama | Ne Zaman Kullanılır |
|-----|----------|---------------------|
| `personal` | Kişisel asistan modu | Bireysel kullanım, öğrenme, hatırlatmalar |
| `business` | Kurumsal mod | Müşteri hizmetleri, çoklu kullanıcı, raporlama |

### 2. LLM Ayarları (`llm`)

Ollama model yapılandırması.

```yaml
llm:
  model: "granite4:tiny-h"        # Kullanılacak model
  base_url: "http://localhost:11434"  # Ollama API adresi
  temperature: 0.7                # Yaratıcılık (0.0-1.0)
  max_tokens: 500                 # Maksimum cevap uzunluğu
```

**Model Seçimi:**

| Model | Boyut | Hız | Önerilen Kullanım |
|-------|-------|-----|-------------------|
| `granite4:tiny-h` | Küçük | Çok Hızlı | Genel kullanım ⭐ |
| `llama3.2:3b` | Orta | Hızlı | Dengeli performans |
| `mistral:7b` | Büyük | Yavaş | Gelişmiş görevler |

**Temperature Değerleri:**

- `0.0-0.3`: Tutarlı, tahmin edilebilir cevaplar (müşteri hizmetleri)
- `0.4-0.7`: Dengeli (genel kullanım) ⭐
- `0.8-1.0`: Yaratıcı, çeşitli cevaplar (brainstorming)

### 3. Bellek Sistemi (`memory`)

Konuşmaların nasıl saklanacağını belirler.

```yaml
memory:
  backend: "json"           # "json" veya "sql"
  json_dir: "memories"      # JSON için klasör
  db_path: "memories.db"    # SQL için veritabanı
```

**Backend Karşılaştırması:**

| Özellik | JSON | SQL |
|---------|------|-----|
| Kurulum | Çok Kolay ⭐ | Kolay |
| Performans | İyi | Çok İyi ⭐ |
| Arama | Basit | Gelişmiş ⭐ |
| Bilgi Bankası | ❌ | ✅ ⭐ |
| Önerilen | Başlangıç | Production ⭐ |

### 4. Prompt Şablonu (`prompt`)

Bot'un konuşma stilini belirler.

```yaml
prompt:
  template: "personal_assistant"  # Kullanılacak şablon
  variables:
    user_name: "Ahmet"
    tone: "samimi"
```

**Mevcut Şablonlar:**

| Şablon | Kullanım Alanı |
|--------|----------------|
| `personal_assistant` | Kişisel asistan ⭐ |
| `customer_service` | Müşteri hizmetleri ⭐ |
| `tech_support` | Teknik destek |
| `sales_assistant` | Satış danışmanı |
| `education_tutor` | Eğitim asistanı |
| `health_advisor` | Sağlık bilgilendirme |
| `booking_assistant` | Rezervasyon |
| `hr_assistant` | İnsan kaynakları |

---

## 🎯 Gelişmiş Ayarlar

### Personal Mod Özellikleri

```yaml
personal:
  user_name: "Ahmet Yılmaz"
  enable_reminders: true          # Hatırlatma sistemi
  enable_personal_notes: true     # Kişisel notlar
  privacy_level: "high"           # Gizlilik seviyesi
  share_data: false               # Veri paylaşımı
```

### Business Mod Özellikleri

```yaml
business:
  company_name: "ABC Şirketi"
  departments:
    - "Müşteri Hizmetleri"
    - "Satış"
    - "Teknik Destek"
  enable_multi_user: true         # Çoklu kullanıcı
  enable_reporting: true          # Raporlama
  security_level: "high"          # Güvenlik seviyesi
```

### Bilgi Bankası Yapılandırması

```yaml
knowledge_base:
  enabled: true                   # Bilgi bankasını aktif et
  auto_load: true                 # Otomatik yükleme
  default_kb: "ecommerce"         # Varsayılan KB
  search_limit: 5                 # Arama sonuç limiti
  min_relevance_score: 0.3        # Minimum ilgililik skoru
```

**Varsayılan KB'ler:**
- `ecommerce`: E-ticaret için hazır bilgiler
- `tech_support`: Teknik destek için hazır bilgiler
- `custom`: Kendi KB'nizi yükleyin

### Güvenlik Ayarları

```yaml
security:
  filter_sensitive_data: true     # Hassas veri filtreleme
  sensitive_keywords:
    - "kredi kartı"
    - "şifre"
    - "TC kimlik"
  rate_limit:
    enabled: true
    max_requests_per_minute: 60
```

### Loglama

```yaml
logging:
  enabled: true
  level: "INFO"                   # DEBUG, INFO, WARNING, ERROR
  file: "mem_agent.log"
  max_size_mb: 10
  backup_count: 5
  log_user_messages: true
  mask_sensitive: true            # Hassas bilgileri maskele
```

---

## 💼 Kullanım Senaryoları

### Senaryo 1: Kişisel Asistan (En Basit)

```yaml
# config.yaml - Minimal setup

usage_mode: "personal"

llm:
  model: "granite4:tiny-h"

memory:
  backend: "json"
```

**Kullanım:**
```python
from mem_agent import MemAgent

agent = MemAgent(config_file="config.yaml")
agent.set_user("ahmet123", name="Ahmet")
response = agent.chat("Bugün ne yapmalıyım?")
```

### Senaryo 2: Müşteri Hizmetleri (Önerilen)

```yaml
# config.yaml - Müşteri hizmetleri için

usage_mode: "business"

llm:
  model: "granite4:tiny-h"
  temperature: 0.5              # Tutarlı cevaplar için

memory:
  backend: "sql"                # Gelişmiş arama için
  db_path: "customer_memories.db"

prompt:
  template: "customer_service"
  variables:
    company_name: "ABC Mağazası"
    tone: "profesyonel ve yardımsever"

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

### Senaryo 3: Teknik Destek

```yaml
# config.yaml - Teknik destek için

usage_mode: "business"

llm:
  model: "granite4:tiny-h"
  temperature: 0.3              # Daha teknik, tutarlı

memory:
  backend: "sql"

prompt:
  template: "tech_support"
  variables:
    product_name: "XYZ Yazılımı"
    support_level: "L1 ve L2"

knowledge_base:
  enabled: true
  default_kb: "tech_support"
  search_limit: 10              # Daha fazla sonuç

logging:
  level: "DEBUG"                # Detaylı loglama
  log_user_messages: true
```

### Senaryo 4: Eğitim Asistanı

```yaml
# config.yaml - Eğitim için

usage_mode: "personal"

llm:
  model: "granite4:tiny-h"
  temperature: 0.6              # Açıklayıcı ve yaratıcı

prompt:
  template: "education_tutor"
  variables:
    subject: "Python Programlama"
    level: "başlangıç"
    teaching_style: "adım adım"

memory:
  backend: "sql"                # Öğrenme geçmişi için
```

---

## 🔍 Sorun Giderme

### Hata: "Config dosyası bulunamadı"

**Çözüm:**
```bash
# Config dosyasının doğru yerde olduğundan emin olun
ls config.yaml

# Yoksa oluşturun
cp config.yaml.example config.yaml
```

### Hata: "Ollama bağlantısı başarısız"

**Çözüm:**
```yaml
# config.yaml - URL'yi kontrol edin
llm:
  base_url: "http://localhost:11434"  # Port numarasını kontrol edin
```

```bash
# Ollama servisini başlatın
ollama serve

# Bağlantıyı test edin
curl http://localhost:11434/api/tags
```

### Hata: "Model bulunamadı"

**Çözüm:**
```bash
# Modeli indirin
ollama pull granite4:tiny-h

# Mevcut modelleri listeleyin
ollama list

# Config'de doğru model adını kullanın
```

### Hata: "SQL veritabanı hatası"

**Çözüm:**
```yaml
# JSON'a geçiş yapın (daha basit)
memory:
  backend: "json"
  json_dir: "memories"
```

### Performans Sorunları

**Çözüm 1: Daha küçük model kullanın**
```yaml
llm:
  model: "granite4:tiny-h"  # En hızlı
```

**Çözüm 2: Token limitini düşürün**
```yaml
llm:
  max_tokens: 300  # Daha kısa cevaplar
```

**Çözüm 3: Bellek limitini ayarlayın**
```yaml
response:
  recent_conversations_limit: 3  # Daha az geçmiş
```

---

## 📚 Ek Kaynaklar

- **Hızlı Başlangıç**: [QUICKSTART_TR.md](../QUICKSTART_TR.md)
- **Entegrasyon Rehberi**: [INTEGRATION_GUIDE.md](../INTEGRATION_GUIDE.md)
- **Örnekler**: `examples/` klasörü
- **Proje Yapısı**: [STRUCTURE.md](../STRUCTURE.md)

---

## 💡 İpuçları

1. **Başlangıç için JSON kullanın**: Daha sonra SQL'e geçebilirsiniz
2. **Minimal config ile başlayın**: Sadece ihtiyacınız olanları ekleyin
3. **Temperature'ı ayarlayın**: Görevinize göre optimize edin
4. **Loglama açık tutun**: Hata ayıklama için faydalı
5. **Güvenlik ayarlarını atlayın**: Production'da mutlaka aktif edin

---

**Son güncelleme:** 2025-10-13  
**Versiyon:** 2.0.0

