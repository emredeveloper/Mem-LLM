# Test Suite README

This directory contains the Mem-LLM test suite.

## Test Structure

```text
tests/
|-- unit/                   # Unit tests (isolated, fast)
|-- integration/            # Integration tests (external services)
|-- api/                    # API endpoint tests
`-- test_multi_agent/       # Multi-agent coverage
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run focused suites
```bash
# Unit tests
pytest tests/unit -q

# Integration tests
pytest tests/integration -q

# API tests
pytest tests/api -q

# LM Studio only
pytest tests -q -s -k "lmstudio and not ollama"
```

### Run with coverage
```bash
pytest --cov=mem_llm --cov-report=html --cov-report=term-missing
```

## Test Dependencies

Core dev dependencies are defined in `pyproject.toml`:
- `pytest>=7.4.0`
- `pytest-cov>=4.1.0`
- `pytest-asyncio>=0.21.0`
- `pytest-mock>=3.11.0`
- `httpx>=0.24.0`

## Troubleshooting

### Import errors
```bash
pip install -e .
pip install -e .[dev]
```

### LM Studio integration tests
Make sure LM Studio is running locally on `http://localhost:1234` and has a model loaded.

### Ollama integration tests
```bash
ollama serve
curl http://localhost:11434/api/tags
```

## Contributing

When adding features or bug fixes:
1. Add or update unit tests.
2. Update integration tests when behavior changes.
3. Keep README examples and version references current.
