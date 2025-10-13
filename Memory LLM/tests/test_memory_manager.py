"""
MemoryManager Specific Tests
"""

import unittest
import tempfile
import shutil
import os

from mem_llm import MemoryManager


class TestMemoryManager(unittest.TestCase):
    """MemoryManager specific tests"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.memory_dir = os.path.join(self.temp_dir, "test_memories")
        self.memory = MemoryManager(self.memory_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_memory_creation(self):
        """Memory creation test"""
        self.assertIsNotNone(self.memory)
        self.assertTrue(os.path.exists(self.memory_dir))


if __name__ == "__main__":
    print("MemoryManager tests are running...")
    unittest.main()

