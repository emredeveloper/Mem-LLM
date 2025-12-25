from pathlib import Path

from setuptools import find_packages, setup

# Read README.md for long description
import os
from pathlib import Path

# Try multiple possible paths for README.md
readme_path = None
possible_paths = [
    Path(__file__).parent / "Memory LLM" / "README.md",  # Original location
    Path(__file__).parent / "README.md",  # In same directory as setup.py
    Path("Memory LLM") / "README.md",  # Relative path
]

for path in possible_paths:
    if path.exists():
        readme_path = path
        break

long_description = "A powerful Memory LLM library with Hierarchical Memory and Multi-Backend support"
try:
    if readme_path and readme_path.exists():
        with open(readme_path, 'r', encoding="utf-8") as f:
            long_description = f.read()
    else:
        print(f"README.md not found at any of these locations: {[str(p) for p in possible_paths]}")
except Exception as e:
    print(f"Error reading README: {e}")
    # Use a shorter description in case of error
    long_description = "A powerful Memory LLM library with Hierarchical Memory and Multi-Backend support"

setup(
    name="mem-llm",
    version="2.4.0",
    description="Mem-LLM is a Python framework for building privacy-first, memory-enabled AI assistants that run 100% locally.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cihat Emre Karataş",
    packages=find_packages(where="Memory LLM"),
    package_dir={"": "Memory LLM"},
    install_requires=[
        "ollama",
        "chromadb",
        "sentence-transformers",
        "pytest",
        "pyyaml",
        "networkx",
        "psutil",
    ],
    python_requires=">=3.8",
)
