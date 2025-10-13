"""
LLM Client Specific Tests
"""

import unittest

from mem_llm import OllamaClient


class TestLLMClient(unittest.TestCase):
    """LLM Client specific tests"""

    def setUp(self):
        self.client = OllamaClient(model="granite4:tiny-h")

    def test_client_creation(self):
        """Client creation test"""
        self.assertIsNotNone(self.client)
        self.assertEqual(self.client.model, "granite4:tiny-h")


if __name__ == "__main__":
    print("LLM Client tests are running...")
    unittest.main()

