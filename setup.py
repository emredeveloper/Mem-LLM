from setuptools import find_packages, setup

setup(
    name="mem-llm",
    version="2.2.5",
    description="A powerful Memory LLM library with Hierarchical Memory and Multi-Backend support",
    author="Emre Q",
    packages=find_packages(where="Memory LLM"),
    package_dir={"": "Memory LLM"},
    install_requires=["ollama", "chromadb", "sentence-transformers", "pytest", "pyyaml"],
    python_requires=">=3.8",
)
