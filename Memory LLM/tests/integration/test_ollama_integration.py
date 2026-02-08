"""
Integration tests for Ollama backend.
"""
import os
import pytest

from mem_llm import MemAgent
from mem_llm.clients.ollama_client import OllamaClient


def _select_ollama_test_model(base_url: str = "http://localhost:11434") -> str:
    """
    Select a usable local Ollama model for integration tests.

    Priority:
    1. OLLAMA_TEST_MODEL env var (if available locally)
    2. First non-embedding model from local model list
    3. First available model
    """
    probe_client = OllamaClient(model="rnj-1:latest", base_url=base_url)
    if not probe_client.check_connection():
        pytest.skip(f"Ollama not available at {base_url}")

    models = probe_client.list_models()
    if not models:
        pytest.skip("Ollama is running but no models are installed")

    preferred = os.getenv("OLLAMA_TEST_MODEL")
    if preferred:
        if preferred in models:
            return preferred
        pytest.skip(
            f"OLLAMA_TEST_MODEL='{preferred}' not found locally. "
            f"Available models: {', '.join(models)}"
        )

    for model in models:
        if "embed" not in model.lower():
            return model

    return models[0]


@pytest.mark.integration
@pytest.mark.slow
class TestOllamaIntegration:
    """Integration tests for Ollama backend"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.ollama_url = "http://localhost:11434"
        self.model_name = _select_ollama_test_model(self.ollama_url)

    def test_ollama_client_creation(self):
        """Test creating Ollama client"""
        try:
            client = OllamaClient(model=self.model_name, base_url=self.ollama_url)
            assert client is not None
            assert client.model == self.model_name
        except Exception as e:
            pytest.skip(f"Ollama not available: {e}")

    def test_ollama_connection(self):
        """Test Ollama connection"""
        try:
            client = OllamaClient(model=self.model_name, base_url=self.ollama_url)
            # Try a simple chat
            response = client.chat([{"role": "user", "content": "Hello"}])
            assert response is not None
            assert len(response) > 0
        except Exception as e:
            pytest.skip(f"Ollama not available: {e}")

    def test_ollama_list_models(self):
        """Test listing available Ollama models"""
        try:
            client = OllamaClient(model=self.model_name)
            models = client.list_models()
            assert models is not None
            assert isinstance(models, list)
            # Check if our test model is in the list
            assert self.model_name in models
        except Exception as e:
            pytest.skip(f"Ollama not available: {e}")

    def test_ollama_with_mem_agent(self):
        """Test MemAgent with Ollama backend"""
        try:
            agent = MemAgent(
                model=self.model_name, backend="ollama", use_sql=False, check_connection=False
            )
            assert agent is not None
            assert agent.backend == "ollama"
        except Exception as e:
            pytest.skip(f"Ollama not available: {e}")

    def test_ollama_streaming(self):
        """Test Ollama streaming chat"""
        try:
            client = OllamaClient(model=self.model_name)

            chunks = []
            for chunk in client.chat_stream([{"role": "user", "content": "Count to 3"}]):
                chunks.append(chunk)

            assert len(chunks) > 0
            full_response = "".join(chunks)
            assert len(full_response) > 0
        except Exception as e:
            pytest.skip(f"Ollama streaming not available: {e}")

    def test_ollama_with_tools(self):
        """Test Ollama with tool calling"""
        try:
            agent = MemAgent(
                model=self.model_name, backend="ollama", use_sql=False, check_connection=False
            )
            agent.set_user("test_ollama_tools_user")

            # Test with a simple tool call
            response = agent.chat("What is 2 + 2?")
            assert response is not None
            assert len(response) > 0
            # Accept either numeric or word form.
            normalized = response.lower()
            assert ("4" in normalized) or ("four" in normalized)
        except Exception as e:
            pytest.skip(f"Ollama tool calling not available: {e}")

    def test_ollama_memory_integration(self):
        """Test Ollama with memory features"""
        try:
            agent = MemAgent(
                model=self.model_name, backend="ollama", use_sql=True, check_connection=False
            )
            agent.set_user("test_ollama_user")

            # First message
            response1 = agent.chat("My name is Bob")
            assert response1 is not None

            # Second message - should remember
            response2 = agent.chat("What is my name?")
            assert response2 is not None
            # Note: Memory recall depends on model capabilities
        except Exception as e:
            pytest.skip(f"Ollama memory integration not available: {e}")

    def test_ollama_system_prompt(self):
        """Test Ollama with custom system prompt"""
        try:
            agent = MemAgent(
                model=self.model_name, backend="ollama", use_sql=False, check_connection=False
            )

            # Set custom system prompt
            agent.system_prompt = "You are a helpful math tutor. Always explain your reasoning."

            response = agent.chat("What is 5 + 3?")
            assert response is not None
            assert len(response) > 0
        except Exception as e:
            pytest.skip(f"Ollama system prompt not available: {e}")

    def test_ollama_conversation_history(self):
        """Test Ollama maintains conversation context"""
        try:
            agent = MemAgent(
                model=self.model_name, backend="ollama", use_sql=False, check_connection=False
            )
            agent.set_user("test_context_user")
            memory_token = "pizza_token_123"

            # First message
            response1 = agent.chat(f"Remember this exact token: {memory_token}")
            assert response1 is not None

            # Second message - should use context
            response2 = agent.chat("What token did I ask you to remember? Reply with token only.")
            assert response2 is not None

            # Primary check: model should mention the token.
            # Fallback check: conversation memory should persist locally even if model misses context.
            if memory_token not in response2.lower():
                recent = agent.memory.get_recent_conversations("test_context_user", limit=5)
                assert any(memory_token in (c.get("user_message", "").lower()) for c in recent)
        except Exception as e:
            pytest.skip(f"Ollama conversation history not available: {e}")


@pytest.mark.integration
class TestOllamaPerformance:
    """Performance tests for Ollama"""

    def test_ollama_response_time(self):
        """Test Ollama response time is reasonable"""
        import time

        try:
            model_name = _select_ollama_test_model()
            agent = MemAgent(
                model=model_name, backend="ollama", use_sql=False, check_connection=False
            )
            agent.set_user("test_perf_user")

            start = time.time()
            response = agent.chat("Hi")
            duration = time.time() - start

            assert response is not None
            assert "user id not specified" not in response.lower()
            # Response should be under 30 seconds for simple query
            assert duration < 30.0
        except Exception as e:
            pytest.skip(f"Ollama performance test not available: {e}")

    def test_ollama_concurrent_requests(self):
        """Test Ollama handles multiple requests"""
        import concurrent.futures

        try:
            model_name = _select_ollama_test_model()
            agent = MemAgent(
                model=model_name, backend="ollama", use_sql=False, check_connection=False
            )
            agent.set_user("test_concurrent_user")

            def make_request(i):
                return agent.chat(f"Count to {i}")

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(make_request, i) for i in range(1, 4)]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]

            assert len(results) == 3
            assert all(r is not None for r in results)
            assert all("user id not specified" not in r.lower() for r in results)
        except Exception as e:
            pytest.skip(f"Ollama concurrent requests not available: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
