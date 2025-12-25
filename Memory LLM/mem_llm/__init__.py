"""
Memory-LLM: Memory-Enabled Mini Assistant
AI library that remembers user interactions
"""

from .base_llm_client import BaseLLMClient  # noqa: F401

# New multi-backend support (v1.3.0+)
from .clients import LMStudioClient  # noqa: F401
from .clients import OllamaClient as OllamaClientNew  # noqa: F401
from .llm_client import OllamaClient  # noqa: F401 Backward compatibility
from .llm_client_factory import LLMClientFactory  # noqa: F401
from .mem_agent import MemAgent  # noqa: F401
from .memory_manager import MemoryManager  # noqa: F401

# Tools (optional)
try:
    from .memory_tools import MemoryTools, ToolExecutor  # noqa: F401

    __all_tools__ = ["MemoryTools", "ToolExecutor"]
except ImportError:
    __all_tools__ = []

# Pro version imports (optional)
try:
    from .config_from_docs import create_config_from_document  # noqa: F401
    from .config_manager import get_config  # noqa: F401
    from .dynamic_prompt import dynamic_prompt_builder  # noqa: F401
    from .memory_db import SQLMemoryManager  # noqa: F401

    __all_pro__ = [
        "SQLMemoryManager",
        "get_config",
        "create_config_from_document",
        "dynamic_prompt_builder",
    ]
except ImportError:
    __all_pro__ = []

# Security features (optional, v1.1.0+)
try:
    from .prompt_security import (  # noqa: F401
        InputSanitizer,
        PromptInjectionDetector,
        SecurePromptBuilder,
    )

    __all_security__ = ["PromptInjectionDetector", "InputSanitizer", "SecurePromptBuilder"]
except ImportError:
    __all_security__ = []

# Enhanced features (v1.1.0+)
try:
    from .logger import MemLLMLogger, get_logger  # noqa: F401
    from .retry_handler import SafeExecutor, exponential_backoff_retry  # noqa: F401

    __all_enhanced__ = ["get_logger", "MemLLMLogger", "exponential_backoff_retry", "SafeExecutor"]
except ImportError:
    __all_enhanced__ = []

# Conversation Summarization (v1.2.0+)
try:
    from .conversation_summarizer import AutoSummarizer, ConversationSummarizer  # noqa: F401

    __all_summarizer__ = ["ConversationSummarizer", "AutoSummarizer"]
except ImportError:
    __all_summarizer__ = []

# Data Export/Import (v1.2.0+)
try:
    from .data_export_import import DataExporter, DataImporter  # noqa: F401

    __all_export_import__ = ["DataExporter", "DataImporter"]
except ImportError:
    __all_export_import__ = []

# Response Metrics (v1.3.1+)
try:
    from .response_metrics import (  # noqa: F401
        ChatResponse,
        ResponseMetricsAnalyzer,
        calculate_confidence,
    )

    __all_metrics__ = ["ChatResponse", "ResponseMetricsAnalyzer", "calculate_confidence"]
except ImportError:
    __all_metrics__ = []

__version__ = "2.4.0"
__author__ = "Cihat Emre Karataş"

# Multi-backend LLM support (v1.3.0+)
__all_llm_backends__ = ["BaseLLMClient", "LLMClientFactory", "OllamaClientNew", "LMStudioClient"]

# Tool system (v2.0.0+)
try:
    from .builtin_tools import BUILTIN_TOOLS  # noqa: F401
    from .tool_system import Tool, ToolRegistry, tool  # noqa: F401
    from .tool_workspace import ToolWorkspace, get_workspace, set_workspace  # noqa: F401

    __all_tools__ = [
        "tool",
        "Tool",
        "ToolRegistry",
        "BUILTIN_TOOLS",
        "ToolWorkspace",
        "get_workspace",
        "set_workspace",
    ]
except ImportError:
    __all_tools__ = []

# CLI
try:
    from .cli import cli  # noqa: F401

    __all_cli__ = ["cli"]
except ImportError:
    __all_cli__ = []

# Analytics (v2.1.4+)
try:
    from .config_presets import ConfigPresets  # noqa: F401
    from .conversation_analytics import ConversationAnalytics  # noqa: F401

    __all_analytics__ = ["ConversationAnalytics", "ConfigPresets"]
except ImportError:
    __all_analytics__ = []

# Multi-Agent Systems (v2.2.0+)
try:
    from .multi_agent import (  # noqa: F401
        AgentMessage,
        AgentRegistry,
        AgentRole,
        AgentStatus,
        BaseAgent,
        CommunicationHub,
        MessageQueue,
    )

    __all_multi_agent__ = [
        "BaseAgent",
        "AgentRole",
        "AgentStatus",
        "AgentMessage",
        "AgentRegistry",
        "CommunicationHub",
        "MessageQueue",
    ]
except ImportError:
    __all_multi_agent__ = []

# Hierarchical Memory (v2.2.3+)
try:
    from .memory.hierarchy import AutoCategorizer, HierarchicalMemory  # noqa: F401

    __all_hierarchy__ = ["HierarchicalMemory", "AutoCategorizer"]
except ImportError:
    __all_hierarchy__ = []

# Workflow Engine (v2.3.0+)
try:
    from .workflow import Step, Workflow  # noqa: F401

    __all_workflow__ = ["Workflow", "Step"]
except ImportError:
    __all_workflow__ = []

# Graph Memory (v2.3.0+)
try:
    from .memory.graph import GraphExtractor, GraphStore  # noqa: F401

    __all_graph__ = ["GraphStore", "GraphExtractor"]
except ImportError:
    __all_graph__ = []


__all__ = (
    [
        "MemAgent",
        "MemoryManager",
        "OllamaClient",
    ]
    + __all_llm_backends__
    + __all_tools__
    + __all_pro__
    + __all_cli__
    + __all_security__
    + __all_enhanced__
    + __all_summarizer__
    + __all_export_import__
    + __all_metrics__
    + __all_analytics__
    + __all_multi_agent__
    + __all_hierarchy__
    + __all_workflow__
    + __all_graph__
)
