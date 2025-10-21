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

from typing import Optional, Dict, List, Any, Union
from datetime import datetime
import logging
import json
import os

# Core dependencies
from .memory_manager import MemoryManager
from .llm_client import OllamaClient

# Advanced features (optional)
try:
    from .memory_db import SQLMemoryManager
    from .knowledge_loader import KnowledgeLoader
    from .config_manager import get_config
    from .memory_tools import ToolExecutor, MemoryTools
    from .dynamic_prompt import dynamic_prompt_builder
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
                 db_path: Optional[str] = None,
                 load_knowledge_base: bool = True,
                 ollama_url: str = "http://localhost:11434",
                 check_connection: bool = False,
                 enable_security: bool = False):
        """
        Args:
            model: LLM model to use
            config_file: Configuration file (optional)
            use_sql: Use SQL database (True) or JSON (False)
            memory_dir: Memory directory (for JSON mode or if db_path not specified)
            db_path: SQLite database path (for SQL mode, e.g., ":memory:" or "path/to/db.db")
            load_knowledge_base: Automatically load knowledge base
            ollama_url: Ollama API URL
            check_connection: Verify Ollama connection on startup (default: False)
            enable_security: Enable prompt injection protection (v1.1.0+, default: False for backward compatibility)
        """
        
        # Setup logging first
        self._setup_logging()
        
        # Security features (v1.1.0+)
        self.enable_security = enable_security
        self.security_detector = None
        self.security_sanitizer = None
        
        if enable_security:
            try:
                from .prompt_security import PromptInjectionDetector, InputSanitizer
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
        self.has_tools: bool = False  # Track tools status

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
            
            # Ensure memories directory exists (skip for :memory:)
            import os
            if final_db_path != ":memory:":
                db_dir = os.path.dirname(final_db_path)
                if db_dir and not os.path.exists(db_dir):
                    os.makedirs(db_dir, exist_ok=True)
            
            self.memory = SQLMemoryManager(final_db_path)
            self.logger.info(f"SQL memory system active: {final_db_path}")
        else:
            # JSON memory (simple)
            json_dir = memory_dir or self.config.get("memory.json_dir", "memories") if self.config else "memories"
            self.memory = MemoryManager(json_dir)
            self.logger.info(f"JSON memory system active: {json_dir}")

        # Active user and system prompt
        self.current_user: Optional[str] = None
        self.current_system_prompt: Optional[str] = None

        # LLM client
        self.model = model  # Store model name
        self.use_sql = use_sql  # Store SQL usage flag
        self.llm = OllamaClient(model, ollama_url)
        
        # Optional connection check on startup
        if check_connection:
            self.logger.info("Checking Ollama connection...")
            if not self.llm.check_connection():
                error_msg = (
                    "❌ ERROR: Cannot connect to Ollama service!\n"
                    "   \n"
                    "   Solutions:\n"
                    "   1. Start Ollama: ollama serve\n"
                    "   2. Check if Ollama is running: http://localhost:11434\n"
                    "   3. Verify ollama_url parameter is correct\n"
                    "   \n"
                    "   To skip this check, use: MemAgent(check_connection=False)"
                )
                self.logger.error(error_msg)
                raise ConnectionError("Ollama service not available")
            
            # Check if model exists
            available_models = self.llm.list_models()
            if model not in available_models:
                error_msg = (
                    f"❌ ERROR: Model '{model}' not found!\n"
                    f"   \n"
                    f"   Solutions:\n"
                    f"   1. Download model: ollama pull {model}\n"
                    f"   2. Use an available model: {', '.join(available_models[:3])}\n"
                    f"   \n"
                    f"   Available models: {len(available_models)} found\n"
                    f"   To skip this check, use: MemAgent(check_connection=False)"
                )
                self.logger.error(error_msg)
                raise ValueError(f"Model '{model}' not available")
            
            self.logger.info(f"✅ Ollama connection verified, model '{model}' ready")
        
        self.logger.info(f"LLM client ready: {model}")

        # Initialize state variables FIRST
        self.current_user: Optional[str] = None
        self.current_system_prompt: Optional[str] = None

        # Advanced features (if available)
        if ADVANCED_AVAILABLE:
            self._setup_advanced_features(load_knowledge_base)
        else:
            print("⚠️  Load additional packages for advanced features")
            # Build basic prompt even without advanced features
            self._build_dynamic_system_prompt()

        # Tool system (always available)
        self.tool_executor = ToolExecutor(self.memory)

        self.logger.info("MemAgent successfully initialized")

    # === UNIFIED SYSTEM METHODS ===

    def _setup_logging(self) -> None:
        """Setup logging system"""
        log_config = {}
        if ADVANCED_AVAILABLE and hasattr(self, 'config') and self.config:
            log_config = self.config.get("logging", {})

        # Default to WARNING level to keep console clean (users can override in config)
        default_level = "WARNING"
        
        if log_config.get("enabled", True):
            # Only console logging (no file) - keep workspace clean
            logging.basicConfig(
                level=getattr(logging, log_config.get("level", default_level)),
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.StreamHandler()  # Console only
                ]
            )

        self.logger = logging.getLogger("MemAgent")
        
        # Set default level for mem_llm loggers
        logging.getLogger("mem_llm").setLevel(getattr(logging, log_config.get("level", default_level)))

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
                        self.has_knowledge_base = True  # KB loaded!
                    elif default_kb == "tech_support":
                        count = kb_loader.load_default_tech_support_kb()
                        self.logger.info(f"Technical support knowledge base loaded: {count} records")
                        self.has_knowledge_base = True  # KB loaded!
                    elif default_kb == "business_tech_support":
                        count = kb_loader.load_default_tech_support_kb()
                        self.logger.info(f"Corporate technical support knowledge base loaded: {count} records")
                        self.has_knowledge_base = True  # KB loaded!
                    elif default_kb == "personal_learning":
                        # Simple KB for personal learning
                        count = kb_loader.load_default_ecommerce_kb()  # Temporarily use the same KB
                        self.logger.info(f"Personal learning knowledge base loaded: {count} records")
                        self.has_knowledge_base = True  # KB loaded!
                except Exception as e:
                    self.logger.error(f"Knowledge base loading error: {e}")
                    self.has_knowledge_base = False

        # Build dynamic system prompt based on active features
        self._build_dynamic_system_prompt()

    def _build_dynamic_system_prompt(self) -> None:
        """Build dynamic system prompt based on active features"""
        if not ADVANCED_AVAILABLE:
            # Fallback simple prompt
            self.current_system_prompt = "You are a helpful AI assistant."
            return
        
        # Get config data
        business_config = None
        personal_config = None
        
        if hasattr(self, 'config') and self.config:
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
                has_tools=False,  # Not advertised yet
                is_multi_user=False,  # Always False for now, per-session state
                business_config=business_config,
                personal_config=personal_config,
                memory_type="sql" if self.use_sql else "json"
            )
            
            # Log feature summary
            feature_summary = dynamic_prompt_builder.get_feature_summary(
                has_knowledge_base=self.has_knowledge_base,
                has_tools=False,
                is_multi_user=False,
                memory_type="sql" if self.use_sql else "json"
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
        
        # Security check (v1.1.0+) - opt-in
        security_info = {}
        if self.enable_security and self.security_detector and self.security_sanitizer:
            # Detect injection attempts
            risk_level = self.security_detector.get_risk_level(message)
            is_suspicious, patterns = self.security_detector.detect(message)
            
            if risk_level in ["high", "critical"]:
                self.logger.warning(f"🚨 Blocked {risk_level} risk input from {user_id}: {len(patterns)} patterns detected")
                return f"⚠️ Your message was blocked due to security concerns. Please rephrase your request."
            
            if is_suspicious:
                self.logger.info(f"⚠️ Suspicious input from {user_id} (risk: {risk_level}): {len(patterns)} patterns")
            
            # Sanitize input
            original_message = message
            message = self.security_sanitizer.sanitize(message, aggressive=(risk_level == "medium"))
            
            if message != original_message:
                self.logger.debug(f"Input sanitized for {user_id}")
            
            security_info = {
                "risk_level": risk_level,
                "sanitized": message != original_message,
                "patterns_detected": len(patterns)
            }

        # Check tool commands first
        tool_result = self.tool_executor.execute_user_command(message, user_id)
        if tool_result:
            return tool_result

        # Knowledge base search (if using SQL)
        kb_context = ""
        if ADVANCED_AVAILABLE and isinstance(self.memory, SQLMemoryManager):
            # Check config only if it exists, otherwise always use KB
            use_kb = True
            kb_limit = 5
            
            if hasattr(self, 'config') and self.config:
                use_kb = self.config.get("response.use_knowledge_base", True)
                kb_limit = self.config.get("knowledge_base.search_limit", 5)
            
            if use_kb:
                try:
                    kb_results = self.memory.search_knowledge(query=message, limit=kb_limit)

                    if kb_results:
                        kb_context = "\n\n📚 RELEVANT KNOWLEDGE BASE:\n"
                        for i, result in enumerate(kb_results, 1):
                            kb_context += f"{i}. Q: {result['question']}\n   A: {result['answer']}\n"
                        kb_context += "\n⚠️ USE THIS INFORMATION TO ANSWER! Be brief but accurate.\n"
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

                # Add conversations in chronological order (oldest first)
                for conv in recent_convs:
                    messages.append({"role": "user", "content": conv.get('user_message', '')})
                    messages.append({"role": "assistant", "content": conv.get('bot_response', '')})
        except Exception as e:
            self.logger.error(f"Memory history loading error: {e}")

        # Add current message WITH knowledge base context (if available)
        final_message = message
        if kb_context:
            # Inject KB directly into user message for maximum visibility
            final_message = f"{kb_context}\n\nUser Question: {message}"
        
        messages.append({"role": "user", "content": final_message})

        # Get response from LLM
        try:
            response = self.llm.chat(
                messages=messages,
                temperature=self.config.get("llm.temperature", 0.2) if hasattr(self, 'config') and self.config else 0.2,  # Very focused
                max_tokens=self.config.get("llm.max_tokens", 2000) if hasattr(self, 'config') and self.config else 2000  # Enough tokens for thinking models
            )
            
            # Fallback: If response is empty (can happen with thinking models)
            if not response or response.strip() == "":
                self.logger.warning(f"Empty response from model {self.llm.model}, retrying with simpler prompt...")
                
                # Retry with just the current message, no history
                simple_messages = [
                    {"role": "system", "content": "You are a helpful assistant. Respond directly and concisely."},
                    {"role": "user", "content": message}
                ]
                response = self.llm.chat(simple_messages, temperature=0.7, max_tokens=2000)
                
                # If still empty, provide fallback
                if not response or response.strip() == "":
                    response = "I'm having trouble responding right now. Could you rephrase your question?"
                    self.logger.error(f"Model {self.llm.model} returned empty response even after retry")
                    
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
                
                # Extract and save user info to profile
                self._update_user_profile(user_id, message, response)
        except Exception as e:
            self.logger.error(f"Interaction saving error: {e}")

        return response
    
    def _update_user_profile(self, user_id: str, message: str, response: str):
        """Extract user info from conversation and update profile"""
        msg_lower = message.lower()
        
        # Extract information
        extracted = {}
        
        # Extract name
        if "my name is" in msg_lower or "i am" in msg_lower or "i'm" in msg_lower or "adım" in msg_lower or "ismim" in msg_lower:
            for phrase in ["my name is ", "i am ", "i'm ", "adım ", "ismim ", "benim adım "]:
                if phrase in msg_lower:
                    name_part = message[msg_lower.index(phrase) + len(phrase):].strip()
                    name = name_part.split()[0] if name_part else None
                    if name and len(name) > 1:
                        extracted['name'] = name.strip('.,!?')
                        break
        
        # Extract favorite food
        if "favorite food" in msg_lower or "favourite food" in msg_lower or "sevdiğim yemek" in msg_lower or "en sevdiğim" in msg_lower:
            if "is" in msg_lower or ":" in msg_lower:
                food = msg_lower.split("is")[-1].strip() if "is" in msg_lower else msg_lower.split(":")[-1].strip()
                food = food.strip('.,!?')
                if food and len(food) < 50:
                    extracted['favorite_food'] = food
        
        # Extract location
        if "i live in" in msg_lower or "i'm from" in msg_lower or "yaşıyorum" in msg_lower or "yaşadığım" in msg_lower:
            for phrase in ["i live in ", "i'm from ", "from ", "yaşıyorum", "yaşadığım yer", "yaşadığım şehir"]:
                if phrase in msg_lower:
                    loc = message[msg_lower.index(phrase) + len(phrase):].strip()
                    location = loc.split()[0] if loc else None
                    if location and len(location) > 2:
                        extracted['location'] = location.strip('.,!?')
                        break
        
        # Save updates
        if extracted:
            try:
                # SQL memory - store in preferences JSON
                if hasattr(self.memory, 'update_user_profile'):
                    # Get current profile
                    profile = self.memory.get_user_profile(user_id) or {}
                    
                    # Update name directly if extracted
                    updates = {}
                    if 'name' in extracted:
                        updates['name'] = extracted.pop('name')
                    
                    # Store other info in preferences
                    if extracted:
                        current_prefs = profile.get('preferences')
                        if current_prefs:
                            try:
                                prefs = json.loads(current_prefs) if isinstance(current_prefs, str) else current_prefs
                            except:
                                prefs = {}
                        else:
                            prefs = {}
                        
                        prefs.update(extracted)
                        updates['preferences'] = json.dumps(prefs)
                    
                    if updates:
                        self.memory.update_user_profile(user_id, updates)
                        self.logger.debug(f"Profile updated for {user_id}: {extracted}")
                
                # JSON memory - direct update
                elif hasattr(self.memory, 'update_profile'):
                    self.memory.update_profile(user_id, extracted)
                    self.logger.debug(f"Profile updated for {user_id}: {extracted}")
            except Exception as e:
                self.logger.error(f"Error updating profile: {e}")

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
            # Check if SQL or JSON memory
            if hasattr(self.memory, 'get_user_profile'):
                # SQL memory - merge preferences into main dict
                profile = self.memory.get_user_profile(uid)
                if not profile:
                    return {}
                
                # Parse preferences JSON if exists
                result = {
                    'user_id': profile.get('user_id'),
                    'name': profile.get('name'),
                    'first_seen': profile.get('first_seen'),
                    'last_interaction': profile.get('last_interaction'),
                }
                
                # Merge preferences
                prefs_str = profile.get('preferences')
                if prefs_str:
                    try:
                        prefs = json.loads(prefs_str) if isinstance(prefs_str, str) else prefs_str
                        result.update(prefs)  # Add favorite_food, location, etc.
                    except:
                        pass
                
                return result
            else:
                # JSON memory
                memory_data = self.memory.load_memory(uid)
                return memory_data.get('profile', {})
        except Exception as e:
            self.logger.error(f"Error getting user profile: {e}")
            return {}
    
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

