# BU DOSYA ARTIK KULLANILMIYOR - BİRLEŞİK SİSTEM KULLANIN
# Lütfen test_mem_agent.py dosyasını kullanın


@unittest.skipUnless(PRO_AVAILABLE, "Pro modülleri mevcut değil")
class TestMemAgentPro(unittest.TestCase):
    """MemAgentPro gelişmiş fonksiyonlarını test eder"""

    def setUp(self):
        """Her test öncesi kurulum"""
        self.temp_dir = tempfile.mkdtemp()

        # Test için ayrı config dosyası oluştur
        self.config_file = os.path.join(self.temp_dir, "test_config.yaml")
        self._create_test_config()

        # Test için ayrı veritabanı dosyası
        self.db_path = os.path.join(self.temp_dir, "test_memories.db")

        # Agent oluştur
        self.agent = MemAgentPro(config_file=self.config_file)

    def tearDown(self):
        """Her test sonrası temizlik"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_test_config(self):
        """Test için basit config dosyası oluştur"""
        config_content = """
llm:
  model: "granite4:tiny-h"
  base_url: "http://localhost:11434"
  temperature: 0.7

memory:
  backend: "sql"
  db_path: "test_memories.db"

prompt:
  template: "customer_service"
  variables:
    company_name: "Test Şirketi"

knowledge_base:
  enabled: true
  auto_load: false

logging:
  enabled: false
"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)

    def test_pro_agent_creation(self):
        """Pro agent oluşturma testi"""
        self.assertIsNotNone(self.agent)
        self.assertIsInstance(self.agent, MemAgentPro)

    def test_config_loading(self):
        """Yapılandırma yükleme testi"""
        config = get_config(self.config_file)

        self.assertIsNotNone(config)
        self.assertEqual(config.get("llm.model"), "granite4:tiny-h")
        self.assertEqual(config.get("prompt.template"), "customer_service")

    def test_sql_memory_creation(self):
        """SQL bellek oluşturma testi"""
        self.assertIsNotNone(self.agent.memory)
        self.assertIsInstance(self.agent.memory, SQLMemoryManager)

    def test_user_creation_pro(self):
        """Pro kullanıcı oluşturma testi"""
        user_id = "pro_test_user"
        self.agent.set_user(user_id, name="Pro Test Kullanıcı")

        # Kullanıcı veritabanında var mı kontrolü
        profile = self.agent.memory.get_user_profile(user_id)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.get('name'), 'Pro Test Kullanıcı')

    def test_advanced_chat(self):
        """Gelişmiş sohbet testi"""
        self.agent.set_user("chat_test")

        response = self.agent.chat("Merhaba! Nasılsın?")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

    def test_prompt_templates(self):
        """Prompt şablonları testi"""
        templates = prompt_manager.list_templates()

        self.assertIsInstance(templates, list)
        self.assertGreater(len(templates), 0)
        self.assertIn("customer_service", templates)

    def test_template_rendering(self):
        """Şablon oluşturma testi"""
        template = prompt_manager.get_template("customer_service")
        self.assertIsNotNone(template)

        rendered = template.render(company_name="TestCo")
        self.assertIsInstance(rendered, str)
        self.assertIn("TestCo", rendered)

    def test_knowledge_base_creation(self):
        """Bilgi bankası oluşturma testi"""
        # Bilgi ekleme testi
        kb_id = self.agent.add_knowledge(
            category="test",
            question="Test sorusu",
            answer="Test cevabı",
            keywords=["test"],
            priority=5
        )

        self.assertGreater(kb_id, 0)

    def test_knowledge_search(self):
        """Bilgi bankası arama testi"""
        # Test verisi ekle
        self.agent.add_knowledge("ürün", "Laptop ne kadar?", "1000 TL", ["laptop", "fiyat"])

        # Arama testi
        results = self.agent.memory.search_knowledge("laptop")
        self.assertGreater(len(results), 0)

        # İlk sonuç kontrolü
        first_result = results[0]
        self.assertEqual(first_result['category'], 'ürün')
        self.assertIn('laptop', first_result.get('question', '').lower())


@unittest.skipUnless(PRO_AVAILABLE, "Pro modülleri mevcut değil")
class TestSQLMemoryManager(unittest.TestCase):
    """SQL bellek yöneticisi testleri"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_sql.db")
        self.memory = SQLMemoryManager(self.db_path)

    def tearDown(self):
        self.memory.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_sql_creation(self):
        """SQL veritabanı oluşturma testi"""
        self.assertIsNotNone(self.memory)
        self.assertTrue(os.path.exists(self.db_path))

    def test_user_operations(self):
        """Kullanıcı işlemleri testi"""
        user_id = "sql_test_user"

        # Kullanıcı ekleme
        self.memory.add_user(user_id, name="SQL Test")

        # Kullanıcı kontrolü
        profile = self.memory.get_user_profile(user_id)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.get('name'), 'SQL Test')

    def test_conversation_operations(self):
        """Konuşma işlemleri testi"""
        user_id = "conv_test"

        # Konuşma ekleme
        conv_id = self.memory.add_interaction(
            user_id=user_id,
            user_message="SQL test mesajı",
            bot_response="SQL test cevabı",
            metadata={"test": True}
        )

        self.assertGreater(conv_id, 0)

        # Konuşma kontrolü
        conversations = self.memory.get_recent_conversations(user_id)
        self.assertEqual(len(conversations), 1)

        conv = conversations[0]
        self.assertEqual(conv['user_message'], "SQL test mesajı")
        self.assertEqual(conv['bot_response'], "SQL test cevabı")

    def test_statistics(self):
        """İstatistik testi"""
        # Birkaç kullanıcı ve konuşma ekle
        for i in range(3):
            user_id = f"stat_user_{i}"
            self.memory.add_user(user_id)
            self.memory.add_interaction(user_id, f"Mesaj {i}", f"Cevap {i}")

        # İstatistikleri kontrol et
        stats = self.memory.get_statistics()

        self.assertIsInstance(stats, dict)
        self.assertEqual(stats['total_users'], 3)
        self.assertEqual(stats['total_interactions'], 3)
        self.assertAlmostEqual(stats['avg_interactions_per_user'], 1.0)


@unittest.skipUnless(PRO_AVAILABLE, "Pro modülleri mevcut değil")
class TestKnowledgeLoader(unittest.TestCase):
    """Bilgi bankası yükleyici testleri"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_kb.db")
        self.memory = SQLMemoryManager(self.db_path)

        self.loader = KnowledgeLoader(self.memory)

    def tearDown(self):
        self.memory.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_ecommerce_kb_loading(self):
        """E-ticaret bilgi bankası yükleme testi"""
        count = self.loader.load_default_ecommerce_kb()

        self.assertGreater(count, 0)

        # Arama testi
        results = self.memory.search_knowledge("kargo")
        self.assertGreater(len(results), 0)

    def test_tech_support_kb_loading(self):
        """Teknik destek bilgi bankası yükleme testi"""
        count = self.loader.load_default_tech_support_kb()

        self.assertGreater(count, 0)

        # Arama testi
        results = self.memory.search_knowledge("bağlantı")
        self.assertGreater(len(results), 0)


def run_pro_tests():
    """Pro testlerini çalıştır"""
    if not PRO_AVAILABLE:
        print("❌ Pro modülleri mevcut değil!")
        return False

    print("🚀 MEM-AGENT PRO TEST SUITE")
    print("=" * 50)

    # Test suite oluştur
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Tüm Pro test sınıflarını ekle
    test_classes = [TestMemAgentPro, TestSQLMemoryManager, TestKnowledgeLoader]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Test çalıştır
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    if PRO_AVAILABLE:
        success = run_pro_tests()

        if success:
            print("\n✅ Tüm Pro testler başarıyla geçti!")
        else:
            print("\n❌ Bazı Pro testler başarısız oldu!")
    else:
        print("❌ Pro modülleri yüklenemedi!")

    print("=" * 50)
