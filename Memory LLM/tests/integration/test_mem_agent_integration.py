"""
Integration Tests
Tests all system components working together
"""

import os
import shutil
import unittest
import uuid
from pathlib import Path

# Import all modules
from mem_llm import MemAgent, ToolExecutor


class TestIntegration(unittest.TestCase):
    """System integration tests"""

    def setUp(self):
        """Setup before test"""
        root = Path(__file__).resolve().parents[1] / ".tmp"
        root.mkdir(parents=True, exist_ok=True)
        self.temp_dir = str(root / f"integration_{uuid.uuid4().hex[:8]}")
        os.makedirs(self.temp_dir, exist_ok=True)

        # For simple agent (JSON memory)
        self.simple_agent = MemAgent(
            model="rnj-1:latest",
            use_sql=False,
            memory_dir=os.path.join(self.temp_dir, "simple_memories"),
        )

        # For advanced agent (SQL memory and config)
        config_file = os.path.join(self.temp_dir, "integration_config.yaml")
        self._create_integration_config(config_file)

        try:
            self.advanced_agent = MemAgent(config_file=config_file, use_sql=True)
            self.advanced_available = True
        except Exception as e:
            print(f"  Advanced agent could not be created: {e}")
            self.advanced_available = False

    def tearDown(self):
        """Cleanup after test"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_integration_config(self, config_file):
        """Config file for integration test"""
        config_content = """
llm:
  model: "ministral-3:14b"
  base_url: "http://localhost:11434"
  temperature: 0.7

memory:
  backend: "sql"
  db_path: "integration_test.db"

prompt:
  template: "customer_service"
  variables:
    company_name: "Integration Test Company"

knowledge_base:
  enabled: true
  auto_load: false

logging:
  enabled: false
"""
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(config_content)

    def test_cross_compatibility(self):
        """Cross-compatibility test for JSON and SQL memory."""

        user_id = "cross_compat_user"

        # Chat with the simple agent (JSON memory)
        self.simple_agent.set_user(user_id, name="Cross Test")
        response1 = self.simple_agent.chat("Hello simple agent!")

        # Use the same user with the advanced agent (SQL memory)
        if self.advanced_available:
            self.advanced_agent.set_user(user_id)
            response2 = self.advanced_agent.chat("Hello advanced agent!")

            # Each agent should work with its own memory backend.
            # Different backends store data independently.
            self.assertIsInstance(response1, str)
            self.assertIsInstance(response2, str)

    def test_memory_tool_integration(self):
        """Tool integration test."""
        user_id = "tool_integration_user"

        # Use tools with the simple agent
        self.simple_agent.set_user(user_id)

        # Create the tool executor
        tool_executor = ToolExecutor(self.simple_agent.memory)

        # Use the tool directly
        result = tool_executor.memory_tools.execute_tool("show_user_info", {"user_id": user_id})
        self.assertIsInstance(result, str)

        # Use the tool through chat flow
        response = self.simple_agent.chat("What do you know about me?", user_id=user_id)
        self.assertIsInstance(response, str)

    @unittest.skip("prompt_manager module deprecated")
    def test_prompt_template_integration(self):
        """Prompt template integration test."""
        pass

    def test_config_integration(self):
        """Configuration integration test."""
        if self.advanced_available:
            # The advanced agent should load configuration.
            self.assertIsNotNone(self.advanced_agent.config)

            # Check configuration values
            if hasattr(self.advanced_agent, "config") and self.advanced_agent.config:
                model = self.advanced_agent.config.get("llm.model")
                self.assertIsNotNone(model)

    def test_knowledge_base_integration(self):
        """Knowledge base integration test."""
        if self.advanced_available:
            # Test knowledge insertion
            kb_id = self.advanced_agent.add_knowledge(
                category="integration_test",
                question="Integration test question?",
                answer="Integration test answer",
                keywords=["test", "integration"],
                priority=5,
            )

            self.assertGreater(kb_id, 0)

            # Test knowledge search
            results = self.advanced_agent.memory.search_knowledge("test")
            self.assertGreater(len(results), 0)

    def test_error_handling(self):
        """Error handling test."""
        # Try chatting without setting a user
        response = self.simple_agent.chat("Test")
        self.assertIn("Error", response)

        # Invalid tool command
        tool_executor = ToolExecutor(self.simple_agent.memory)
        result = tool_executor.memory_tools.execute_tool("nonexistent_tool", {})
        self.assertIn("not found", result)

    def test_performance_basic(self):
        """Basic performance test."""
        import time

        user_id = "perf_test"
        self.simple_agent.set_user(user_id)

        # A few quick messages
        start_time = time.time()

        for i in range(3):
            _ = self.simple_agent.chat(f"Performance test message {i}")

        end_time = time.time()
        duration = end_time - start_time

        # Three messages should complete within a reasonable time window.
        self.assertLess(duration, 60.0)

    def test_memory_consistency(self):
        """Memory consistency test."""
        import uuid

        user_id = f"consistency_test_{uuid.uuid4().hex[:8]}"

        # Talk with the simple agent
        self.simple_agent.set_user(user_id)

        # Add three conversations
        for i in range(3):
            self.simple_agent.chat(f"Conversation {i}")

        # Verify that conversations were stored
        if hasattr(self.simple_agent.memory, "get_recent_conversations"):
            simple_conversations = self.simple_agent.memory.get_recent_conversations(user_id)
            self.assertIsInstance(simple_conversations, list)
            self.assertGreaterEqual(len(simple_conversations), 3)


def run_integration_tests():
    """Run the integration test suite."""
    print(" INTEGRATION TEST SUITE")
    print("=" * 50)

    # Build the test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestIntegration)

    # Run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_integration_tests()

    if success:
        print("\n All integration tests passed successfully!")
    else:
        print("\n Some integration tests failed!")

    print("=" * 50)


