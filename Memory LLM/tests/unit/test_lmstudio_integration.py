import os
import sys

# Ensure parent directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from mem_llm import MemAgent


def test_lmstudio_default_model_logic():
    """Verify that using backend='lmstudio' switches the default model to google/gemma-3-4b."""
    # Initialize without checking connection (offline test)
    agent = MemAgent(backend="lmstudio", check_connection=False)

    assert agent.backend == "lmstudio"
    assert (
        agent.model == "google/gemma-3-4b"
    ), "Default model for LM Studio should be google/gemma-3-4b"


def test_lmstudio_explicit_model_preserved():
    """Verify that providing an explicit model overrides the default switching logic."""
    custom_model = "my-custom-model"
    agent = MemAgent(backend="lmstudio", model=custom_model, check_connection=False)

    assert agent.backend == "lmstudio"
    assert agent.model == custom_model, "Explicit model should be preserved"


def test_ollama_default_preserved():
    """Verify that Ollama default remains unchanged."""
    agent = MemAgent(backend="ollama", check_connection=False)

    assert agent.backend == "ollama"
    assert agent.model == "ministral-3:3b", "Ollama default should be ministral-3:3b"
