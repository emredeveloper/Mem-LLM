# Contributing to Mem-LLM

Thank you for your interest in contributing to Mem-LLM! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/emredeveloper/Mem-LLM/issues)
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, Mem-LLM version)
   - Error messages or logs if applicable

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue with the `feature` label
3. Describe the feature and its use case
4. Explain why it would be valuable

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Write or update tests
5. Run the test suite: `pytest`
6. Run linters: `black mem_llm tests && flake8 mem_llm tests`
7. Commit with clear messages
8. Push and create a Pull Request

## Development Setup

### Prerequisites

- Python 3.10+
- Ollama or LM Studio (for testing)
- Git

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Mem-LLM.git
cd Mem-LLM

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mem_llm --cov-report=html

# Run specific test file
pytest tests/unit/test_tool_system.py -v

# Run by marker
pytest -m unit  # Unit tests only
pytest -m integration  # Integration tests
```

### Code Style

We use the following tools for code quality:

- **Black** - Code formatting (line length: 100)
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking

Run all checks:

```bash
black mem_llm tests
isort mem_llm tests
flake8 mem_llm tests
mypy mem_llm
```

### Commit Messages

Use clear, descriptive commit messages:

- `feat: Add new feature X`
- `fix: Fix bug in Y`
- `docs: Update README`
- `test: Add tests for Z`
- `refactor: Improve code structure`

## Project Structure

```
mem_llm/
├── mem_agent.py          # Main agent class
├── clients/              # LLM backend clients
├── memory/               # Memory systems
├── multi_agent/          # Multi-agent framework
├── tool_system.py        # Function calling
├── api_server.py         # REST API
└── web_ui/               # Web interface
```

## Testing Guidelines

- Write unit tests for new functionality
- Maintain test coverage above 80%
- Use meaningful test names
- Include both positive and negative test cases

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update CHANGELOG.md for releases

## Questions?

- Open an issue for questions
- Email: karatasqemre@gmail.com
- GitHub: [@emredeveloper](https://github.com/emredeveloper)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
