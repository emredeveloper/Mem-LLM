"""
Memory Tools Specific Tests
"""

import unittest
import tempfile
import shutil
import os

from mem_llm import MemoryManager, MemoryTools


class TestMemoryTools(unittest.TestCase):
    """Memory Tools specific tests"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.memory_dir = os.path.join(self.temp_dir, "test_memories")
        self.memory = MemoryManager(self.memory_dir)
        self.memory.add_interaction("test_user", "Test message", "Test response")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_tools_creation(self):
        """Tools creation test"""
        tools = MemoryTools(self.memory)
        self.assertIsNotNone(tools)
        self.assertIn('list_memories', tools.tools)


if __name__ == "__main__":
    print("Memory Tools tests are running...")
    unittest.main()

