"""
MemoryManager Özel Testleri
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import tempfile
import shutil

from memory_manager import MemoryManager


class TestMemoryManager(unittest.TestCase):
    """MemoryManager özel testleri"""

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


if __name__ == "__main__":
    print("MemoryManager testleri çalıştırılıyor...")
    unittest.main()

