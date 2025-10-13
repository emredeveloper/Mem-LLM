"""
Mem-Agent: Memory-Enabled Mini Assistant
AI library that remembers user interactions
"""

from .mem_agent import MemAgent
from .memory_manager import MemoryManager
from .llm_client import OllamaClient

# Tools (optional)
try:
    from .memory_tools import MemoryTools, ToolExecutor
    __all_tools__ = ["MemoryTools", "ToolExecutor"]
except ImportError:
    __all_tools__ = []

# Pro version imports (optional)
try:
    from .memory_db import SQLMemoryManager
    from .prompt_templates import prompt_manager
    from .config_manager import get_config
    __all_pro__ = ["SQLMemoryManager", "prompt_manager", "get_config"]
except ImportError:
    __all_pro__ = []

__version__ = "2.0.0"
__author__ = "C. Emre Karataş"

__all__ = [
    "MemAgent",
    "MemoryManager",
    "OllamaClient",
] + __all_tools__ + __all_pro__

