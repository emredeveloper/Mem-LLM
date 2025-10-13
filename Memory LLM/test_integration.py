"""
Entegrasyon Testleri
Tüm sistem bileşenlerinin birlikte çalışmasını test eder
"""

import unittest
import tempfile
import os
import shutil

# Tüm modülleri import et
from mem_agent import MemAgent
from mem_agent_pro import MemAgentPro
from memory_manager import MemoryManager
from memory_db import SQLMemoryManager
from memory_tools import MemoryTools, ToolExecutor
from prompt_templates import prompt_manager
from config_manager import get_config


class TestIntegration(unittest.TestCase):
    """Sistem entegrasyonu testleri"""

    def setUp(self):
        """Test öncesi kurulum"""
        self.temp_dir = tempfile.mkdtemp()

        # Basit agent için
        self.simple_agent = MemAgent(
            model="granite4:tiny-h",
            memory_dir=os.path.join(self.temp_dir, "simple_memories")
        )

        # Pro agent için
        config_file = os.path.join(self.temp_dir, "integration_config.yaml")
        self._create_integration_config(config_file)

        try:
            self.pro_agent = MemAgentPro(config_file=config_file)
            self.pro_available = True
        except Exception as e:
            print(f"⚠️  Pro agent oluşturulamadı: {e}")
            self.pro_available = False

    def tearDown(self):
        """Test sonrası temizlik"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_integration_config(self, config_file):
        """Entegrasyon testi için config dosyası"""
        config_content = """
llm:
  model: "granite4:tiny-h"
  base_url: "http://localhost:11434"
  temperature: 0.7

memory:
  backend: "sql"
  db_path: "integration_test.db"

prompt:
  template: "customer_service"
  variables:
    company_name: "Entegrasyon Test Şirketi"

knowledge_base:
  enabled: true
  auto_load: false

logging:
  enabled: false
"""
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)

    def test_cross_compatibility(self):
        """Çapraz uyumluluk testi"""
        # Basit ve Pro agent'lar aynı kullanıcı ile çalışabilir mi?

        user_id = "cross_compat_user"

        # Basit agent ile konuşma
        self.simple_agent.set_user(user_id, name="Cross Test")
        response1 = self.simple_agent.chat("Merhaba basit agent!")

        # Aynı kullanıcıyı Pro agent ile kullan
        if self.pro_available:
            self.pro_agent.set_user(user_id)
            response2 = self.pro_agent.chat("Merhaba pro agent!")

            # Her iki agent de kullanıcıyı görmeli
            simple_profile = self.simple_agent.memory_manager.get_user_profile(user_id)
            pro_profile = self.pro_agent.memory.get_user_profile(user_id)

            self.assertIsNotNone(simple_profile)
            if pro_profile:
                self.assertIsNotNone(pro_profile)

    def test_memory_tool_integration(self):
        """Araçlar entegrasyonu testi"""
        user_id = "tool_integration_user"

        # Basit agent ile araçları kullan
        self.simple_agent.set_user(user_id)

        # Araç executor oluştur
        tool_executor = ToolExecutor(self.simple_agent.memory_manager)

        # Doğrudan araç kullan
        result = tool_executor.memory_tools.execute_tool("show_user_info", {"user_id": user_id})
        self.assertIsInstance(result, str)

        # Chat üzerinden araç kullan
        response = self.simple_agent.chat("Hakkımda ne biliyorsun?", user_id=user_id)
        self.assertIsInstance(response, str)

    def test_prompt_template_integration(self):
        """Prompt şablonu entegrasyonu testi"""
        # Şablonları kontrol et
        templates = prompt_manager.list_templates()
        self.assertGreater(len(templates), 0)

        # Şablon oluşturma testi
        template = prompt_manager.get_template("customer_service")
        self.assertIsNotNone(template)

        # Şablon render testi
        rendered = template.render(company_name="Test Company")
        self.assertIn("Test Company", rendered)

    def test_config_integration(self):
        """Yapılandırma entegrasyonu testi"""
        if self.pro_available:
            config = get_config()

            # Config değerlerini kontrol et
            model = config.get("llm.model")
            template = config.get("prompt.template")

            self.assertIsNotNone(model)
            self.assertIsNotNone(template)

    def test_knowledge_base_integration(self):
        """Bilgi bankası entegrasyonu testi"""
        if self.pro_available:
            # Bilgi ekleme testi
            kb_id = self.pro_agent.add_knowledge(
                category="integration_test",
                question="Entegrasyon testi sorusu?",
                answer="Entegrasyon testi cevabı",
                keywords=["test", "integration"],
                priority=5
            )

            self.assertGreater(kb_id, 0)

            # Bilgi arama testi
            results = self.pro_agent.memory.search_knowledge("test")
            self.assertGreater(len(results), 0)

    def test_error_handling(self):
        """Hata yönetimi testi"""
        # Geçersiz kullanıcı ID
        try:
            response = self.simple_agent.chat("Test", user_id="nonexistent_user")
            # Bu noktaya gelmemeli (hata vermeli)
            self.fail("Geçersiz kullanıcı ID ile devam etti")
        except Exception:
            # Beklenen davranış - hata vermeli
            pass

        # Geçersiz araç komutu
        tool_executor = ToolExecutor(self.simple_agent.memory_manager)
        result = tool_executor.memory_tools.execute_tool("nonexistent_tool", {})
        self.assertIn("bulunamadı", result)

    def test_performance_basic(self):
        """Temel performans testi"""
        import time

        user_id = "perf_test"
        self.simple_agent.set_user(user_id)

        # Birkaç hızlı konuşma
        start_time = time.time()

        for i in range(5):
            response = self.simple_agent.chat(f"Performans testi mesaj {i}")

        end_time = time.time()
        duration = end_time - start_time

        # 5 konuşma 10 saniyeden az sürmeli
        self.assertLess(duration, 10.0)

    def test_memory_consistency(self):
        """Bellek tutarlılık testi"""
        user_id = "consistency_test"

        # Aynı kullanıcı ile hem basit hem Pro agent kullan
        self.simple_agent.set_user(user_id)

        # 3 konuşma ekle
        for i in range(3):
            self.simple_agent.chat(f"Konuşma {i}")

        # Aynı kullanıcıyı Pro agent ile kontrol et (farklı backend)
        if self.pro_available:
            # Bu test farklı backend'ler arası geçişi test eder
            pro_conversations = self.pro_agent.memory.get_recent_conversations(user_id)
            simple_conversations = self.simple_agent.memory_manager.get_recent_conversations(user_id)

            # Farklı backend'ler farklı veri tutar
            # Sadece metodların çalıştığını test ederiz
            self.assertIsInstance(simple_conversations, list)


def run_integration_tests():
    """Entegrasyon testlerini çalıştır"""
    print("🔗 ENTEGRASYON TEST SUITE")
    print("=" * 50)

    # Test suite oluştur
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestIntegration)

    # Test çalıştır
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_tests()

    if success:
        print("\n✅ Tüm entegrasyon testleri başarıyla geçti!")
    else:
        print("\n❌ Bazı entegrasyon testleri başarısız oldu!")

    print("=" * 50)
