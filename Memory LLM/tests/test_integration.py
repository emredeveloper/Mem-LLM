"""
Integration Tests
Tests all system components working together
"""

import unittest
import tempfile
import shutil
import os

# Import all modules
from mem_llm import (
    MemAgent,
    MemoryManager,
    SQLMemoryManager,
    MemoryTools,
    ToolExecutor,
    prompt_manager,
    get_config
)


class TestIntegration(unittest.TestCase):
    """System integration tests"""

    def setUp(self):
        """Setup before test"""
        self.temp_dir = tempfile.mkdtemp()

        # For simple agent (JSON memory)
        self.simple_agent = MemAgent(
            model="granite4:tiny-h",
            use_sql=False,
            memory_dir=os.path.join(self.temp_dir, "simple_memories")
        )

        # For advanced agent (SQL memory and config)
        config_file = os.path.join(self.temp_dir, "integration_config.yaml")
        self._create_integration_config(config_file)

        try:
            self.advanced_agent = MemAgent(
                config_file=config_file,
                use_sql=True
            )
            self.advanced_available = True
        except Exception as e:
            print(f"⚠️  Advanced agent could not be created: {e}")
            self.advanced_available = False

    def tearDown(self):
        """Cleanup after test"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_integration_config(self, config_file):
        """Config file for integration test"""
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
        """Çapraz uyumluluk testi - JSON ve SQL bellek"""

        user_id = "cross_compat_user"

        # Basit agent ile konuşma (JSON bellek)
        self.simple_agent.set_user(user_id, name="Cross Test")
        response1 = self.simple_agent.chat("Merhaba basit agent!")

        # Aynı kullanıcıyı gelişmiş agent ile kullan (SQL bellek)
        if self.advanced_available:
            self.advanced_agent.set_user(user_id)
            response2 = self.advanced_agent.chat("Merhaba gelişmiş agent!")

            # Her iki agent de kendi belleğinde kullanıcıyı görmeli
            # Not: Farklı backend'ler farklı veri tutar
            self.assertIsInstance(response1, str)
            self.assertIsInstance(response2, str)

    def test_memory_tool_integration(self):
        """Araçlar entegrasyonu testi"""
        user_id = "tool_integration_user"

        # Basit agent ile araçları kullan
        self.simple_agent.set_user(user_id)

        # Araç executor oluştur
        tool_executor = ToolExecutor(self.simple_agent.memory)

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
        if self.advanced_available:
            # Gelişmiş agent config kullanıyor
            self.assertIsNotNone(self.advanced_agent.config)
            
            # Config değerlerini kontrol et
            if hasattr(self.advanced_agent, 'config') and self.advanced_agent.config:
                model = self.advanced_agent.config.get("llm.model")
                self.assertIsNotNone(model)

    def test_knowledge_base_integration(self):
        """Bilgi bankası entegrasyonu testi"""
        if self.advanced_available:
            # Bilgi ekleme testi
            kb_id = self.advanced_agent.add_knowledge(
                category="integration_test",
                question="Entegrasyon testi sorusu?",
                answer="Entegrasyon testi cevabı",
                keywords=["test", "integration"],
                priority=5
            )

            self.assertGreater(kb_id, 0)

            # Bilgi arama testi
            results = self.advanced_agent.memory.search_knowledge("test")
            self.assertGreater(len(results), 0)

    def test_error_handling(self):
        """Hata yönetimi testi"""
        # Kullanıcı olmadan chat deneme
        response = self.simple_agent.chat("Test")
        self.assertIn("Error", response)  # Error mesajı İngilizce

        # Geçersiz araç komutu
        tool_executor = ToolExecutor(self.simple_agent.memory)
        result = tool_executor.memory_tools.execute_tool("nonexistent_tool", {})
        self.assertIn("not found", result)  # İngilizce mesaj

    def test_performance_basic(self):
        """Temel performans testi"""
        import time

        user_id = "perf_test"
        self.simple_agent.set_user(user_id)

        # Birkaç hızlı konuşma
        start_time = time.time()

        for i in range(3):
            response = self.simple_agent.chat(f"Performans testi mesaj {i}")

        end_time = time.time()
        duration = end_time - start_time

        # 3 konuşma makul bir sürede tamamlanmalı (60 saniye)
        # LLM çağrıları yavaş olabilir, gerçekçi bir limit
        self.assertLess(duration, 60.0)

    def test_memory_consistency(self):
        """Bellek tutarlılık testi"""
        import uuid
        user_id = f"consistency_test_{uuid.uuid4().hex[:8]}"  # Benzersiz user_id

        # Basit agent ile konuşmalar
        self.simple_agent.set_user(user_id)

        # 3 konuşma ekle
        for i in range(3):
            self.simple_agent.chat(f"Konuşma {i}")

        # Konuşmaların kaydedildiğini kontrol et
        if hasattr(self.simple_agent.memory, 'get_recent_conversations'):
            simple_conversations = self.simple_agent.memory.get_recent_conversations(user_id)
            self.assertIsInstance(simple_conversations, list)
            self.assertGreaterEqual(len(simple_conversations), 3)  # En az 3 olmalı


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

