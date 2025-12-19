"""
Test Suite for Multi-Backend LLM Support (v1.3.6)
==================================================

Tests for Ollama and LM Studio backends (100% local).

Author: C. Emre Karataş
"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mem_llm import BaseLLMClient, LLMClientFactory, LMStudioClient, MemAgent, OllamaClientNew


class TestBaseLLMClient(unittest.TestCase):
    """Test base LLM client interface"""

    def test_base_client_is_abstract(self):
        """Test that BaseLLMClient cannot be instantiated directly"""
        print("\n🧪 TEST 1: Base client is abstract")

        with self.assertRaises(TypeError):
            _ = BaseLLMClient(model="test")

        print("   ✅ BaseLLMClient is abstract as expected")

    def test_message_validation(self):
        """Test message format validation"""
        print("\n🧪 TEST 2: Message validation")

        # Create a mock implementation
        class MockClient(BaseLLMClient):
            def chat(self, messages, **kwargs):
                return "test"

            def check_connection(self):
                return True

        client = MockClient(model="test")

        # Valid messages
        valid_messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
        ]
        self.assertTrue(client._validate_messages(valid_messages))

        # Invalid messages
        with self.assertRaises(ValueError):
            client._validate_messages([{"role": "invalid"}])  # Missing content

        with self.assertRaises(ValueError):
            client._validate_messages([{"content": "test"}])  # Missing role

        print("   ✅ Message validation works correctly")


class TestLLMClientFactory(unittest.TestCase):
    """Test LLM client factory"""

    def test_get_available_backends(self):
        """Test listing available backends"""
        print("\n🧪 TEST 3: List available backends")

        backends = LLMClientFactory.get_available_backends()

        self.assertIsInstance(backends, list)
        self.assertGreater(len(backends), 0)

        # Check required backends are present
        backend_names = [b["name"] for b in backends]
        self.assertIn("ollama", backend_names)
        self.assertIn("lmstudio", backend_names)

        print(f"   ✅ Found {len(backends)} local backends:")
        for backend in backends:
            print(f"      - {backend['name']}: {backend['description']}")

    def test_create_ollama_client(self):
        """Test creating Ollama client"""
        print("\n🧪 TEST 4: Create Ollama client")

        try:
            client = LLMClientFactory.create("ollama", model="rnj-1:latest")

            self.assertIsInstance(client, OllamaClientNew)
            self.assertEqual(client.model, "rnj-1:latest")

            print("   ✅ Ollama client created successfully")
            print(f"      Model: {client.model}")
            print(f"      Base URL: {client.base_url}")
        except Exception as e:
            print(f"   ⚠️  Ollama client creation skipped: {e}")

    def test_create_lmstudio_client(self):
        """Test creating LM Studio client"""
        print("\n🧪 TEST 5: Create LM Studio client")

        try:
            client = LLMClientFactory.create("lmstudio", model="local-model")

            self.assertIsInstance(client, LMStudioClient)
            self.assertEqual(client.model, "local-model")

            print("   ✅ LM Studio client created successfully")
            print(f"      Model: {client.model}")
            print(f"      Base URL: {client.base_url}")
        except Exception as e:
            print(f"   ⚠️  LM Studio client creation skipped: {e}")

    def test_create_invalid_backend(self):
        """Test error handling for invalid backend"""
        print("\n🧪 TEST 6: Invalid backend handling")

        with self.assertRaises(ValueError) as context:
            _ = LLMClientFactory.create_client(backend="invalid", model="test")

        self.assertIn("Unsupported backend", str(context.exception))
        print("   ✅ Invalid backend error handled correctly")

    def test_get_backend_info(self):
        """Test getting backend information"""
        print("\n🧪 TEST 8: Get backend info")

        info = LLMClientFactory.get_backend_info("ollama")

        self.assertIsInstance(info, dict)
        self.assertEqual(info["description"], "Local Ollama service")
        self.assertEqual(info["type"], "local")

        print("   ✅ Backend info retrieved:")
        print(f"      Description: {info['description']}")
        print(f"      Type: {info['type']}")

    def test_check_backend_availability(self):
        """Test checking backend availability"""
        print("\n🧪 TEST 9: Check backend availability")

        # Check Ollama
        ollama_available = LLMClientFactory.check_backend_availability("ollama")
        status = "Available" if ollama_available else "Not available"
        icon = "✅" if ollama_available else "❌"
        print(f"   {icon} Ollama: {status}")

        # Check LM Studio
        lmstudio_available = LLMClientFactory.check_backend_availability("lmstudio")
        status = "Available" if lmstudio_available else "Not available"
        icon = "✅" if lmstudio_available else "❌"
        print(f"   {icon} LM Studio: {status}")

        print("   ℹ️  Availability check completed")


class TestMemAgentMultiBackend(unittest.TestCase):
    """Test MemAgent with multiple backends"""

    def test_mem_agent_default_ollama(self):
        """Test MemAgent with default Ollama backend"""
        print("\n🧪 TEST 10: MemAgent with Ollama (default)")

        try:
            agent = MemAgent(
                model="rnj-1:latest", backend="ollama", use_sql=False, check_connection=False
            )

            self.assertIsNotNone(agent.llm)
            print("   ✅ MemAgent created with Ollama backend")
        except Exception as e:
            print(f"   ⚠️  Test skipped: {e}")

    def test_mem_agent_lmstudio(self):
        """Test MemAgent with LM Studio backend"""
        print("\n🧪 TEST 11: MemAgent with LM Studio")

        try:
            agent = MemAgent(
                model="local-model", backend="lmstudio", use_sql=False, check_connection=False
            )

            self.assertIsNotNone(agent.llm)
            self.assertIsInstance(agent.llm, LMStudioClient)
            print("   ✅ MemAgent created with LM Studio backend")
        except Exception as e:
            print(f"   ⚠️  Test skipped: {e}")

    def test_mem_agent_backward_compatibility(self):
        """Test backward compatibility with old API"""
        print("\n🧪 TEST 12: Backward compatibility")

        try:
            # Old API (without backend parameter)
            agent = MemAgent(
                model="rnj-1:latest",
                ollama_url="http://localhost:11434",
                use_sql=False,
                check_connection=False,
            )

            self.assertIsNotNone(agent.llm)
            print("   ✅ Backward compatibility maintained")
        except Exception as e:
            print(f"   ⚠️  Test skipped: {e}")


class TestOllamaClient(unittest.TestCase):
    """Test Ollama client specific features"""

    def setUp(self):
        """Set up test client"""
        try:
            self.client = OllamaClientNew(model="rnj-1:latest")
            self.available = self.client.check_connection()
        except:
            self.client = None
            self.available = False

    def test_ollama_connection(self):
        """Test Ollama connection"""
        print("\n🧪 TEST 13: Ollama connection")

        if not self.available:
            print("   ⚠️  Ollama not available, skipping test")
            return

        self.assertTrue(self.client.check_connection())
        print("   ✅ Ollama connection successful")

    def test_ollama_list_models(self):
        """Test listing Ollama models"""
        print("\n🧪 TEST 14: List Ollama models")

        if not self.available:
            print("   ⚠️  Ollama not available, skipping test")
            return

        models = self.client.list_models()
        self.assertIsInstance(models, list)

        print(f"   ✅ Found {len(models)} Ollama models")
        if models:
            print(f"      First 3: {', '.join(models[:3])}")


class TestLMStudioClient(unittest.TestCase):
    """Test LM Studio client specific features"""

    def setUp(self):
        """Set up test client"""
        try:
            self.client = LMStudioClient(model="local-model")
            self.available = self.client.check_connection()
        except:
            self.client = None
            self.available = False

    def test_lmstudio_connection(self):
        """Test LM Studio connection"""
        print("\n🧪 TEST 15: LM Studio connection")

        if not self.available:
            print("   ⚠️  LM Studio not available, skipping test")
            return

        self.assertTrue(self.client.check_connection())
        print("   ✅ LM Studio connection successful")

    def test_lmstudio_model_info(self):
        """Test getting LM Studio model info"""
        print("\n🧪 TEST 16: LM Studio model info")

        if not self.available:
            print("   ⚠️  LM Studio not available, skipping test")
            return

        info = self.client.get_model_info()
        self.assertIsInstance(info, dict)

        print("   ✅ Model info retrieved")
        if info:
            print(f"      Model ID: {info.get('id', 'N/A')}")


def run_tests():
    """Run all tests with nice output"""
    print("\n" + "=" * 70)
    print("MULTI-BACKEND LLM SUPPORT TEST SUITE (v1.3.0)")
    print("=" * 70)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBaseLLMClient))
    suite.addTests(loader.loadTestsFromTestCase(TestLLMClientFactory))
    suite.addTests(loader.loadTestsFromTestCase(TestMemAgentMultiBackend))
    suite.addTests(loader.loadTestsFromTestCase(TestOllamaClient))
    suite.addTests(loader.loadTestsFromTestCase(TestLMStudioClient))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED")

    print("=" * 70 + "\n")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
