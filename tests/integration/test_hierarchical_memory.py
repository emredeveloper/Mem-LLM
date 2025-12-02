#!/usr/bin/env python3
"""
Integration tests for Hierarchical Memory System
"""

import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Generator

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest  # noqa: E402

from mem_llm import MemAgent  # noqa: E402

# Configuration
OLLAMA_MODEL = "granite4:3b"
LMSTUDIO_MODEL = "llama-3.2-3b-instruct"  # Example model, user might need to adjust


@pytest.fixture
def agent_ollama() -> Generator[MemAgent, None, None]:
    """Fixture for MemAgent with Ollama backend"""
    agent = MemAgent(
        backend="ollama",
        model=OLLAMA_MODEL,
        enable_hierarchical_memory=True,
        use_sql=False,
        check_connection=False,  # Skip check for CI/Test speed
    )
    yield agent


def test_hierarchy_flow_ollama(agent_ollama):
    """Test full flow with Ollama"""
    user_id = "test_user_ollama"
    agent_ollama.set_user(user_id)

    # 1. Add interaction
    response = agent_ollama.chat("What is the capital of France?")
    assert len(response) > 0

    # 2. Verify Hierarchy
    h_mem = agent_ollama.hierarchical_memory
    assert h_mem is not None

    # Check Episode Layer
    episodes = h_mem.episode_layer.get(None, user_id=user_id)
    assert len(episodes) > 0
    assert "France" in episodes[0]["user_message"]

    # Check Trace Layer (might be empty if categorization fails or is mocked)
    # But with live LLM it should work
    traces = h_mem.trace_layer.get(None, user_id=user_id)
    assert len(traces) > 0

    # Check Category Layer
    categories = h_mem.category_layer.get(None, user_id=user_id)
    assert len(categories) > 0
    # Likely "geography" or "general"

    # Check Domain Layer
    domains = h_mem.domain_layer.get(None, user_id=user_id)
    assert len(domains) > 0


def test_context_injection(agent_ollama):
    """Test that context is correctly retrieved"""
    user_id = "test_context_user"
    agent_ollama.set_user(user_id)

    # Seed memory
    agent_ollama.chat("I love programming in Python.")
    agent_ollama.chat("I also enjoy hiking.")

    # Get context
    context = agent_ollama.hierarchical_memory.get_context(user_id)

    assert "Active Domains" in context
    assert "Recent Topics" in context
    assert "Short-term Memory" in context
    assert "python" in context.lower() or "programming" in context.lower()


# Note: LM Studio test requires a running instance.
# We mark it as skipped if connection fails or explicitly requested.
@pytest.mark.skipif(
    os.environ.get("TEST_LMSTUDIO") != "true", reason="LM Studio tests disabled by default"
)
def test_hierarchy_flow_lmstudio():
    """Test full flow with LM Studio"""
    try:
        agent = MemAgent(
            backend="lmstudio",
            model=LMSTUDIO_MODEL,
            enable_hierarchical_memory=True,
            use_sql=False,
            base_url="http://localhost:1234/v1",
        )

        user_id = "test_user_lmstudio"
        agent.set_user(user_id)

        response = agent.chat("Hello, how are you?")
        assert len(response) > 0

        # Verify layers populated
        assert len(agent.hierarchical_memory.trace_layer.get(None, user_id=user_id)) > 0

    except Exception as e:
        pytest.fail(f"LM Studio test failed: {e}")


if __name__ == "__main__":
    # Manual run for quick debugging
    a = MemAgent(backend="ollama", model=OLLAMA_MODEL, enable_hierarchical_memory=True)
    test_hierarchy_flow_ollama(a)
    print("✅ Manual test passed!")
