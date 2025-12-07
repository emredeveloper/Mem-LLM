from pathlib import Path
from setuptools import find_packages, setup

# Read README.md for long description
readme_file = Path(__file__).parent / "Memory LLM" / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="mem-llm",
    version="2.2.7",
    description="A powerful Memory LLM library with Hierarchical Memory and Multi-Backend support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Emre Q",
    packages=find_packages(where="Memory LLM"),
    package_dir={"": "Memory LLM"},
    install_requires=["ollama", "chromadb", "sentence-transformers", "pytest", "pyyaml"],
    python_requires=">=3.10",
)
