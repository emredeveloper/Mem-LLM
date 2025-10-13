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
from mem_agent import MemAgent

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

from typing import Optional, Dict, List, Any, Union
from datetime import datetime
import logging
import json
import os

# Core dependencies
from memory_manager import MemoryManager
from llm_client import OllamaClient

# Advanced features (optional)
try:
    from memory_db import SQLMemoryManager
    from prompt_templates import prompt_manager
    from knowledge_loader import KnowledgeLoader
    from config_manager import get_config
    from memory_tools import ToolExecutor, MemoryTools
    ADVANCED_AVAILABLE = True
except ImportError:
    ADVANCED_AVAILABLE = False
    print("⚠️  Advanced features not available (install additional packages)")


class MemAgent:
    """
    Powerful and unified Mem-Agent system

    Production-ready assistant that combines all features in one place.
    """

    def __init__(self,
                 model: str = "granite4:tiny-h",
                 config_file: Optional[str] = None,
                 use_sql: bool = True,
                 memory_dir: Optional[str] = None,
                 load_knowledge_base: bool = True,
                 ollama_url: str = "http://localhost:11434"):
        """
        Args:
            model: LLM model to use
            config_file: Configuration file (optional)
            use_sql: Use SQL database (True) or JSON (False)
            memory_dir: Memory directory
            load_knowledge_base: Automatically load knowledge base
            ollama_url: Ollama API URL
        """

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

        # Setup logging
        self._setup_logging()

        # Memory system selection
        if use_sql and ADVANCED_AVAILABLE:
            # SQL memory (advanced)
            db_path = memory_dir or self.config.get("memory.db_path", "memories.db") if self.config else "memories.db"
            self.memory = SQLMemoryManager(db_path)
            self.logger.info(f"SQL memory system active: {db_path}")
        else:
            # JSON memory (simple)
            json_dir = memory_dir or self.config.get("memory.json_dir", "memories") if self.config else "memories"
            self.memory = MemoryManager(json_dir)
            self.logger.info(f"JSON memory system active: {json_dir}")

        # LLM client
        self.llm = OllamaClient(model, ollama_url)
        self.logger.info(f"LLM client ready: {model}")

        # Advanced features (if available)
        if ADVANCED_AVAILABLE:
            self._setup_advanced_features(load_knowledge_base)
        else:
            print("⚠️  Load additional packages for advanced features")

        # Active user and system prompt
        self.current_user: Optional[str] = None
        self.current_system_prompt: Optional[str] = None

        # Tool system (always available)
        self.tool_executor = ToolExecutor(self.memory)

        self.logger.info("MemAgent successfully initialized")

    # === UNIFIED SYSTEM METHODS ===

    def _setup_logging(self) -> None:
        """Setup logging system"""
        log_config = {}
        if ADVANCED_AVAILABLE and hasattr(self, 'config') and self.config:
            log_config = self.config.get("logging", {})

        if log_config.get("enabled", True):
            logging.basicConfig(
                level=getattr(logging, log_config.get("level", "INFO")),
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_config.get("file", "mem_agent.log")),
                    logging.StreamHandler()
                ]
            )

        self.logger = logging.getLogger("MemAgent")

    def _setup_advanced_features(self, load_knowledge_base: bool) -> None:
        """Setup advanced features"""
        # Load knowledge base (according to usage mode)
        if load_knowledge_base:
            kb_loader = KnowledgeLoader(self.memory)

            # Get KB settings from config
            if hasattr(self, 'config') and self.config:
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
                    elif default_kb == "tech_support":
                        count = kb_loader.load_default_tech_support_kb()
                        self.logger.info(f"Technical support knowledge base loaded: {count} records")
                    elif default_kb == "business_tech_support":
                        count = kb_loader.load_default_tech_support_kb()
                        self.logger.info(f"Corporate technical support knowledge base loaded: {count} records")
                    elif default_kb == "personal_learning":
                        # Simple KB for personal learning
                        count = kb_loader.load_default_ecommerce_kb()  # Temporarily use the same KB
                        self.logger.info(f"Personal learning knowledge base loaded: {count} records")
                except Exception as e:
                    self.logger.error(f"Knowledge base loading error: {e}")

        # Load system prompt (according to usage mode)
        if hasattr(self, 'config') and self.config:
            prompt_config = self.config.get("prompt", {})

            # Select default template according to usage mode
            if self.usage_mode == "business":
                default_template = "business_customer_service"
            else:  # personal
                default_template = "personal_assistant"

            template_name = prompt_config.get("template", default_template)
            variables = prompt_config.get("variables", {})

            # Additional variables for business mode
            if self.usage_mode == "business":
                business_config = self.config.get("business", {})
                variables.update({
                    "company_name": business_config.get("company_name", "Our Company"),
                    "founded_year": business_config.get("founded_year", "2010"),
                    "employee_count": business_config.get("employee_count", "100+"),
                    "industry": business_config.get("industry", "Teknoloji")
                })
            else:  # personal
                personal_config = self.config.get("personal", {})
                variables.update({
                    "user_name": personal_config.get("user_name", "User"),
                    "timezone": personal_config.get("timezone", "Europe/London")
                })

            try:
                variables['current_date'] = datetime.now().strftime("%Y-%m-%d")
                self.current_system_prompt = prompt_manager.render_prompt(template_name, **variables)
                self.logger.info(f"Prompt template loaded: {template_name} (Mode: {self.usage_mode})")
            except Exception as e:
                self.logger.error(f"Prompt template loading error: {e}")
                self.current_system_prompt = f"You are a helpful assistant in {self.usage_mode} mode."

    def check_setup(self) -> Dict[str, Any]:
        """Check system setup"""
        ollama_running = self.llm.check_connection()
        models = self.llm.list_models()
        model_exists = self.llm.model in models

        # Memory statistics
        try:
            if hasattr(self.memory, 'get_statistics'):
                stats = self.memory.get_statistics()
            else:
                # Simple statistics for JSON memory
                stats = {
                    "total_users": 0,
                    "total_interactions": 0,
                    "knowledge_base_entries": 0
                }
        except Exception:
            stats = {
                "total_users": 0,
                "total_interactions": 0,
                "knowledge_base_entries": 0
            }

        return {
            "ollama_running": ollama_running,
            "available_models": models,
            "target_model": self.llm.model,
            "model_ready": model_exists,
            "memory_backend": "SQL" if ADVANCED_AVAILABLE and isinstance(self.memory, SQLMemoryManager) else "JSON",
            "total_users": stats.get('total_users', 0),
            "total_interactions": stats.get('total_interactions', 0),
            "kb_entries": stats.get('knowledge_base_entries', 0),
            "status": "ready" if (ollama_running and model_exists) else "not_ready"
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
            if hasattr(self.memory, 'update_user_profile'):
                self.memory.update_user_profile(user_id, {"name": name})

        self.logger.debug(f"Active user set: {user_id}")

    def chat(self, message: str, user_id: Optional[str] = None,
             metadata: Optional[Dict] = None) -> str:
        """
        Chat with user

        Args:
            message: User's message
            user_id: User ID (optional)
            metadata: Additional information

        Returns:
            Bot's response
        """
        # Determine user
        if user_id:
            self.set_user(user_id)
        elif not self.current_user:
            return "Error: User ID not specified."

        user_id = self.current_user

        # Check tool commands first
        tool_result = self.tool_executor.execute_user_command(message, user_id)
        if tool_result:
            return tool_result

        # Knowledge base search (if using SQL)
        kb_context = ""
        if ADVANCED_AVAILABLE and isinstance(self.memory, SQLMemoryManager) and hasattr(self, 'config') and self.config:
            if self.config.get("response.use_knowledge_base", True):
                try:
                    kb_results = self.memory.search_knowledge(
                        query=message,
                        limit=self.config.get("knowledge_base.search_limit", 5)
                    )

                    if kb_results:
                        kb_context = "\n\nRelevant Information:\n"
                        for i, result in enumerate(kb_results, 1):
                            kb_context += f"{i}. S: {result['question']}\n   C: {result['answer']}\n"
                except Exception as e:
                    self.logger.error(f"Knowledge base search error: {e}")

        # Get conversation history
        messages = []
        if self.current_system_prompt:
            messages.append({"role": "system", "content": self.current_system_prompt})

        # Add memory history
        try:
            if hasattr(self.memory, 'get_recent_conversations'):
                recent_limit = self.config.get("response.recent_conversations_limit", 5) if hasattr(self, 'config') and self.config else 5
                recent_convs = self.memory.get_recent_conversations(user_id, recent_limit)

                for conv in reversed(recent_convs):
                    messages.append({"role": "user", "content": conv.get('user_message', '')})
                    messages.append({"role": "assistant", "content": conv.get('bot_response', '')})
        except Exception as e:
            self.logger.error(f"Memory history loading error: {e}")

        # Add knowledge base context
        if kb_context:
            messages.append({
                "role": "system",
                "content": f"You can use this information when answering the user's question:{kb_context}"
            })

        # Add current message
        messages.append({"role": "user", "content": message})

        # Get response from LLM
        try:
            response = self.llm.chat(
                messages=messages,
                temperature=self.config.get("llm.temperature", 0.7) if hasattr(self, 'config') and self.config else 0.7,
                max_tokens=self.config.get("llm.max_tokens", 500) if hasattr(self, 'config') and self.config else 500
            )
        except Exception as e:
            self.logger.error(f"LLM response error: {e}")
            response = "Sorry, I cannot respond right now. Please try again later."

        # Save interaction
        try:
            if hasattr(self.memory, 'add_interaction'):
                self.memory.add_interaction(
                    user_id=user_id,
                    user_message=message,
                    bot_response=response,
                    metadata=metadata
                )
        except Exception as e:
            self.logger.error(f"Interaction saving error: {e}")

        return response

    def add_knowledge(self, category: str, question: str, answer: str,
                     keywords: Optional[List[str]] = None, priority: int = 0) -> int:
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
            if hasattr(self.memory, 'get_statistics'):
                return self.memory.get_statistics()
            else:
                # Simple statistics for JSON memory
                return {
                    "total_users": 0,
                    "total_interactions": 0,
                    "memory_backend": "JSON"
                }
        except Exception as e:
            self.logger.error(f"Statistics retrieval error: {e}")
            return {}

    def search_history(self, keyword: str, user_id: Optional[str] = None) -> List[Dict]:
        """Search in user history"""
        uid = user_id or self.current_user
        if not uid:
            return []

        try:
            if hasattr(self.memory, 'search_conversations'):
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
            if hasattr(self.memory, 'get_user_profile'):
                profile = self.memory.get_user_profile(uid)
                if profile:
                    return f"User: {uid}\nName: {profile.get('name', 'Unknown')}\nFirst conversation: {profile.get('first_seen', 'Unknown')}"
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
            if hasattr(self.memory, 'get_recent_conversations') and hasattr(self.memory, 'get_user_profile'):
                conversations = self.memory.get_recent_conversations(uid, 1000)
                profile = self.memory.get_user_profile(uid)

                if format == "json":
                    export_data = {
                        "user_id": uid,
                        "export_date": datetime.now().isoformat(),
                        "profile": profile,
                        "conversations": conversations
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
            if hasattr(self.memory, 'clear_memory'):
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

    def close(self) -> None:
        """Clean up resources"""
        if hasattr(self.memory, 'close'):
            self.memory.close()
        self.logger.info("MemAgent closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

