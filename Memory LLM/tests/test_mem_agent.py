"""
Mem-Agent Comprehensive Test Suite
Tests all basic functions
"""

import unittest
import tempfile
import json
import time
import shutil
import os

# Test edilecek modüller
from mem_llm import MemAgent, MemoryManager, OllamaClient


class TestMemAgent(unittest.TestCase):
    """MemAgent temel fonksiyonlarını test eder"""

    def setUp(self):
        """Her test öncesi kurulum"""
        self.temp_dir = tempfile.mkdtemp()
        self.memory_dir = os.path.join(self.temp_dir, "test_memories")

        self.agent = MemAgent(
            model="granite4:tiny-h",
            use_sql=False,
            memory_dir=self.memory_dir
        )

    def tearDown(self):
        """Her test sonrası temizlik"""
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

    def test_basic_chat(self):
        """Temel sohbet testi"""
        self.agent.set_user("test_user")

        response = self.agent.chat("Merhaba!")
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)


class TestMemoryManager(unittest.TestCase):
    """MemoryManager fonksiyonlarını test eder"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.memory_dir = os.path.join(self.temp_dir, "test_memories")
        self.memory = MemoryManager(self.memory_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_memory_creation(self):
        """Bellek oluşturma testi"""
        self.assertIsNotNone(self.memory)
        self.assertTrue(os.path.exists(self.memory_dir))


class TestLLMClient(unittest.TestCase):
    """LLM istemcisi testleri"""

    def setUp(self):
        self.client = OllamaClient(model="granite4:tiny-h")

    def test_client_creation(self):
        """İstemci oluşturma testi"""
        self.assertIsNotNone(self.client)
        self.assertEqual(self.client.model, "granite4:tiny-h")


if __name__ == "__main__":
    print("🧪 MEM-AGENT TEST SUITE")
    print("=" * 50)

    # Tüm testleri çalıştır
    unittest.main(verbosity=2)

