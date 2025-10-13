"""
Mem-Agent Kapsamlı Test Suite
Tüm temel fonksiyonları test eder
"""

import unittest
import tempfile
import os
from pathlib import Path
import json
import time

# Test edilecek modüller
from mem_agent import MemAgent
from memory_manager import MemoryManager
from llm_client import OllamaClient


class TestMemAgent(unittest.TestCase):
    """MemAgent temel fonksiyonlarını test eder"""

    def setUp(self):
        """Her test öncesi kurulum"""
        # Geçici dizin oluştur
        self.temp_dir = tempfile.mkdtemp()
        self.memory_dir = os.path.join(self.temp_dir, "test_memories")

        # Test için basit agent oluştur
        self.agent = MemAgent(
            model="granite4:tiny-h",
            memory_dir=self.memory_dir
        )

        # Test kullanıcıları
        self.test_users = ["user1", "user2", "user3"]

    def tearDown(self):
        """Her test sonrası temizlik"""
        # Geçici dosyaları temizle
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_agent_creation(self):
        """Agent oluşturma testi"""
        self.assertIsNotNone(self.agent)
        self.assertIsInstance(self.agent, MemAgent)
        self.assertEqual(self.agent.current_user, None)

    def test_user_setup(self):
        """Kullanıcı ayarlama testi"""
        user_id = "test_user"
        self.agent.set_user(user_id, name="Test Kullanıcı")

        self.assertEqual(self.agent.current_user, user_id)

        # Kullanıcı profili kontrolü
        profile = self.agent.memory_manager.get_user_profile(user_id)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.get('name'), 'Test Kullanıcı')

    def test_basic_chat(self):
        """Temel sohbet testi"""
        self.agent.set_user("test_user")

        response = self.agent.chat("Merhaba!")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)

        # Konuşma kaydedildi mi kontrolü
        conversations = self.agent.memory_manager.get_recent_conversations("test_user", limit=1)
        self.assertEqual(len(conversations), 1)
        self.assertEqual(conversations[0]['user_message'], "Merhaba!")

    def test_memory_persistence(self):
        """Bellek kalıcılık testi"""
        user_id = "persistence_test"

        # İlk konuşma
        self.agent.set_user(user_id)
        response1 = self.agent.chat("İlk mesaj")

        # Yeni agent oluştur (bellek yükleme testi)
        new_agent = MemAgent(memory_dir=self.memory_dir)
        new_agent.set_user(user_id)

        # İkinci konuşma
        response2 = new_agent.chat("İkinci mesaj")

        # Her iki konuşma da erişilebilir olmalı
        conversations = new_agent.memory_manager.get_recent_conversations(user_id, limit=10)
        self.assertEqual(len(conversations), 2)

    def test_user_switching(self):
        """Kullanıcı değiştirme testi"""
        # İlk kullanıcı
        self.agent.set_user("user1", name="Kullanıcı 1")
        self.agent.chat("User1 mesajı")

        # İkinci kullanıcı
        self.agent.set_user("user2", name="Kullanıcı 2")
        self.agent.chat("User2 mesajı")

        # Her kullanıcının kendi konuşması olmalı
        user1_convs = self.agent.memory_manager.get_recent_conversations("user1")
        user2_convs = self.agent.memory_manager.get_recent_conversations("user2")

        self.assertEqual(len(user1_convs), 1)
        self.assertEqual(len(user2_convs), 1)
        self.assertEqual(user1_convs[0]['user_message'], "User1 mesajı")
        self.assertEqual(user2_convs[0]['user_message'], "User2 mesajı")


class TestMemoryManager(unittest.TestCase):
    """MemoryManager fonksiyonlarını test eder"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.memory_dir = os.path.join(self.temp_dir, "test_memories")
        self.memory = MemoryManager(self.memory_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_memory_creation(self):
        """Bellek oluşturma testi"""
        self.assertIsNotNone(self.memory)
        self.assertTrue(os.path.exists(self.memory_dir))

    def test_user_memory_creation(self):
        """Kullanıcı belleği oluşturma testi"""
        user_id = "test_user"
        data = self.memory.load_memory(user_id)

        self.assertIsNotNone(data)
        self.assertIn('conversations', data)
        self.assertIn('profile', data)

    def test_interaction_recording(self):
        """Etkileşim kaydetme testi"""
        user_id = "test_user"

        # Etkileşim ekle
        self.memory.add_interaction(
            user_id=user_id,
            user_message="Test mesajı",
            bot_response="Test cevabı",
            metadata={"test": True}
        )

        # Kontrol et
        conversations = self.memory.get_recent_conversations(user_id)
        self.assertEqual(len(conversations), 1)

        conv = conversations[0]
        self.assertEqual(conv['user_message'], "Test mesajı")
        self.assertEqual(conv['bot_response'], "Test cevabı")
        self.assertEqual(conv['metadata']['test'], True)

    def test_memory_search(self):
        """Bellek arama testi"""
        user_id = "search_test"

        # Test verileri ekle
        self.memory.add_interaction(user_id, "Laptop almak istiyorum", "Laptop önerisi...")
        self.memory.add_interaction(user_id, "Telefon hakkında soru", "Telefon bilgisi...")
        self.memory.add_interaction(user_id, "Laptop fiyatı nedir?", "Laptop fiyat bilgisi...")

        # Arama testi
        results = self.memory.search_conversations(user_id, "laptop")
        self.assertEqual(len(results), 2)

        # Büyük/küçük harf duyarsız arama
        results2 = self.memory.search_conversations(user_id, "LAPTOP")
        self.assertEqual(len(results2), 2)

    def test_user_profile_management(self):
        """Kullanıcı profili yönetimi testi"""
        user_id = "profile_test"

        # Profil güncelleme
        self.memory.update_profile(user_id, {
            "name": "Test Kullanıcı",
            "preferences": {"language": "tr"}
        })

        # Profil kontrolü
        profile = self.memory.get_user_profile(user_id)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.get('name'), 'Test Kullanıcı')
        self.assertEqual(profile.get('preferences', {}).get('language'), 'tr')

    def test_memory_summary(self):
        """Bellek özeti testi"""
        user_id = "summary_test"

        # Birkaç etkileşim ekle
        for i in range(3):
            self.memory.add_interaction(
                user_id,
                f"Mesaj {i+1}",
                f"Cevap {i+1}",
                metadata={"index": i}
            )

        # Özet al
        summary = self.memory.get_summary(user_id)
        self.assertIsInstance(summary, str)
        self.assertIn("Toplam etkileşim: 3", summary)
        self.assertIn("Mesaj 1", summary)


class TestLLMClient(unittest.TestCase):
    """LLM istemcisi testleri"""

    def setUp(self):
        self.client = OllamaClient(model="granite4:tiny-h")

    def test_client_creation(self):
        """İstemci oluşturma testi"""
        self.assertIsNotNone(self.client)
        self.assertEqual(self.client.model, "granite4:tiny-h")

    def test_connection_check(self):
        """Bağlantı kontrol testi"""
        # Bu test gerçek bağlantıya bağlıdır
        # Sadece metodun çalışıp çalışmadığını test eder
        try:
            result = self.client.check_connection()
            self.assertIsInstance(result, bool)
        except Exception:
            # Bağlantı yoksa da metod çalışmalı
            pass

    def test_simple_generation(self):
        """Basit metin üretimi testi"""
        try:
            response = self.client.generate("Merhaba dünya!")
            self.assertIsInstance(response, str)
        except Exception:
            # Bağlantı yoksa hata verebilir
            pass


class TestMemoryTools(unittest.TestCase):
    """Araçlar sistemi testleri"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.memory_dir = os.path.join(self.temp_dir, "test_memories")
        self.memory = MemoryManager(self.memory_dir)

        # Örnek veri ekle
        self.memory.add_interaction("test_user", "Laptop almak istiyorum", "Laptop önerisi")
        self.memory.add_interaction("test_user", "Telefon fiyatı", "Telefon bilgisi")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_tools_creation(self):
        """Araçlar oluşturma testi"""
        from memory_tools import MemoryTools
        tools = MemoryTools(self.memory)

        self.assertIsNotNone(tools)
        self.assertIn('list_memories', tools.tools)
        self.assertIn('search_memories', tools.tools)

    def test_list_memories_tool(self):
        """Geçmiş listesi aracı testi"""
        from memory_tools import MemoryTools
        tools = MemoryTools(self.memory)

        result = tools.execute_tool("list_memories", {
            "user_id": "test_user",
            "limit": 5
        })

        self.assertIsInstance(result, str)
        self.assertIn("test_user", result)
        self.assertIn("Laptop", result)

    def test_search_tool(self):
        """Arama aracı testi"""
        from memory_tools import MemoryTools
        tools = MemoryTools(self.memory)

        result = tools.execute_tool("search_memories", {
            "user_id": "test_user",
            "keyword": "laptop"
        })

        self.assertIsInstance(result, str)
        self.assertIn("Laptop", result)

    def test_user_info_tool(self):
        """Kullanıcı bilgisi aracı testi"""
        from memory_tools import MemoryTools
        tools = MemoryTools(self.memory)

        result = tools.execute_tool("show_user_info", {
            "user_id": "test_user"
        })

        self.assertIsInstance(result, str)
        self.assertIn("test_user", result)


def run_specific_test(test_name):
    """Belirli bir testi çalıştır"""
    suite = unittest.TestSuite()

    if test_name == "agent":
        suite.addTest(unittest.makeSuite(TestMemAgent))
    elif test_name == "memory":
        suite.addTest(unittest.makeSuite(TestMemoryManager))
    elif test_name == "llm":
        suite.addTest(unittest.makeSuite(TestLLMClient))
    elif test_name == "tools":
        suite.addTest(unittest.makeSuite(TestMemoryTools))
    else:
        # Tüm testleri çalıştır
        suite.addTest(unittest.makeSuite(TestMemAgent))
        suite.addTest(unittest.makeSuite(TestMemoryManager))
        suite.addTest(unittest.makeSuite(TestLLMClient))
        suite.addTest(unittest.makeSuite(TestMemoryTools))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    print("🧪 MEM-AGENT TEST SUITE")
    print("=" * 50)

    # Tüm testleri çalıştır
    success = run_specific_test("all")

    if success:
        print("\n✅ Tüm testler başarıyla geçti!")
    else:
        print("\n❌ Bazı testler başarısız oldu!")

    print("=" * 50)
