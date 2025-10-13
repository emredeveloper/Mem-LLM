# 📚 Mem-Agent Dokümantasyon İndeksi

Bu klasör Mem-Agent'ın dokümantasyon merkezi olarak hizmet eder.

## 📖 Ana Dokümantasyon

### Kök Klasördeki Dosyalar

Ana dokümantasyon dosyaları proje kök klasöründe bulunur:

1. **[README_UPDATED.md](../README_UPDATED.md)** - Ana README dosyası
   - Projeye genel bakış
   - Özellikler
   - Kurulum talimatları
   - Temel kullanım

2. **[QUICKSTART_TR.md](../QUICKSTART_TR.md)** - Hızlı Başlangıç Kılavuzu (Türkçe)
   - 5 dakikada başlangıç
   - Adım adım kurulum
   - İlk örnekler

3. **[INTEGRATION_GUIDE.md](../INTEGRATION_GUIDE.md)** - Entegrasyon Rehberi
   - Web API entegrasyonu
   - Database bağlantıları
   - Production deployment
   - Özel yapılandırmalar

3.5. **[docs/CONFIG_GUIDE.md](CONFIG_GUIDE.md)** - Yapılandırma Rehberi ⭐ YENİ
   - Config dosyası nasıl oluşturulur
   - Tüm ayarlar detaylı açıklanmış
   - Kullanım senaryolarına göre örnekler
   - Sorun giderme

4. **[CHANGELOG.md](../CHANGELOG.md)** - Değişiklik Günlüğü
   - Versiyon geçmişi
   - Yeni özellikler
   - Hata düzeltmeleri

5. **[LICENSE](../LICENSE)** - Lisans Dosyası
   - MIT License

## 🎯 Kullanım Örnekleri

Örnek kodlar `../examples/` klasöründe bulunur:

- **example_simple.py** - Basit başlangıç örneği
- **example_business_mode.py** - Kurumsal kullanım
- **example_personal_mode.py** - Kişisel asistan
- **example_customer_service.py** - Müşteri hizmetleri
- **example_memory_tools.py** - Bellek araçları
- **demo_user_tools.py** - Kullanıcı araçları demosu

## 🧪 Test Dosyaları

Test dosyaları `../tests/` klasöründe:

- **test_mem_agent.py** - MemAgent testleri
- **test_integration.py** - Entegrasyon testleri
- **test_memory_manager.py** - Bellek yöneticisi testleri
- **test_memory_tools.py** - Araçlar testleri
- **test_llm_client.py** - LLM istemcisi testleri

## 📦 Yapılandırma

- **[config.yaml](../config.yaml)** - Mevcut yapılandırma dosyası
- **[config.yaml.example](../config.yaml.example)** - Örnek config şablonu ⭐ YENİ
- **[docs/CONFIG_GUIDE.md](CONFIG_GUIDE.md)** - Detaylı config rehberi ⭐ YENİ
- **[requirements.txt](../requirements.txt)** - Python bağımlılıkları
- **[setup.py](../setup.py)** - Kurulum scripti

## 🔧 Core Modüller

Ana modüller kök klasörde:

- `mem_agent.py` - Ana agent sınıfı
- `memory_manager.py` - JSON bellek yöneticisi
- `memory_db.py` - SQL bellek yöneticisi
- `memory_tools.py` - Kullanıcı araçları
- `llm_client.py` - LLM bağlantısı
- `prompt_templates.py` - Prompt şablonları
- `config_manager.py` - Yapılandırma yöneticisi
- `knowledge_loader.py` - Bilgi bankası yükleyici

## 🌟 Başlangıç İçin Önerilen Okuma Sırası

1. **[QUICKSTART_TR.md](../QUICKSTART_TR.md)** - İlk 5 dakika
2. **[config.yaml.example](../config.yaml.example)** - Config dosyası hazırlama ⭐
3. **[examples/example_simple.py](../examples/example_simple.py)** - İlk kod örneği
4. **[docs/CONFIG_GUIDE.md](CONFIG_GUIDE.md)** - Detaylı yapılandırma
5. **[README_UPDATED.md](../README_UPDATED.md)** - Tüm özellikler
6. **[INTEGRATION_GUIDE.md](../INTEGRATION_GUIDE.md)** - Kendi projenize entegre etme

## 💡 Yardım ve Destek

Sorularınız için:
- GitHub Issues: Hata raporları ve özellik istekleri
- Dokümantasyon: Yukarıdaki dosyalar
- Örnekler: `examples/` klasörü

---

Son güncelleme: 2025-10-13
Versiyon: 2.0.0

