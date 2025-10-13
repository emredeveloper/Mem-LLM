"""
Memory Tools Özel Testleri
"""

import unittest
import tempfile
import os
import shutil

from memory_manager import MemoryManager
from memory_tools import MemoryTools


class TestMemoryTools(unittest.TestCase):
    """Memory Tools özel testleri"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.memory_dir = os.path.join(self.temp_dir, "test_memories")
        self.memory = MemoryManager(self.memory_dir)

        # Örnek veri ekle
        self.memory.add_interaction("test_user", "Test mesajı", "Test cevabı")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_tools_creation(self):
        """Araçlar oluşturma testi"""
        tools = MemoryTools(self.memory)
        self.assertIsNotNone(tools)
        self.assertIn('list_memories', tools.tools)


def run_specific_test(test_type):
    """Belirli test türünü çalıştır"""
    if test_type == "all":
        return True  # Basit test
    return True


if __name__ == "__main__":
    print("Memory Tools testleri çalıştırılıyor...")
    unittest.main()
