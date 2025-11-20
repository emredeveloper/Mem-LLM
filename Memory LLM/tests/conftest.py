"""
Shared pytest fixtures and configuration for all tests.
"""
import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_memory_dir():
    """Create a temporary directory for memory storage."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def temp_db_path(temp_memory_dir):
    """Provide a temporary database path."""
    return str(Path(temp_memory_dir) / "test_memory.db")


@pytest.fixture
def sample_user_id():
    """Provide a sample user ID for tests."""
    return "test_user_123"


@pytest.fixture
def sample_conversation():
    """Provide sample conversation data."""
    return [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi! How can I help you?"},
        {"role": "user", "content": "What's the weather?"},
    ]


@pytest.fixture
def mock_llm_response():
    """Provide a mock LLM response."""
    return "This is a mocked LLM response for testing purposes."


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment before each test."""
    import os

    # Store original env vars
    original_env = os.environ.copy()

    yield

    # Restore original env vars
    os.environ.clear()
    os.environ.update(original_env)


# Markers configuration
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "api: API tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
