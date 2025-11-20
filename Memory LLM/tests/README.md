"""
README for Test Suite
======================

This directory contains the test suite for Mem-LLM v2.1.3+.

## Test Structure

```
tests/
├── unit/                   # Unit tests (isolated, fast)
│   ├── test_tool_system.py
│   ├── test_async_tools.py
│   ├── test_memory_manager.py
│   ├── test_vector_store.py
│   ├── test_config_manager.py
│   └── test_response_metrics.py
├── integration/            # Integration tests (with external services)
│   ├── test_ollama_integration.py
│   ├── test_lmstudio_integration.py
│   ├── test_database_integration.py
│   └── test_vector_search_integration.py
├── api/                    # API endpoint tests
│   ├── test_rest_endpoints.py
│   ├── test_websocket.py
│   └── test_streaming.py
└── e2e/                    # End-to-end tests
    ├── test_full_workflow.py
    └── test_multi_user_scenarios.py
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test categories
```bash
# Unit tests only (fast)
pytest -m unit

# Integration tests (requires Ollama/LM Studio)
pytest -m integration

# API tests
pytest -m api

# End-to-end tests
pytest -m e2e

# Async tests
pytest -m asyncio
```

### Run with coverage
```bash
pytest --cov=mem_llm --cov-report=html --cov-report=term-missing
```

### Run specific test file
```bash
pytest tests/unit/test_tool_system.py -v
```

### Run specific test class or function
```bash
pytest tests/unit/test_tool_system.py::TestToolRegistry::test_registry_creation -v
```

## Test Markers

Tests are marked with the following pytest markers:

- `@pytest.mark.unit` - Unit tests (isolated, no external dependencies)
- `@pytest.mark.integration` - Integration tests (require external services)
- `@pytest.mark.api` - API endpoint tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.slow` - Tests that take >5 seconds
- `@pytest.mark.asyncio` - Async tests

## Writing Tests

### Unit Test Example
```python
import pytest
from mem_llm.tool_system import ToolRegistry

@pytest.mark.unit
class TestToolRegistry:
    def test_registry_creation(self):
        registry = ToolRegistry()
        assert registry is not None
```

### Integration Test Example
```python
import pytest
from mem_llm import MemAgent

@pytest.mark.integration
class TestOllamaIntegration:
    def test_chat_with_ollama(self):
        agent = MemAgent(backend='ollama', model='granite4:3b')
        response = agent.chat("Hello")
        assert len(response) > 0
```

### Async Test Example
```python
import pytest

@pytest.mark.asyncio
async def test_async_tool():
    @tool(name="test", description="Test")
    async def async_func(x: int) -> int:
        return x * 2
    
    result = await async_func.execute({"x": 5})
    assert result == 10
```

## Coverage Goals

- **Overall Coverage**: ≥ 80%
- **Unit Tests**: ≥ 90%
- **Integration Tests**: ≥ 70%
- **API Tests**: ≥ 85%

## CI/CD Integration

Tests are automatically run on:
- Every push to `main` or `develop`
- Every pull request
- Weekly schedule (Mondays)

See `.github/workflows/ci.yml` for CI configuration.

## Test Dependencies

Core test dependencies (in `requirements-dev.txt`):
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `pytest-asyncio>=0.21.0` - Async test support
- `pytest-mock>=3.11.0` - Mocking utilities
- `httpx>=0.24.0` - HTTP testing for FastAPI

## Troubleshooting

### Tests fail with ImportError
```bash
pip install -e .
pip install -r requirements-dev.txt
```

### Integration tests fail
Make sure Ollama or LM Studio is running:
```bash
# For Ollama
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

### Coverage report not generated
```bash
# Install coverage dependencies
pip install pytest-cov

# Generate report
pytest --cov=mem_llm --cov-report=html
open htmlcov/index.html  # View in browser
```

## Contributing

When adding new features:
1. Write unit tests first (TDD)
2. Ensure tests pass: `pytest`
3. Check coverage: `pytest --cov`
4. Run linters: `black mem_llm tests && flake8 mem_llm tests`
5. Update this README if needed

## Contact

For questions about testing:
- Open an issue: https://github.com/emredeveloper/Mem-LLM/issues
- Email: karatasqemre@gmail.com
