"""
Mem-Agent: Unified Powerful System
==================================

A powerful Mem-Agent that combines all features in a single system.

Features:
- ✅ SQL and JSON memory support
- ✅ Prompt templates system
- ✅ Knowledge base integration
- ✅ User tools system
- ✅ Configuration management
- ✅ Advanced logging
- ✅ Production-ready structure

Usage:
```python
from memory_llm import MemAgent

# Simple usage
agent = MemAgent()

# Advanced usage
agent = MemAgent(
    config_file="config.yaml",
    use_sql=True,
    load_knowledge_base=True
)
```
"""

import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, Iterator, List, Optional, Union

from .llm_client import OllamaClient  # noqa: F401 Backward compatibility
from .llm_client_factory import LLMClientFactory

# Core dependencies
from .memory_manager import MemoryManager
from .response_metrics import ChatResponse, ResponseMetricsAnalyzer, calculate_confidence
from .tool_system import ToolCallParser, ToolRegistry, format_tools_for_prompt

# Advanced features (optional)
ADVANCED_AVAILABLE = False
GRAPH_AVAILABLE = False
VOICE_AVAILABLE = False

try:
    from .config_manager import get_config
    from .dynamic_prompt import dynamic_prompt_builder
    from .knowledge_loader import KnowledgeLoader
    from .memory.hierarchy import HierarchicalMemory
    from .memory_db import SQLMemoryManager
    from .memory_tools import ToolExecutor

    ADVANCED_AVAILABLE = True

    # New features v2.3.0 - Managed separately to allow partial failures
    try:
        from .memory.graph import GraphExtractor, GraphStore

        GRAPH_AVAILABLE = True
    except ImportError as e:
        print(f"⚠️  Graph features not available (missing dependency): {e}")

except ImportError as e:
    print(f"⚠️  Advanced features not available (install additional packages): {e}")


class MemAgent:
    """
    Powerful and unified Mem-Agent system

    Production-ready assistant that combines all features in one place.
    """

    def __init__(
        self,
        model: str = "rnj-1:latest",
        backend: str = "ollama",
        config_file: Optional[str] = None,
        use_sql: bool = True,
        memory_dir: Optional[str] = None,
        db_path: Optional[str] = None,
        load_knowledge_base: bool = True,
        ollama_url: str = "http://localhost:11434",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        auto_detect_backend: bool = False,
        check_connection: bool = False,
        enable_security: bool = False,
        enable_vector_search: bool = False,
        embedding_model: str = "nomic-embed-text-v2-moe:latest",
        enable_tools: bool = False,
        tools: Optional[List] = None,
        preset: Optional[str] = None,
        enable_hierarchical_memory: bool = False,
        enable_graph_memory: bool = False,
        **llm_kwargs,
    ):
        """
        Args:
            model: LLM model to use
            backend: LLM backend ('ollama', 'lmstudio') - NEW in v1.3.0
            config_file: Configuration file (optional)
            use_sql: Use SQL database (True) or JSON (False)
            memory_dir: Memory directory (for JSON mode or if db_path not specified)
            db_path: SQLite database path (for SQL mode, e.g., ":memory:" or "path/to/db.db")
            load_knowledge_base: Automatically load knowledge base
            ollama_url: Ollama API URL (backward compatibility, use base_url instead)
            base_url: Backend API URL (for local backends) - NEW in v1.3.0
            auto_detect_backend: Auto-detect available LLM backend - NEW in v1.3.0
            check_connection: Verify LLM connection on startup (default: False)
            enable_security: Enable prompt injection protection
                (v1.1.0+, default: False for compatibility)
            enable_vector_search: Enable semantic/vector search for KB
                (v1.3.2+, requires chromadb) - NEW
            embedding_model: Embedding model for vector search
                (default: "nomic-embed-text-v2-moe:latest") - NEW
            preset: Configuration preset name (e.g., 'chatbot', 'code_assistant') - NEW in v2.1.4
            **llm_kwargs: Additional backend-specific parameters

        Examples:
            # Default Ollama
            agent = MemAgent()

            # LM Studio
            agent = MemAgent(backend='lmstudio', model='llama-3-8b')

            # Using Preset
            agent = MemAgent(preset='code_assistant')
        """

        # Setup logging first
        self._setup_logging()

        # Load preset configuration if specified (v2.1.4)
        self.preset_config = {}
        if preset:
            try:
                from .config_presets import ConfigPresets

                presets = ConfigPresets()
                self.preset_config = presets.get_preset(preset)
                self.logger.info(f"📋 Loaded configuration preset: {preset}")

                # Apply preset settings if not explicitly provided
                if "temperature" in self.preset_config and "temperature" not in llm_kwargs:
                    llm_kwargs["temperature"] = self.preset_config["temperature"]

                if "max_tokens" in self.preset_config and "max_tokens" not in llm_kwargs:
                    llm_kwargs["max_tokens"] = self.preset_config["max_tokens"]

                # Note: System prompt and tools are handled later
            except Exception as e:
                self.logger.warning(f"⚠️  Failed to load preset '{preset}': {e}")

        # Security features (v1.1.0+)
        self.enable_security = enable_security
        self.security_detector = None
        self.security_sanitizer = None

        if enable_security:
            try:
                from .prompt_security import InputSanitizer, PromptInjectionDetector

                self.security_detector = PromptInjectionDetector()
                self.security_sanitizer = InputSanitizer()
                self.logger.info("🔒 Security features enabled (prompt injection protection)")
            except ImportError:
                self.logger.warning("⚠️  Security features requested but not available")

        # Load configuration
        self.config = None
        if ADVANCED_AVAILABLE and config_file:
            try:
                self.config = get_config(config_file)
            except Exception:
                print("⚠️  Config file could not be loaded, using default settings")

        # Determine usage mode
        self.usage_mode = "business"  # default
        if self.config:
            self.usage_mode = self.config.get("usage_mode", "business")
        elif config_file:
            # Config file exists but couldn't be loaded
            self.usage_mode = "business"
        else:
            # No config file
            self.usage_mode = "personal"

        # Initialize flags first
        self.has_knowledge_base: bool = False  # Track KB status
        self.has_tools: bool = False  # Track tools status (v1.3.x)
        self.enable_hierarchical_memory = enable_hierarchical_memory

        # Tool system (v2.0.0+)
        # Preset can enable tools if not explicitly disabled
        preset_tools_enabled = self.preset_config.get("tools_enabled", False)
        self.enable_tools = enable_tools or preset_tools_enabled

        self.tool_registry = None
        if self.enable_tools:
            self.tool_registry = ToolRegistry()
            self.has_tools = True

            # Register custom tools if provided
            if tools:
                for tool in tools:
                    self.tool_registry.register_function(tool)
                self.logger.info(
                    f"Successfully loaded {len(self.tool_registry.tools)} tool(s): "
                    f"{[t for t in self.tool_registry.tools.keys()]}"
                )

            builtin_count = len(self.tool_registry.tools)
            self.logger.info(f"🛠️  Tool system enabled ({builtin_count} tools available)")

        # Memory system
        if use_sql and ADVANCED_AVAILABLE:
            # SQL memory (advanced)
            # Determine database path
            if db_path:
                # Use provided db_path (can be ":memory:" for in-memory DB)
                final_db_path = db_path
            elif memory_dir:
                final_db_path = memory_dir
            elif self.config:
                final_db_path = self.config.get("memory.db_path", "memories/memories.db")
            else:
                final_db_path = "memories/memories.db"

            # Get vector search settings from config or parameters
            vector_search_enabled = enable_vector_search
            vector_model = embedding_model

            if self.config:
                vector_search_enabled = self.config.get(
                    "knowledge_base.enable_vector_search", vector_search_enabled
                )
                vector_model = self.config.get("knowledge_base.embedding_model", vector_model)

            # Ensure memories directory exists (skip for :memory:)
            import os

            if final_db_path != ":memory:":
                db_dir = os.path.dirname(final_db_path)
                if db_dir and not os.path.exists(db_dir):
                    os.makedirs(db_dir, exist_ok=True)

            self.memory = SQLMemoryManager(
                final_db_path,
                enable_vector_search=vector_search_enabled,
                embedding_model=vector_model,
            )
            self.logger.info(f"SQL memory system active: {final_db_path}")
            if vector_search_enabled:
                self.logger.info(f"Vector search enabled using model: {vector_model}")
        else:
            # JSON memory (simple)
            json_dir = (
                memory_dir or self.config.get("memory.json_dir", "memories")
                if self.config
                else "memories"
            )
            self.memory = MemoryManager(json_dir)
            self.logger.info(f"JSON memory system active: {json_dir}")

        # Active user and system prompt
        self.current_user: Optional[str] = None
        self.current_system_prompt: Optional[str] = None

        # LLM client
        self.model = model  # Store model name
        self.backend = backend  # Store backend name
        self.use_sql = use_sql  # Store SQL usage flag

        # Default model for LM Studio (v2.3.0)
        if self.backend == "lmstudio" and self.model == "rnj-1:latest":
            self.model = "google/gemma-3-4b"
            self.logger.info(f"🔄 Switched to default LM Studio model: {self.model}")

        # Initialize LLM client (v1.3.0: Multi-backend support)
        # Prepare backend configuration
        llm_config = llm_kwargs.copy()

        # Handle backward compatibility: ollama_url -> base_url
        if base_url is None and backend == "ollama":
            base_url = ollama_url

        # Add base_url for local backends
        if base_url and backend in ["ollama", "lmstudio"]:
            llm_config["base_url"] = base_url

        # Add api_key for cloud backends
        # Auto-detect backend if requested
        if auto_detect_backend:
            self.logger.info("🔍 Auto-detecting available LLM backend...")
            self.llm = LLMClientFactory.auto_detect()
            if self.llm:
                detected_backend = self.llm.__class__.__name__
                self.logger.info(f"✅ Detected and using: {detected_backend}")
            else:
                self.logger.error("❌ No LLM backend available.")
                raise RuntimeError(
                    "No LLM backend detected. Please start a local LLM service "
                    "(Ollama or LM Studio)."
                )
        else:
            # Create client using factory
            try:
                # Use self.model which might have been updated (e.g. LM Studio default)
                self.llm = LLMClientFactory.create(backend=backend, model=self.model, **llm_config)
                self.logger.info(f"✅ Initialized {backend} backend with model: {self.model}")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize {backend} backend: {e}")
                raise

        # Optional connection check on startup
        if check_connection:
            backend_name = backend if not auto_detect_backend else "LLM service"
            self.logger.info(f"Checking {backend_name} connection...")
            if not self.llm.check_connection():
                error_msg = f"❌ ERROR: Cannot connect to {backend_name}!\n"

                if backend == "ollama":
                    error_msg += (
                        "   \n"
                        "   Solutions:\n"
                        "   1. Start Ollama: ollama serve\n"
                        "   2. Check if Ollama is running: http://localhost:11434\n"
                        "   3. Verify base_url parameter is correct\n"
                    )
                elif backend == "lmstudio":
                    error_msg += (
                        "   \n"
                        "   Solutions:\n"
                        "   1. Start LM Studio\n"
                        "   2. Load a model in LM Studio\n"
                        "   3. Start local server (default: http://localhost:1234)\n"
                        "   4. Verify base_url parameter is correct\n"
                    )

                error_msg += "   \n   To skip this check, use: MemAgent(check_connection=False)"
                self.logger.error(error_msg)
                raise ConnectionError(f"{backend_name} not available")

            # Check if model exists (for backends that support listing)
            try:
                available_models = self.llm.list_models()
                if available_models and self.model not in available_models:
                    error_msg = (
                        f"❌ ERROR: Model '{self.model}' not found in {backend}!\n"
                        f"   \n"
                        f"   Available models: {', '.join(available_models[:5])}\n"
                        f"   Total: {len(available_models)} models available\n"
                        f"   \n"
                        f"   To skip this check, use: MemAgent(check_connection=False)"
                    )
                    self.logger.error(error_msg)
                    raise ValueError(f"Model '{self.model}' not available")
            except Exception:
                # Some backends may not support list_models, skip check
                pass

            self.logger.info(f"✅ {backend_name} connection verified, model '{self.model}' ready")

        self.logger.info(f"LLM client ready: {self.model} on {backend}")

        # Advanced features (if available)
        if ADVANCED_AVAILABLE:
            self._setup_advanced_features(load_knowledge_base)
        else:
            print("⚠️  Load additional packages for advanced features")
            # Build basic prompt even without advanced features
            self._build_dynamic_system_prompt()

        # Tool system (always available)
        self.tool_executor = ToolExecutor(self.memory)

        # Initialize Hierarchical Memory if enabled (after memory and LLM are ready)
        if self.enable_hierarchical_memory and ADVANCED_AVAILABLE:
            self.hierarchical_memory = HierarchicalMemory(self.memory, self.llm)
            self.logger.info("🧠 Hierarchical Memory System enabled")
        else:
            self.hierarchical_memory = None

        # Metrics tracking system (v1.3.1+)
        self.metrics_analyzer = ResponseMetricsAnalyzer()
        self.track_metrics = True  # Can be disabled if needed

        # Graph Memory (v2.3.0)
        self.graph_store = None
        self.graph_extractor = None
        if enable_graph_memory and ADVANCED_AVAILABLE and GRAPH_AVAILABLE:
            # Determine graph path based on memory configuration
            graph_path = "memories/graph.json"
            if use_sql and db_path and db_path != ":memory:":
                # Use same dir as DB
                import os

                db_dir = os.path.dirname(db_path)
                if db_dir:
                    graph_path = os.path.join(db_dir, "graph.json")
            elif memory_dir:
                import os

                graph_path = os.path.join(memory_dir, "graph.json")

            self.graph_store = GraphStore(persistence_path=graph_path)
            self.graph_extractor = GraphExtractor(self)
            self.logger.info(f"🕸️ Graph Memory enabled (path: {graph_path})")

        self.logger.info("MemAgent successfully initialized")

    # === UNIFIED SYSTEM METHODS ===

    def _setup_logging(self) -> None:
        """Setup logging system"""
        log_config = {}
        if ADVANCED_AVAILABLE and hasattr(self, "config") and self.config:
            log_config = self.config.get("logging", {})

        # Default to WARNING level to keep console clean (users can override in config)
        default_level = "WARNING"

        if log_config.get("enabled", True):
            # Only console logging (no file) - keep workspace clean
            logging.basicConfig(
                level=getattr(logging, log_config.get("level", default_level)),
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                handlers=[logging.StreamHandler()],  # Console only
            )

        self.logger = logging.getLogger("MemAgent")

        # Set default level for mem_llm loggers
        logging.getLogger("mem_llm").setLevel(
            getattr(logging, log_config.get("level", default_level))
        )

    def _setup_advanced_features(self, load_knowledge_base: bool) -> None:
        """Setup advanced features"""
        # Load knowledge base (according to usage mode)
        if load_knowledge_base:
            kb_loader = KnowledgeLoader(self.memory)

            # Get KB settings from config
            if hasattr(self, "config") and self.config:
                kb_config = self.config.get("knowledge_base", {})

                # Select default KB according to usage mode
                if self.usage_mode == "business":
                    default_kb = kb_config.get("default_kb", "business_tech_support")
                else:  # personal
                    default_kb = kb_config.get("default_kb", "personal_learning")

                try:
                    if default_kb == "ecommerce":
                        count = kb_loader.load_default_ecommerce_kb()
                        self.logger.info(f"E-commerce knowledge base loaded: {count} records")
                        self.has_knowledge_base = True  # KB loaded!
                    elif default_kb == "tech_support":
                        count = kb_loader.load_default_tech_support_kb()
                        self.logger.info(
                            f"Technical support knowledge base loaded: {count} records"
                        )
                        self.has_knowledge_base = True  # KB loaded!
                    elif default_kb == "business_tech_support":
                        count = kb_loader.load_default_tech_support_kb()
                        self.logger.info(
                            f"Corporate technical support knowledge base loaded: {count} records"
                        )
                        self.has_knowledge_base = True  # KB loaded!
                    elif default_kb == "personal_learning":
                        # Simple KB for personal learning
                        count = kb_loader.load_default_ecommerce_kb()  # Temporarily use the same KB
                        self.logger.info(
                            f"Personal learning knowledge base loaded: {count} records"
                        )
                        self.has_knowledge_base = True  # KB loaded!
                except Exception as e:
                    self.logger.error(f"Knowledge base loading error: {e}")
                self.has_knowledge_base = False

        # Build dynamic system prompt based on active features
        self._build_dynamic_system_prompt()

    def _build_dynamic_system_prompt(self) -> None:
        """Build dynamic system prompt based on active features"""
        # Check if preset system prompt is available (v2.1.4)
        if (
            hasattr(self, "preset_config")
            and self.preset_config
            and "system_prompt" in self.preset_config
        ):
            base_prompt = self.preset_config["system_prompt"]

            # Add tool information if tools are enabled
            if self.enable_tools and self.tool_registry:
                tools_list = self.tool_registry.list_tools()
                tools_prompt = format_tools_for_prompt(tools_list)
                base_prompt += f"\n\n{tools_prompt}"

            self.current_system_prompt = base_prompt
            self.logger.info("📋 Using preset system prompt")
            return

        if not ADVANCED_AVAILABLE:
            # Fallback simple prompt
            self.current_system_prompt = "You are a helpful AI assistant."
            return

        # Get config data
        business_config = None
        personal_config = None

        if hasattr(self, "config") and self.config:
            if self.usage_mode == "business":
                business_config = self.config.get("business", {})
            else:
                personal_config = self.config.get("personal", {})

        # Check if tools are enabled (future feature)
        # For now, tools are always available but not advertised in prompt
        # self.has_tools = False  # Will be enabled when tool system is ready

        # Build prompt using dynamic builder
        try:
            self.current_system_prompt = dynamic_prompt_builder.build_prompt(
                usage_mode=self.usage_mode,
                has_knowledge_base=self.has_knowledge_base,
                has_tools=self.enable_tools,  # Now advertised when enabled (v2.0+)
                is_multi_user=False,  # Always False for now, per-session state
                business_config=business_config,
                personal_config=personal_config,
                memory_type="sql" if self.use_sql else "json",
            )

            # Add tool information to prompt if tools are enabled (v2.0+)
            if self.enable_tools and self.tool_registry:
                tools_list = self.tool_registry.list_tools()
                tools_prompt = format_tools_for_prompt(tools_list)
                self.current_system_prompt += f"\n\n{tools_prompt}"

            # Log feature summary
            feature_summary = dynamic_prompt_builder.get_feature_summary(
                has_knowledge_base=self.has_knowledge_base,
                has_tools=self.enable_tools,
                is_multi_user=False,
                memory_type="sql" if self.use_sql else "json",
            )
            self.logger.info(f"Dynamic prompt built: {feature_summary}")

        except Exception as e:
            self.logger.error(f"Dynamic prompt building error: {e}")
            # Fallback
            self.current_system_prompt = "You are a helpful AI assistant."

    def check_setup(self) -> Dict[str, Any]:
        """Check system setup"""
        ollama_running = self.llm.check_connection()
        models = self.llm.list_models()
        model_exists = self.llm.model in models

        # Memory statistics
        try:
            if hasattr(self.memory, "get_statistics"):
                stats = self.memory.get_statistics()
            else:
                # Simple statistics for JSON memory
                stats = {"total_users": 0, "total_interactions": 0, "knowledge_base_entries": 0}
        except Exception:
            stats = {"total_users": 0, "total_interactions": 0, "knowledge_base_entries": 0}

        return {
            "ollama_running": ollama_running,
            "available_models": models,
            "target_model": self.llm.model,
            "model_ready": model_exists,
            "memory_backend": (
                "SQL"
                if ADVANCED_AVAILABLE and isinstance(self.memory, SQLMemoryManager)
                else "JSON"
            ),
            "total_users": stats.get("total_users", 0),
            "total_interactions": stats.get("total_interactions", 0),
            "kb_entries": stats.get("knowledge_base_entries", 0),
            "status": "ready" if (ollama_running and model_exists) else "not_ready",
        }

    def set_user(self, user_id: str, name: Optional[str] = None) -> None:
        """
        Set active user

        Args:
            user_id: User ID
            name: User name (optional)
        """
        self.current_user = user_id

        # Add user for SQL memory
        if ADVANCED_AVAILABLE and isinstance(self.memory, SQLMemoryManager):
            self.memory.add_user(user_id, name)

        # Update user name (if provided)
        if name:
            if hasattr(self.memory, "update_user_profile"):
                self.memory.update_user_profile(user_id, {"name": name})

        self.logger.debug(f"Active user set: {user_id}")

    def _execute_tool_calls(self, response_text: str, max_iterations: int = 3) -> str:
        """
        Execute tool calls found in LLM response and get results.

        Args:
            response_text: LLM response that may contain tool calls
            max_iterations: Maximum number of tool execution iterations

        Returns:
            Final response after all tool executions
        """
        iteration = 0
        current_text = response_text

        while iteration < max_iterations:
            # Check if response contains tool calls
            if not ToolCallParser.has_tool_call(current_text):
                break

            # Parse tool calls
            tool_calls = ToolCallParser.parse(current_text)
            if not tool_calls:
                break

            self.logger.info(f"🔧 Detected {len(tool_calls)} tool call(s)")

            # Execute each tool
            tool_results = []
            for call in tool_calls:
                tool_name = call["tool"]
                arguments = call["arguments"]

                self.logger.info(f"  Executing: {tool_name}({arguments})")

                # Check if tool exists before executing
                if not self.tool_registry.get(tool_name):
                    self.logger.warning(f"Tool '{tool_name}' not found in registry. Available tools: {list(self.tool_registry.tools.keys())}")
                    # Skip this tool call and continue with others
                    continue

                # Execute tool
                result = self.tool_registry.execute(tool_name, **arguments)

                # Handle memory-specific tools
                if result.status.value == "success" and isinstance(result.result, str):
                    if result.result.startswith("MEMORY_SEARCH:"):
                        keyword = result.result.split(":", 1)[1]
                        try:
                            search_results = self.memory_manager.search_conversations(keyword)
                            if search_results:
                                formatted = (
                                    f"Found {len(search_results)} results for '{keyword}':\n"
                                )
                                for idx, conv in enumerate(search_results[:5], 1):
                                    msg_preview = conv.get("message", "N/A")[:100]
                                    user_name = conv.get("user", "N/A")
                                    formatted += f"{idx}. {user_name}: {msg_preview}...\n"
                                result.result = formatted
                            else:
                                result.result = f"No conversations found containing '{keyword}'"
                        except Exception as e:
                            result.result = f"Memory search error: {e}"

                    elif result.result == "MEMORY_USER_INFO":
                        try:
                            user_info = f"Current user: {self.current_user or 'Not set'}"
                            if self.current_user:
                                conv_count = len(
                                    self.memory_manager.get_conversation_history(self.current_user)
                                )
                                user_info += f"\nTotal conversations: {conv_count}"
                            result.result = user_info
                        except Exception as e:
                            result.result = f"User info error: {e}"

                    elif result.result.startswith("MEMORY_LIST_CONVERSATIONS:"):
                        try:
                            limit = int(result.result.split(":", 1)[1])
                            history = self.memory_manager.get_conversation_history(
                                self.current_user or "default", limit=limit
                            )
                            if history:
                                formatted = f"Last {len(history)} conversations:\n"
                                for idx, conv in enumerate(history, 1):
                                    role = conv.get("role", "unknown")
                                    msg = conv.get("content", "")[:80]
                                    formatted += f"{idx}. [{role}] {msg}...\n"
                                result.result = formatted
                            else:
                                result.result = "No conversation history found"
                        except Exception as e:
                            result.result = f"Conversation list error: {e}"

                if result.status.value == "success":  # Compare with enum value
                    self.logger.info(f"  ✅ Success: {result.result}")
                    tool_results.append(f"Tool '{tool_name}' returned: {result.result}")
                else:
                    self.logger.warning(f"  ❌ Error: {result.error}")
                    tool_results.append(f"Tool '{tool_name}' failed with error: {result.error}")

            # Remove tool call syntax from response
            clean_text = ToolCallParser.remove_tool_calls(current_text)

            # If we have tool results, ask LLM to continue with the results
            if tool_results:
                results_text = "\n".join(tool_results)

                # Build follow-up message for LLM
                follow_up = (
                    f"{clean_text}\n\nTool Results:\n{results_text}\n\n"
                    "Please provide the final answer to the user based on these results."
                )

                # Get LLM response with tool results
                try:
                    messages = [
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful assistant. "
                                "Use the tool results to answer the user's question."
                            ),
                        },
                        {"role": "user", "content": follow_up},
                    ]

                    llm_response = self.llm.chat(messages=messages, temperature=0.7, max_tokens=500)

                    current_text = llm_response
                    iteration += 1
                except Exception as e:
                    self.logger.error(f"Error getting follow-up response: {e}")
                    # Return what we have
                    return f"{clean_text}\n\n{results_text}"
            else:
                # No tool results, return clean text
                return clean_text

        return current_text

    def chat(
        self,
        message: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
        return_metrics: bool = False,
    ) -> Union[str, ChatResponse]:
        """
        Chat with user

        Args:
            message: User's message
            user_id: User ID (optional)
            metadata: Additional information
            return_metrics: If True, returns ChatResponse with metrics; if False,
                            returns only text (default)

        Returns:
            Bot's response (str) or ChatResponse object with metrics
        """
        # Start timing
        start_time = time.time()
        # Determine user
        if user_id:
            self.set_user(user_id)
        elif not self.current_user:
            error_response = "Error: User ID not specified."
            if return_metrics:
                return ChatResponse(
                    text=error_response,
                    confidence=1.0,
                    source="tool",
                    latency=(time.time() - start_time) * 1000,
                    timestamp=datetime.now(),
                    kb_results_count=0,
                    metadata={"error": True},
                )
            return error_response

        user_id = self.current_user

        # Initialize tracking variables
        kb_results_count = 0
        used_kb = False
        used_memory = False
        response_source = "model"  # Default source

        # Security check (v1.1.0+) - opt-in
        # Security check (v1.1.0+) - opt-in
        if self.enable_security and self.security_detector and self.security_sanitizer:
            # Detect injection attempts
            risk_level = self.security_detector.get_risk_level(message)
            is_suspicious, patterns = self.security_detector.detect(message)

            if risk_level in ["high", "critical"]:
                self.logger.warning(
                    f"🚨 Blocked {risk_level} risk input from {user_id}: "
                    f"{len(patterns)} patterns detected"
                )
                return (
                    "⚠️ Your message was blocked due to security concerns. "
                    "Please rephrase your request."
                )

            if is_suspicious:
                self.logger.info(
                    f"⚠️ Suspicious input from {user_id} (risk: {risk_level}): "
                    f"{len(patterns)} patterns"
                )

            # Sanitize input
            original_message = message
            message = self.security_sanitizer.sanitize(message, aggressive=(risk_level == "medium"))

            if message != original_message:
                self.logger.debug(f"Input sanitized for {user_id}")

            _ = {  # noqa: F841
                "risk_level": risk_level,
                "sanitized": message != original_message,
                "patterns_detected": len(patterns),
            }

        # Check tool commands first
        tool_result = self.tool_executor.execute_user_command(message, user_id)
        if tool_result:
            latency = (time.time() - start_time) * 1000
            if return_metrics:
                return ChatResponse(
                    text=tool_result,
                    confidence=0.95,  # Tools are deterministic
                    source="tool",
                    latency=latency,
                    timestamp=datetime.now(),
                    kb_results_count=0,
                    metadata={"tool_command": True},
                )
            return tool_result

        # Knowledge base search (if using SQL)
        kb_context = ""
        if ADVANCED_AVAILABLE and isinstance(self.memory, SQLMemoryManager):
            # Check config only if it exists, otherwise always use KB
            use_kb = True
            kb_limit = 5

            if hasattr(self, "config") and self.config:
                use_kb = self.config.get("response.use_knowledge_base", True)
                kb_limit = self.config.get("knowledge_base.search_limit", 5)

            if use_kb:
                try:
                    kb_results = self.memory.search_knowledge(query=message, limit=kb_limit)

                    if kb_results:
                        kb_results_count = len(kb_results)
                        used_kb = True
                        kb_context = "\n\n📚 RELEVANT KNOWLEDGE BASE:\n"
                        for i, result in enumerate(kb_results, 1):
                            kb_context += (
                                f"{i}. Q: {result['question']}\n   A: {result['answer']}\n"
                            )
                        kb_context += (
                            "\n⚠️ USE THIS INFORMATION TO ANSWER! Be brief but accurate.\n"
                        )
                except Exception as e:
                    self.logger.error(f"Knowledge base search error: {e}")

        # Rebuild system prompt to include any newly registered tools (v2.1.1+)
        if self.enable_tools and self.tool_registry:
            self._build_dynamic_system_prompt()

        # Get conversation history
        messages = []
        if self.current_system_prompt:
            messages.append({"role": "system", "content": self.current_system_prompt})

        # Add memory history
        try:
            if hasattr(self.memory, "get_recent_conversations"):
                recent_limit = (
                    self.config.get("response.recent_conversations_limit", 5)
                    if hasattr(self, "config") and self.config
                    else 5
                )
                recent_convs = self.memory.get_recent_conversations(user_id, recent_limit)

                if recent_convs:
                    used_memory = True

                # Add conversations in chronological order (oldest first)
                for conv in recent_convs:
                    messages.append({"role": "user", "content": conv.get("user_message", "")})
                    messages.append({"role": "assistant", "content": conv.get("bot_response", "")})
        except Exception as e:
            self.logger.error(f"Memory history loading error: {e}")

        # Add current message WITH knowledge base context (if available)
        final_message = message
        if kb_context:
            # Inject KB directly into user message for maximum visibility
            final_message = f"{kb_context}\n\nUser Question: {message}"

        messages.append({"role": "user", "content": final_message})

        # Get response from LLM
        temperature = (
            self.config.get("llm.temperature", 0.2)
            if hasattr(self, "config") and self.config
            else 0.2
        )
        try:
            response = self.llm.chat(
                messages=messages,
                temperature=temperature,
                max_tokens=(
                    self.config.get("llm.max_tokens", 2000)
                    if hasattr(self, "config") and self.config
                    else 2000
                ),  # Enough tokens for thinking models
            )

            # Fallback: If response is empty (can happen with thinking models)
            if not response or response.strip() == "":
                self.logger.warning(
                    f"Empty response from model {self.llm.model}, retrying with simpler prompt..."
                )

                # Retry with just the current message, no history
                simple_messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Respond directly and concisely.",
                    },
                    {"role": "user", "content": message},
                ]
                response = self.llm.chat(simple_messages, temperature=0.7, max_tokens=2000)

                # If still empty, provide fallback
                if not response or response.strip() == "":
                    response = (
                        "I'm having trouble responding right now. Could you rephrase your question?"
                    )
                    self.logger.error(
                        f"Model {self.llm.model} returned empty response even after retry"
                    )

        except Exception as e:
            self.logger.error(f"LLM response error: {e}")
            response = "Sorry, I cannot respond right now. Please try again later."

        # Execute tool calls if tools are enabled (v2.0+)
        if self.enable_tools and self.tool_registry and response:
            try:
                response = self._execute_tool_calls(response)
            except Exception as e:
                self.logger.error(f"Tool execution error: {e}")
                # Continue with original response

        # Calculate latency
        latency = (time.time() - start_time) * 1000

        # Determine response source
        if used_kb and used_memory:
            response_source = "hybrid"
        elif used_kb:
            response_source = "knowledge_base"
        else:
            response_source = "model"

        # Calculate confidence score
        confidence = calculate_confidence(
            kb_results_count=kb_results_count,
            temperature=temperature,
            used_memory=used_memory,
            response_length=len(response),
        )

        # Build enriched metadata with response metrics
        enriched_metadata = {}
        if metadata:
            enriched_metadata.update(metadata)
        enriched_metadata.update(
            {
                "confidence": round(confidence, 3),
                "source": response_source,
                "latency_ms": round(latency, 1),
                "kb_results_count": kb_results_count,
                "used_memory": used_memory,
                "used_kb": used_kb,
                "response_length": len(response),
                "model": self.model,
                "temperature": temperature,
            }
        )

        # Save interaction
        try:
            if self.hierarchical_memory:
                # Use hierarchical memory manager
                self.hierarchical_memory.add_interaction(
                    user_id=user_id,
                    user_message=message,
                    bot_response=response,
                    metadata=enriched_metadata,
                )
            elif hasattr(self.memory, "add_interaction"):
                self.memory.add_interaction(
                    user_id=user_id,
                    user_message=message,
                    bot_response=response,
                    metadata=enriched_metadata,
                )

                # Extract and save user info to profile
                self._update_user_profile(user_id, message, response)

                # Update graph memory (v2.3.0)
                self._update_graph_memory(message, response)

                # Always update summary after each conversation (JSON mode)
                if not self.use_sql and hasattr(self.memory, "conversations"):
                    self._update_conversation_summary(user_id)
                    # Save summary update
                    if user_id in self.memory.user_profiles:
                        self.memory.save_memory(user_id)
        except Exception as e:
            self.logger.error(f"Interaction saving error: {e}")

        # Create response metrics object
        chat_response = ChatResponse(
            text=response,
            confidence=confidence,
            source=response_source,
            latency=latency,
            timestamp=datetime.now(),
            kb_results_count=kb_results_count,
            metadata={
                "model": self.model,
                "temperature": temperature,
                "used_memory": used_memory,
                "used_kb": used_kb,
                "user_id": user_id,
            },
        )

        # Track metrics if enabled
        if self.track_metrics:
            self.metrics_analyzer.add_metric(chat_response)

        # Return based on user preference
        if return_metrics:
            return chat_response
        else:
            return response

    def chat_stream(
        self, message: str, user_id: Optional[str] = None, metadata: Optional[Dict] = None
    ) -> Iterator[str]:
        """
        Chat with user using streaming response (real-time)

        This method streams the response as it's generated, providing a better UX
        for longer responses (like ChatGPT's typing effect).

        Args:
            message: User's message
            user_id: User ID (optional)
            metadata: Additional information

        Yields:
            Response text chunks as they arrive from the LLM

        Example:
            >>> agent = MemAgent()
            >>> agent.set_user("alice")
            >>> for chunk in agent.chat_stream("Python nedir?"):
            ...     print(chunk, end='', flush=True)
            Python bir programlama dilidir...
        """
        # Start timing
        start_time = time.time()

        # Determine user
        if user_id:
            self.set_user(user_id)
        elif not self.current_user:
            yield "Error: User ID not specified."
            return

        user_id = self.current_user

        # Initialize tracking variables
        kb_results_count = 0
        used_kb = False
        used_memory = False

        # Security check (v1.1.0+) - opt-in
        if self.enable_security and self.security_detector and self.security_sanitizer:
            risk_level = self.security_detector.get_risk_level(message)
            is_suspicious, patterns = self.security_detector.detect(message)

            if risk_level in ["high", "critical"]:
                self.logger.warning(f"🚨 Blocked {risk_level} risk input from {user_id}")
                yield (
                    "⚠️ Your message was blocked due to security concerns. "
                    "Please rephrase your request."
                )
                return

            # Sanitize input
            message = self.security_sanitizer.sanitize(message, aggressive=(risk_level == "medium"))

        # Check tool commands first
        tool_result = self.tool_executor.execute_user_command(message, user_id)
        if tool_result:
            yield tool_result
            return

        # Knowledge base search (if using SQL)
        kb_context = ""
        if ADVANCED_AVAILABLE and isinstance(self.memory, SQLMemoryManager):
            use_kb = True
            kb_limit = 5

            if hasattr(self, "config") and self.config:
                use_kb = self.config.get("response.use_knowledge_base", True)
                kb_limit = self.config.get("knowledge_base.search_limit", 5)

            if use_kb:
                try:
                    kb_results = self.memory.search_knowledge(query=message, limit=kb_limit)

                    if kb_results:
                        kb_results_count = len(kb_results)
                        used_kb = True
                        kb_context = "\n\n📚 RELEVANT KNOWLEDGE BASE:\n"
                        for i, result in enumerate(kb_results, 1):
                            kb_context += (
                                f"{i}. Q: {result['question']}\n   A: {result['answer']}\n"
                            )
                        kb_context += (
                            "\n⚠️ USE THIS INFORMATION TO ANSWER! Be brief but accurate.\n"
                        )
                except Exception as e:
                    self.logger.error(f"Knowledge base search error: {e}")

        # Rebuild system prompt to include any newly registered tools (v2.1.1+)
        if self.enable_tools and self.tool_registry:
            self._build_dynamic_system_prompt()

        # Get conversation history
        messages = []
        if self.current_system_prompt:
            messages.append({"role": "system", "content": self.current_system_prompt})

        # Add memory history
        try:
            if hasattr(self.memory, "get_recent_conversations"):
                recent_limit = (
                    self.config.get("response.recent_conversations_limit", 5)
                    if hasattr(self, "config") and self.config
                    else 5
                )
                recent_convs = self.memory.get_recent_conversations(user_id, recent_limit)

                if recent_convs:
                    used_memory = True

                # Add conversations in chronological order
                for conv in recent_convs:
                    messages.append({"role": "user", "content": conv.get("user_message", "")})
                    messages.append({"role": "assistant", "content": conv.get("bot_response", "")})
        except Exception as e:
            self.logger.error(f"Memory history loading error: {e}")

        # Add current message WITH knowledge base context (if available)
        final_message = message
        if kb_context:
            final_message = f"{kb_context}\n\nUser Question: {message}"

        messages.append({"role": "user", "content": final_message})

        # Get streaming response from LLM
        temperature = (
            self.config.get("llm.temperature", 0.2)
            if hasattr(self, "config") and self.config
            else 0.2
        )
        max_tokens = (
            self.config.get("llm.max_tokens", 2000)
            if hasattr(self, "config") and self.config
            else 2000
        )

        # Collect full response for saving
        full_response = ""

        try:
            # Stream chunks from LLM
            for chunk in self.llm.chat_stream(
                messages=messages, temperature=temperature, max_tokens=max_tokens
            ):
                full_response += chunk
                yield chunk

        except Exception as e:
            error_msg = f"Streaming error: {str(e)}"
            self.logger.error(error_msg)
            yield f"\n\n⚠️ {error_msg}"
            return

        # Calculate latency
        latency = (time.time() - start_time) * 1000

        # Determine response source
        response_source = "model"
        if used_memory and used_kb:
            response_source = "hybrid"
        elif used_kb:
            response_source = "knowledge_base"

        # Calculate confidence
        confidence = calculate_confidence(
            kb_results_count=kb_results_count,
            temperature=temperature,
            used_memory=used_memory,
            response_length=len(full_response),
        )

        # Build enriched metadata
        enriched_metadata = {}
        if metadata:
            enriched_metadata.update(metadata)
        enriched_metadata.update(
            {
                "confidence": round(confidence, 3),
                "source": response_source,
                "latency_ms": round(latency, 1),
                "kb_results_count": kb_results_count,
                "used_memory": used_memory,
                "used_kb": used_kb,
                "response_length": len(full_response),
                "model": self.model,
                "temperature": temperature,
                "streaming": True,
            }
        )

        # Save interaction
        try:
            if hasattr(self.memory, "add_interaction"):
                self.memory.add_interaction(
                    user_id=user_id,
                    user_message=message,
                    bot_response=full_response,
                    metadata=enriched_metadata,
                )

                # Extract and save user info to profile
                self._update_user_profile(user_id, message, full_response)

                # Update graph memory (v2.3.0)
                self._update_graph_memory(message, full_response)

                # Update summary (JSON mode)
                if not self.use_sql and hasattr(self.memory, "conversations"):
                    self._update_conversation_summary(user_id)
                    if user_id in self.memory.user_profiles:
                        self.memory.save_memory(user_id)
        except Exception as e:
            self.logger.error(f"Interaction saving error: {e}")

        # Track metrics if enabled
        if self.track_metrics:
            chat_response = ChatResponse(
                text=full_response,
                confidence=confidence,
                source=response_source,
                latency=latency,
                timestamp=datetime.now(),
                kb_results_count=kb_results_count,
                metadata={
                    "model": self.model,
                    "temperature": temperature,
                    "used_memory": used_memory,
                    "used_kb": used_kb,
                    "user_id": user_id,
                    "streaming": True,
                },
            )
            self.metrics_analyzer.add_metric(chat_response)

    def _update_user_profile(self, user_id: str, message: str, response: str):
        """Extract user info from conversation and update profile"""
        msg_lower = message.lower()

        # Extract information
        extracted = {}

        # Extract name
        if (
            "my name is" in msg_lower
            or "i am" in msg_lower
            or "i'm" in msg_lower
            or "adım" in msg_lower
            or "ismim" in msg_lower
        ):
            for phrase in ["my name is ", "i am ", "i'm ", "adım ", "ismim ", "benim adım "]:
                if phrase in msg_lower:
                    name_part = message[msg_lower.index(phrase) + len(phrase) :].strip()
                    name = name_part.split()[0] if name_part else None
                    if name and len(name) > 1:
                        extracted["name"] = name.strip(".,!?")
                        break

        # Extract favorite food
        if (
            "favorite food" in msg_lower
            or "favourite food" in msg_lower
            or "sevdiğim yemek" in msg_lower
            or "en sevdiğim" in msg_lower
        ):
            if "is" in msg_lower or ":" in msg_lower:
                food = (
                    msg_lower.split("is")[-1].strip()
                    if "is" in msg_lower
                    else msg_lower.split(":")[-1].strip()
                )
                food = food.strip(".,!?")
                if food and len(food) < 50:
                    extracted["favorite_food"] = food

        # Extract location
        if (
            "i live in" in msg_lower
            or "i'm from" in msg_lower
            or "yaşıyorum" in msg_lower
            or "yaşadığım" in msg_lower
        ):
            for phrase in [
                "i live in ",
                "i'm from ",
                "from ",
                "yaşıyorum",
                "yaşadığım yer",
                "yaşadığım şehir",
            ]:
                if phrase in msg_lower:
                    loc = message[msg_lower.index(phrase) + len(phrase) :].strip()
                    location = loc.split()[0] if loc else None
                    if location and len(location) > 2:
                        extracted["location"] = location.strip(".,!?")
                        break

        # Save updates
        if extracted:
            try:
                # SQL memory - store in preferences JSON
                if hasattr(self.memory, "update_user_profile"):
                    # Get current profile
                    profile = self.memory.get_user_profile(user_id) or {}

                    # Update name directly if extracted
                    updates = {}
                    if "name" in extracted:
                        updates["name"] = extracted.pop("name")

                    # Store other info in preferences
                    if extracted:
                        current_prefs = profile.get("preferences")
                        if current_prefs:
                            try:
                                prefs = (
                                    json.loads(current_prefs)
                                    if isinstance(current_prefs, str)
                                    else current_prefs
                                )
                            except Exception:
                                prefs = {}
                        else:
                            prefs = {}

                        prefs.update(extracted)
                        updates["preferences"] = json.dumps(prefs)

                    if updates:
                        self.memory.update_user_profile(user_id, updates)
                        self.logger.debug(f"Profile updated for {user_id}: {extracted}")

                # JSON memory - direct update
                elif hasattr(self.memory, "update_profile"):
                    # Load memory if not already loaded
                    if user_id not in self.memory.user_profiles:
                        self.memory.load_memory(user_id)

                    # For JSON memory, merge into preferences
                    current_profile = self.memory.user_profiles.get(user_id, {})
                    current_prefs = current_profile.get("preferences", {})

                    # Handle case where preferences might be a JSON string
                    if isinstance(current_prefs, str):
                        try:
                            current_prefs = json.loads(current_prefs)
                        except Exception:
                            current_prefs = {}

                    # Update preferences
                    if extracted:
                        current_prefs.update(extracted)
                        self.memory.user_profiles[user_id]["preferences"] = current_prefs

                    # Update name if extracted
                    if "name" in extracted:
                        self.memory.user_profiles[user_id]["name"] = extracted["name"]

                    # Auto-generate summary from conversation history
                    self._update_conversation_summary(user_id)

                    # Save to disk
                    self.memory.save_memory(user_id)
                    self.logger.debug(f"Profile updated for {user_id}: {extracted}")
            except Exception as e:
                self.logger.error(f"Error updating profile: {e}")

    def _update_graph_memory(self, message: str, response: str) -> None:
        """Extract triplets from conversation and update graph memory"""
        if not self.graph_extractor or not self.graph_store:
            return

        try:
            # Combine message and response for context
            text = f"User: {message}\nAssistant: {response}"

            # Extract triplets
            triplets = self.graph_extractor.extract(text)

            if triplets:
                self.logger.info(f"🕸️ Found {len(triplets)} graph triplets to save")
                for source, relation, target in triplets:
                    self.graph_store.add_triplet(source, relation, target)

                # Save graph to disk
                self.graph_store.save()
        except Exception as e:
            self.logger.error(f"Graph memory update error: {e}")

    def clear_graph_memory(self, user_id: str):
        """Clear knowledge graph memory for user"""
        if self.graph_store:
            self.graph_store.clear()
            self.logger.info(f"Graph memory cleared for {user_id}")
            return True
        return False

    def _update_conversation_summary(self, user_id: str) -> None:
        """
        Auto-generate conversation summary for user profile

        Args:
            user_id: User ID
        """
        try:
            if not hasattr(self.memory, "conversations"):
                return

            # Ensure memory is loaded
            if user_id not in self.memory.conversations:
                self.memory.load_memory(user_id)

            conversations = self.memory.conversations.get(user_id, [])
            if not conversations:
                return

            # Get recent conversations for summary
            recent_convs = conversations[-10:]  # Last 10 conversations

            # Extract topics/interests
            all_messages = " ".join([c.get("user_message", "") for c in recent_convs])
            topics = self._extract_topics(all_messages)

            # Calculate engagement stats
            total_interactions = len(conversations)
            avg_response_length = (
                sum(len(c.get("bot_response", "")) for c in recent_convs) / len(recent_convs)
                if recent_convs
                else 0
            )

            # Build summary
            summary = {
                "total_interactions": total_interactions,
                "topics_of_interest": topics[:5] if topics else [],  # Top 5 topics
                "avg_response_length": round(avg_response_length, 0),
                "last_active": recent_convs[-1].get("timestamp") if recent_convs else None,
                "engagement_level": (
                    "high"
                    if total_interactions > 20
                    else ("medium" if total_interactions > 5 else "low")
                ),
            }

            # Update profile summary (JSON mode)
            if user_id in self.memory.user_profiles:
                self.memory.user_profiles[user_id]["summary"] = summary

        except Exception as e:
            self.logger.debug(f"Summary generation skipped: {e}")

    def _extract_topics(self, text: str) -> List[str]:
        """
        Extract key topics/interests from conversation text

        Args:
            text: Combined conversation text

        Returns:
            List of extracted topics
        """
        # Simple keyword extraction (can be enhanced with NLP)
        keywords_map = {
            "python": "Python Programming",
            "javascript": "JavaScript",
            "coding": "Programming",
            "weather": "Weather",
            "food": "Food & Dining",
            "music": "Music",
            "sport": "Sports",
            "travel": "Travel",
            "work": "Work",
            "help": "Support",
            "problem": "Problem Solving",
            "question": "Questions",
            "chat": "Chatting",
        }

        text_lower = text.lower()
        found_topics = []

        for keyword, topic in keywords_map.items():
            if keyword in text_lower:
                found_topics.append(topic)

        # Remove duplicates while preserving order
        seen = set()
        unique_topics = []
        for topic in found_topics:
            if topic not in seen:
                seen.add(topic)
                unique_topics.append(topic)

        return unique_topics

    def get_user_profile(self, user_id: Optional[str] = None) -> Dict:
        """
        Get user's profile info

        Args:
            user_id: User ID (uses current_user if not specified)

        Returns:
            User profile dictionary with all info (name, favorite_food, location, etc.)
        """
        uid = user_id or self.current_user
        if not uid:
            return {}

        try:
            # Check if SQL or JSON memory - SQL has SQLMemoryManager type
            if ADVANCED_AVAILABLE and isinstance(self.memory, SQLMemoryManager):
                # SQL memory - merge preferences into main dict
                profile = self.memory.get_user_profile(uid)
                if not profile:
                    return {}

                # Parse preferences JSON if exists
                result = {
                    "user_id": profile.get("user_id"),
                    "name": profile.get("name"),
                    "first_seen": profile.get("first_seen"),
                    "last_interaction": profile.get("last_interaction"),
                }

                # Merge preferences
                prefs_str = profile.get("preferences")
                if prefs_str:
                    try:
                        prefs = json.loads(prefs_str) if isinstance(prefs_str, str) else prefs_str
                        result.update(prefs)  # Add favorite_food, location, etc.
                    except Exception:
                        pass

                return result
            else:
                # JSON memory - reload from disk to get latest data
                memory_data = self.memory.load_memory(uid)
                profile = memory_data.get(
                    "profile", {}
                ).copy()  # Make a copy to avoid modifying cached data

                # Parse preferences if it's a JSON string
                if isinstance(profile.get("preferences"), str):
                    try:
                        profile["preferences"] = json.loads(profile["preferences"])
                    except Exception:
                        profile["preferences"] = {}

                # Return profile as-is (summary should already be there if it was generated)
                # Only regenerate if truly missing
                summary_value = profile.get("summary")
                summary_is_empty = not summary_value or (
                    isinstance(summary_value, dict) and len(summary_value) == 0
                )

                if summary_is_empty:
                    # Try to regenerate summary if missing (for old users)
                    # Ensure conversations are loaded
                    if uid not in self.memory.conversations:
                        self.memory.load_memory(uid)

                    if uid in self.memory.conversations and len(self.memory.conversations[uid]) > 0:
                        self._update_conversation_summary(uid)
                        # Save the updated summary
                        if uid in self.memory.user_profiles:
                            self.memory.save_memory(uid)
                        # Reload to get updated summary
                        memory_data = self.memory.load_memory(uid)
                        profile = memory_data.get("profile", {}).copy()
                        # Parse preferences again after reload
                        if isinstance(profile.get("preferences"), str):
                            try:
                                profile["preferences"] = json.loads(profile["preferences"])
                            except Exception:
                                profile["preferences"] = {}

                return profile
        except Exception as e:
            self.logger.error(f"Error getting user profile: {e}")
            return {}

    def add_knowledge(
        self,
        category: str,
        question: str,
        answer: str,
        keywords: Optional[List[str]] = None,
        priority: int = 0,
    ) -> int:
        """Add new record to knowledge base"""
        if not ADVANCED_AVAILABLE or not isinstance(self.memory, SQLMemoryManager):
            return 0

        try:
            kb_id = self.memory.add_knowledge(category, question, answer, keywords, priority)
            self.logger.info(f"New knowledge added: {category} - {kb_id}")
            return kb_id
        except Exception as e:
            self.logger.error(f"Knowledge adding error: {e}")
            return 0

    def get_statistics(self) -> Dict[str, Any]:
        """Returns general statistics"""
        try:
            if hasattr(self.memory, "get_statistics"):
                return self.memory.get_statistics()
            else:
                # Simple statistics for JSON memory
                return {"total_users": 0, "total_interactions": 0, "memory_backend": "JSON"}
        except Exception as e:
            self.logger.error(f"Statistics retrieval error: {e}")
            return {}

    def search_history(self, keyword: str, user_id: Optional[str] = None) -> List[Dict]:
        """Search in user history"""
        uid = user_id or self.current_user
        if not uid:
            return []

        try:
            if hasattr(self.memory, "search_conversations"):
                return self.memory.search_conversations(uid, keyword)
            else:
                return []
        except Exception as e:
            self.logger.error(f"History search error: {e}")
            return []

    def show_user_info(self, user_id: Optional[str] = None) -> str:
        """Shows user information"""
        uid = user_id or self.current_user
        if not uid:
            return "User ID not specified."

        try:
            if hasattr(self.memory, "get_user_profile"):
                profile = self.memory.get_user_profile(uid)
                if profile:
                    name = profile.get("name", "Unknown")
                    first_seen = profile.get("first_seen", "Unknown")
                    return f"User: {uid}\nName: {name}\nFirst conversation: {first_seen}"
                else:
                    return f"User {uid} not found."
            else:
                return "This feature is not available."
        except Exception as e:
            return f"Error: {str(e)}"

    def export_memory(self, user_id: Optional[str] = None, format: str = "json") -> str:
        """Export user data"""
        uid = user_id or self.current_user
        if not uid:
            return "User ID not specified."

        try:
            if hasattr(self.memory, "get_recent_conversations") and hasattr(
                self.memory, "get_user_profile"
            ):
                conversations = self.memory.get_recent_conversations(uid, 1000)
                profile = self.memory.get_user_profile(uid)

                if format == "json":
                    export_data = {
                        "user_id": uid,
                        "export_date": datetime.now().isoformat(),
                        "profile": profile,
                        "conversations": conversations,
                    }
                    return json.dumps(export_data, ensure_ascii=False, indent=2)
                elif format == "txt":
                    result = f"{uid} user conversation history\n"
                    result += f"Export date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    result += "=" * 60 + "\n\n"

                    for i, conv in enumerate(conversations, 1):
                        result += f"Conversation {i}:\n"
                        result += f"Date: {conv.get('timestamp', 'Unknown')}\n"
                        result += f"User: {conv.get('user_message', '')}\n"
                        result += f"Bot: {conv.get('bot_response', '')}\n"
                        result += "-" * 40 + "\n"

                    return result
                else:
                    return "Unsupported format. Use json or txt."
            else:
                return "This feature is not available."
        except Exception as e:
            return f"Export error: {str(e)}"

    def clear_user_data(self, user_id: Optional[str] = None, confirm: bool = False) -> str:
        """Delete user data"""
        uid = user_id or self.current_user
        if not uid:
            return "User ID not specified."

        if not confirm:
            return "Use confirm=True parameter to delete data."

        try:
            if hasattr(self.memory, "clear_memory"):
                self.memory.clear_memory(uid)
                return f"All data for user {uid} has been deleted."
            else:
                return "This feature is not available."
        except Exception as e:
            return f"Deletion error: {str(e)}"

    def list_available_tools(self) -> str:
        """List available tools"""
        if ADVANCED_AVAILABLE:
            return self.tool_executor.memory_tools.list_available_tools()
        else:
            return "Tool system not available."

    # === METRICS & ANALYTICS METHODS (v1.3.1+) ===

    def get_response_metrics(self, last_n: Optional[int] = None) -> Dict[str, Any]:
        """
        Get response quality metrics summary

        Args:
            last_n: Analyze only last N responses (None = all)

        Returns:
            Metrics summary dictionary

        Example:
            >>> agent.get_response_metrics(last_n=10)
            {
                'total_responses': 10,
                'avg_latency_ms': 245.3,
                'avg_confidence': 0.82,
                'kb_usage_rate': 0.6,
                'source_distribution': {'knowledge_base': 6, 'model': 4},
                'fast_response_rate': 0.9
            }
        """
        return self.metrics_analyzer.get_summary(last_n)

    def get_latest_response_metric(self) -> Optional[ChatResponse]:
        """
        Get the most recent response metric

        Returns:
            Latest ChatResponse object or None if no metrics
        """
        if not self.metrics_analyzer.metrics_history:
            return None
        return self.metrics_analyzer.metrics_history[-1]

    def get_average_confidence(self, last_n: Optional[int] = None) -> float:
        """
        Get average confidence score

        Args:
            last_n: Analyze only last N responses (None = all)

        Returns:
            Average confidence (0.0-1.0)
        """
        return self.metrics_analyzer.get_average_confidence(last_n)

    def get_kb_usage_rate(self, last_n: Optional[int] = None) -> float:
        """
        Get knowledge base usage rate

        Args:
            last_n: Analyze only last N responses (None = all)

        Returns:
            KB usage rate (0.0-1.0)
        """
        return self.metrics_analyzer.get_kb_usage_rate(last_n)

    def clear_metrics(self) -> None:
        """Clear all metrics history"""
        self.metrics_analyzer.clear_history()
        self.logger.info("Metrics history cleared")

    def export_metrics(self, format: str = "json") -> str:
        """
        Export metrics data

        Args:
            format: Export format ('json' or 'summary')

        Returns:
            Formatted metrics data
        """
        summary = self.get_response_metrics()

        if format == "json":
            return json.dumps(summary, ensure_ascii=False, indent=2)
        elif format == "summary":
            lines = [
                "📊 RESPONSE METRICS SUMMARY",
                "=" * 60,
                f"Total Responses:      {summary['total_responses']}",
                f"Avg Latency:          {summary['avg_latency_ms']:.1f} ms",
                f"Avg Confidence:       {summary['avg_confidence']:.2%}",
                f"KB Usage Rate:        {summary['kb_usage_rate']:.2%}",
                f"Fast Response Rate:   {summary['fast_response_rate']:.2%}",
                "",
                "Source Distribution:",
            ]
            for source, count in summary["source_distribution"].items():
                lines.append(f"  - {source:20s}: {count}")

            lines.extend(["", "Quality Distribution:"])
            for quality, count in summary.get("quality_distribution", {}).items():
                lines.append(f"  - {quality:20s}: {count}")

            return "\n".join(lines)
        else:
            return "Unsupported format. Use 'json' or 'summary'."

    def close(self) -> None:
        """Clean up resources"""
        if hasattr(self.memory, "close"):
            self.memory.close()
        self.logger.info("MemAgent closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
