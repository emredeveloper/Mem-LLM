"""
LLM Clients Package
===================

Multiple LLM backend support for Mem-LLM.

Available Backends:
- OllamaClient: Local Ollama service
- LMStudioClient: LM Studio (OpenAI-compatible)

Author: C. Emre Karataş
Version: 1.3.6
"""

from .lmstudio_client import LMStudioClient
from .ollama_client import OllamaClient

__all__ = [
    "OllamaClient",
    "LMStudioClient",
]
