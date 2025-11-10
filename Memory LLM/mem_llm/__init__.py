"""
Memory-LLM: Memory-Enabled Mini Assistant
AI library that remembers user interactions
"""

from .mem_agent import MemAgent
from .memory_manager import MemoryManager
from .llm_client import OllamaClient  # Backward compatibility
from .base_llm_client import BaseLLMClient
from .llm_client_factory import LLMClientFactory

# New multi-backend support (v1.3.0+)
from .clients import OllamaClient as OllamaClientNew
from .clients import LMStudioClient

# Tools (optional)
try:
    from .memory_tools import MemoryTools, ToolExecutor
    __all_tools__ = ["MemoryTools", "ToolExecutor"]
except ImportError:
    __all_tools__ = []

# Pro version imports (optional)
try:
    from .memory_db import SQLMemoryManager
    from .config_manager import get_config
    from .config_from_docs import create_config_from_document
    from .dynamic_prompt import dynamic_prompt_builder
    __all_pro__ = ["SQLMemoryManager", "get_config", "create_config_from_document", "dynamic_prompt_builder"]
except ImportError:
    __all_pro__ = []

# Security features (optional, v1.1.0+)
try:
    from .prompt_security import (
        PromptInjectionDetector,
        InputSanitizer,
        SecurePromptBuilder
    )
    __all_security__ = ["PromptInjectionDetector", "InputSanitizer", "SecurePromptBuilder"]
except ImportError:
    __all_security__ = []

# Enhanced features (v1.1.0+)
try:
    from .logger import get_logger, MemLLMLogger
    from .retry_handler import exponential_backoff_retry, SafeExecutor
    __all_enhanced__ = ["get_logger", "MemLLMLogger", "exponential_backoff_retry", "SafeExecutor"]
except ImportError:
    __all_enhanced__ = []

# Conversation Summarization (v1.2.0+)
try:
    from .conversation_summarizer import ConversationSummarizer, AutoSummarizer
    __all_summarizer__ = ["ConversationSummarizer", "AutoSummarizer"]
except ImportError:
    __all_summarizer__ = []

# Data Export/Import (v1.2.0+)
try:
    from .data_export_import import DataExporter, DataImporter
    __all_export_import__ = ["DataExporter", "DataImporter"]
except ImportError:
    __all_export_import__ = []

# Response Metrics (v1.3.1+)
try:
    from .response_metrics import ChatResponse, ResponseMetricsAnalyzer, calculate_confidence
    __all_metrics__ = ["ChatResponse", "ResponseMetricsAnalyzer", "calculate_confidence"]
except ImportError:
    __all_metrics__ = []

__version__ = "2.1.3"
__author__ = "Cihat Emre Karataş"

# Multi-backend LLM support (v1.3.0+)
__all_llm_backends__ = ["BaseLLMClient", "LLMClientFactory", "OllamaClientNew", "LMStudioClient"]

# Tool system (v2.0.0+)
try:
    from .tool_system import tool, Tool, ToolRegistry
    from .builtin_tools import BUILTIN_TOOLS
    from .tool_workspace import ToolWorkspace, get_workspace, set_workspace
    __all_tools__ = ["tool", "Tool", "ToolRegistry", "BUILTIN_TOOLS", "ToolWorkspace", "get_workspace", "set_workspace"]
except ImportError:
    __all_tools__ = []

# CLI
try:
    from .cli import cli
    __all_cli__ = ["cli"]
except ImportError:
    __all_cli__ = []

__all__ = [
    "MemAgent",
    "MemoryManager", 
    "OllamaClient",
] + __all_llm_backends__ + __all_tools__ + __all_pro__ + __all_cli__ + __all_security__ + __all_enhanced__ + __all_summarizer__ + __all_export_import__ + __all_metrics__