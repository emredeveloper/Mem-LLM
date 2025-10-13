"""
Setup script for Memory-LLM package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="mem-llm",
    version="1.0.0",
    author="C. Emre Karataş",
    author_email="karatasqemre@gmail.com",  # PyPI için gerekli - kendi emailinizi yazın
    description="Memory-enabled AI assistant with local LLM support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emredeveloper/Mem-LLM",
    packages=find_packages(exclude=['tests*', 'examples*', 'docs*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "pyyaml>=6.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
        ],
    },
    include_package_data=True,
    package_data={
        'memory_llm': ['config.yaml.example'],
    },
    keywords="llm ai memory agent chatbot ollama local",
    project_urls={
        "Bug Reports": "https://github.com/emredeveloper/Mem-LLM/issues",
        "Source": "https://github.com/emredeveloper/Mem-LLM",
    },
)
