"""
Configuration Manager
Reads and manages configuration from YAML file
"""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class ConfigManager:
    """Manages configuration file"""

    def __init__(self, config_file: str = "config.yaml"):
        """
        Args:
            config_file: Configuration file path
        """
        self.config_file = Path(config_file)
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration file"""
        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f) or {}
        else:
            # Default configuration
            self.config = self._get_default_config()
            self.save_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Returns default configuration"""
        return {
            "llm": {
                "model": "rnj-1:latest",
                "base_url": "http://localhost:11434",
                "temperature": 0.7,
                "max_tokens": 500,
            },
            "memory": {
                "backend": "sql",
                "json_dir": "memories",
                "db_path": "memories/memories.db",
                "max_conversations_per_user": 1000,
                "auto_cleanup": True,
                "cleanup_after_days": 90,
            },
            "prompt": {
                "template": "customer_service",
                "variables": {"company_name": "Our Company", "tone": "friendly and professional"},
                "custom_prompt": None,
            },
            "knowledge_base": {
                "enabled": True,
                "auto_load": True,
                "default_kb": "ecommerce",
                "custom_kb_file": None,
                "search_limit": 5,
                "min_relevance_score": 0.3,
                "enable_vector_search": False,  # v1.3.2+ - Optional semantic search
                "embedding_model": "nomic-embed-text-v2-moe:latest",  # Sentence transformers model
            },
            "response": {
                "use_knowledge_base": True,
                "use_memory": True,
                "recent_conversations_limit": 5,
                "format": {"include_greeting": True, "include_follow_up": True, "max_length": 500},
            },
            "security": {
                "filter_sensitive_data": True,
                "sensitive_keywords": ["credit card", "password", "passcode", "CVV", "TR ID"],
                "rate_limit": {
                    "enabled": True,
                    "max_requests_per_minute": 60,
                    "max_requests_per_user_per_minute": 10,
                },
            },
            "logging": {
                "enabled": True,
                "level": "INFO",
                "file": "mem_agent.log",
                "max_size_mb": 10,
                "backup_count": 5,
                "log_user_messages": True,
                "log_bot_responses": True,
                "mask_sensitive": True,
            },
            "performance": {
                "enable_cache": True,
                "cache_ttl_seconds": 3600,
                "enable_parallel": False,
                "max_workers": 4,
            },
            "analytics": {
                "enabled": True,
                "track_response_time": True,
                "track_user_satisfaction": False,
                "track_conversation_length": True,
                "export_interval_hours": 24,
                "export_path": "analytics",
            },
        }

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value with dot notation

        Args:
            key_path: Key path (e.g: "llm.model")
            default: Value to return if not found

        Returns:
            Configuration value
        """
        keys = key_path.split(".")
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def set(self, key_path: str, value: Any) -> None:
        """
        Set configuration value with dot notation

        Args:
            key_path: Key path (e.g: "llm.model")
            value: Value to set
        """
        keys = key_path.split(".")
        config = self.config

        for key in keys[:-1]:
            if key not in config or not isinstance(config[key], dict):
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value

    def save_config(self) -> None:
        """Save configuration to file"""
        with open(self.config_file, "w", encoding="utf-8") as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    def reload(self) -> None:
        """Reload configuration"""
        self._load_config()

    def get_llm_config(self) -> Dict[str, Any]:
        """Returns LLM configuration"""
        return self.get("llm", {})

    def get_memory_config(self) -> Dict[str, Any]:
        """Returns memory configuration"""
        return self.get("memory", {})

    def get_prompt_config(self) -> Dict[str, Any]:
        """Returns prompt configuration"""
        return self.get("prompt", {})

    def get_kb_config(self) -> Dict[str, Any]:
        """Returns knowledge base configuration"""
        return self.get("knowledge_base", {})

    def is_kb_enabled(self) -> bool:
        """Is knowledge base enabled?"""
        return self.get("knowledge_base.enabled", True)

    def is_memory_enabled(self) -> bool:
        """Is memory enabled?"""
        return self.get("response.use_memory", True)

    def get_memory_backend(self) -> str:
        """Returns memory backend type (json or sql)"""
        return self.get("memory.backend", "sql")

    def get_db_path(self) -> str:
        """Returns database file path"""
        return self.get("memory.db_path", "memories.db")

    def get_json_dir(self) -> str:
        """Returns JSON memory directory"""
        return self.get("memory.json_dir", "memories")

    def __repr__(self) -> str:
        return f"ConfigManager(file='{self.config_file}')"


# Global instance
_config_manager: Optional[ConfigManager] = None


def get_config(config_file: str = "config.yaml") -> ConfigManager:
    """
    Returns global configuration manager

    Args:
        config_file: Configuration file

    Returns:
        ConfigManager instance
    """
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager(config_file)
    return _config_manager


def reload_config() -> None:
    """Reloads global configuration"""
    if _config_manager:
        _config_manager.reload()
