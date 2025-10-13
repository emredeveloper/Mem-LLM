"""
Memory Tools Özel Testleri
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import tempfile
import shutil

from memory_manager import MemoryManager
from memory_tools import MemoryTools


class TestMemoryTools(unittest.TestCase):
    """Memory Tools özel testleri"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.memory_dir = os.path.join(self.temp_dir, "test_memories")
        self.memory = MemoryManager(self.memory_dir)
        self.memory.add_interaction("test_user", "Test mesajı", "Test cevabı")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_tools_creation(self):
        """Araçlar oluşturma testi"""
        tools = MemoryTools(self.memory)
        self.assertIsNotNone(tools)
        self.assertIn('list_memories', tools.tools)


if __name__ == "__main__":
    print("Memory Tools testleri çalıştırılıyor...")
    unittest.main()

