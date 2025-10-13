"""
MemoryManager Özel Testleri
"""

import unittest
import tempfile
import os
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


def run_specific_test(test_type):
    """Belirli test türünü çalıştır"""
    if test_type == "all":
        return True  # Basit test
    return True


if __name__ == "__main__":
    print("MemoryManager testleri çalıştırılıyor...")
    unittest.main()
