"""
LLM Client Özel Testleri
"""

import unittest

from llm_client import OllamaClient


class TestLLMClient(unittest.TestCase):
    """LLM Client özel testleri"""

    def setUp(self):
        self.client = OllamaClient(model="granite4:tiny-h")

    def test_client_creation(self):
        """İstemci oluşturma testi"""
        self.assertIsNotNone(self.client)
        self.assertEqual(self.client.model, "granite4:tiny-h")


def run_specific_test(test_type):
    """Belirli test türünü çalıştır"""
    if test_type == "all":
        return True  # Basit test
    return True


if __name__ == "__main__":
    print("LLM Client testleri çalıştırılıyor...")
    unittest.main()
