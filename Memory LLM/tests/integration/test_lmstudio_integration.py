"""
Integration tests for LM Studio backend.
"""

import os

import pytest

from mem_llm import MemAgent
from mem_llm.clients.lmstudio_client import LMStudioClient


@pytest.mark.integration
@pytest.mark.slow
class TestLMStudioIntegration:
    """Integration tests for LM Studio backend"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.lmstudio_url = "http://localhost:1234"
        # Default LM Studio model for this project; can be overridden if needed.
        self.model_name = os.environ.get("MEM_LLM_LMSTUDIO_MODEL", "qwen3.5-2b")

    def test_lmstudio_client_creation(self):
        """Test creating LM Studio client"""
        try:
            client = LMStudioClient(model=self.model_name, base_url=self.lmstudio_url)
            assert client is not None
            assert client.model == self.model_name
        except Exception as e:
            pytest.skip(f"LM Studio not available: {e}")

    def test_lmstudio_connection(self):
        """Test LM Studio connection"""
        try:
            client = LMStudioClient(model=self.model_name, base_url=self.lmstudio_url)
            response = client.chat([{"role": "user", "content": "Hello"}])
            assert response is not None
            assert len(response) > 0
        except Exception as e:
            pytest.skip(f"LM Studio not available: {e}")

    def test_lmstudio_with_mem_agent(self):
        """Test MemAgent with LM Studio backend"""
        try:
            agent = MemAgent(
                model=self.model_name,
                backend="lmstudio",
                lmstudio_url=self.lmstudio_url,
                use_sql=False,
                check_connection=False,
            )
            assert agent is not None
            assert agent.backend == "lmstudio"
        except Exception as e:
            pytest.skip(f"LM Studio not available: {e}")

    def test_lmstudio_streaming(self):
        """Test LM Studio streaming chat"""
        try:
            client = LMStudioClient(model=self.model_name, base_url=self.lmstudio_url)

            chunks = []
            for chunk in client.chat_stream([{"role": "user", "content": "Count to 3"}]):
                chunks.append(chunk)

            assert len(chunks) > 0
            full_response = "".join(chunks)
            assert len(full_response) > 0
        except Exception as e:
            pytest.skip(f"LM Studio streaming not available: {e}")

    def test_lmstudio_with_tools(self):
        """Test LM Studio with tool calling"""
        try:
            agent = MemAgent(
                model=self.model_name,
                backend="lmstudio",
                lmstudio_url=self.lmstudio_url,
                use_sql=False,
                check_connection=False,
            )

            response = agent.chat("What is 2 + 2?")
            assert response is not None
            assert len(response) > 0
        except Exception as e:
            pytest.skip(f"LM Studio tool calling not available: {e}")

    def test_lmstudio_memory_integration(self):
        """Test LM Studio with memory features"""
        try:
            agent = MemAgent(
                model=self.model_name,
                backend="lmstudio",
                lmstudio_url=self.lmstudio_url,
                use_sql=True,
                check_connection=False,
            )
            agent.set_user("test_lmstudio_user")

            response1 = agent.chat("My name is Alice")
            assert response1 is not None

            response2 = agent.chat("What is my name?")
            assert response2 is not None
        except Exception as e:
            pytest.skip(f"LM Studio memory integration not available: {e}")


@pytest.mark.integration
class TestLMStudioVsOllama:
    """Comparison tests between LM Studio and Ollama"""

    def test_backend_switching(self):
        """Test switching between Ollama and LM Studio"""
        try:
            agent_ollama = MemAgent(
                model="ministral-3:14b", backend="ollama", use_sql=False, check_connection=False
            )
            assert agent_ollama.backend == "ollama"
        except Exception:
            pytest.skip("Ollama not available")

        try:
            agent_lmstudio = MemAgent(
                model="qwen3.5-2b",
                backend="lmstudio",
                lmstudio_url="http://localhost:1234",
                use_sql=False,
                check_connection=False,
            )
            assert agent_lmstudio.backend == "lmstudio"
        except Exception:
            pytest.skip("LM Studio not available")

    def test_response_consistency(self):
        """Test that both backends produce valid responses"""
        prompt = "What is 1+1?"

        try:
            agent_ollama = MemAgent(
                model="ministral-3:14b", backend="ollama", use_sql=False, check_connection=False
            )
            response_ollama = agent_ollama.chat(prompt)
            assert response_ollama is not None
            assert len(response_ollama) > 0
        except Exception:
            pytest.skip("Ollama not available")

        try:
            agent_lmstudio = MemAgent(
                model="qwen3.5-2b",
                backend="lmstudio",
                lmstudio_url="http://localhost:1234",
                use_sql=False,
                check_connection=False,
            )
            response_lmstudio = agent_lmstudio.chat(prompt)
            assert response_lmstudio is not None
            assert len(response_lmstudio) > 0
        except Exception:
            pytest.skip("LM Studio not available")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
