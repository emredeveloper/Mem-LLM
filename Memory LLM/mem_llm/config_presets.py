import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class ConfigPresets:
    """Manage configuration presets for MemAgent"""

    BUILTIN_PRESETS = {
        "chatbot": {
            "temperature": 0.7,
            "max_tokens": 500,
            "system_prompt": (
                "You are a helpful, friendly assistant. " "Provide clear and concise answers."
            ),
            "tools_enabled": True,
            "description": "General purpose conversational assistant",
        },
        "code_assistant": {
            "temperature": 0.2,
            "max_tokens": 2000,
            "system_prompt": (
                "You are an expert programmer. Provide code examples, "
                "explanations, and follow best practices. "
                "Always wrap code in markdown blocks."
            ),
            "tools_enabled": True,
            "description": "Specialized for coding tasks and debugging",
        },
        "creative_writer": {
            "temperature": 0.9,
            "max_tokens": 2000,
            "system_prompt": (
                "You are a creative writer. Write engaging, "
                "imaginative, and descriptive content."
            ),
            "tools_enabled": False,
            "description": "High creativity for stories and content generation",
        },
        "tutor": {
            "temperature": 0.5,
            "max_tokens": 1000,
            "system_prompt": (
                "You are a patient tutor. Explain concepts clearly with "
                "examples. Break down complex topics into simple steps."
            ),
            "tools_enabled": True,
            "description": "Educational assistant for learning new topics",
        },
        "analyst": {
            "temperature": 0.3,
            "max_tokens": 1500,
            "system_prompt": (
                "You are a data analyst. Provide insights, patterns, and "
                "objective analysis based on data. Be precise and factual."
            ),
            "tools_enabled": True,
            "description": "Data analysis and objective reporting",
        },
        "translator": {
            "temperature": 0.3,
            "max_tokens": 2000,
            "system_prompt": (
                "You are a professional translator. Translate the text "
                "accurately while preserving the original meaning, "
                "tone, and nuance."
            ),
            "tools_enabled": False,
            "description": "Accurate text translation",
        },
        "summarizer": {
            "temperature": 0.3,
            "max_tokens": 500,
            "system_prompt": (
                "You are a summarization expert. Create concise, accurate "
                "summaries that capture the main points of the content."
            ),
            "tools_enabled": False,
            "description": "Content summarization",
        },
        "researcher": {
            "temperature": 0.4,
            "max_tokens": 2000,
            "system_prompt": (
                "You are a research assistant. Provide well-researched, "
                "comprehensive information with citations where possible."
            ),
            "tools_enabled": True,
            "description": "Deep research and information gathering",
        },
    }

    def __init__(self, custom_presets_dir: Optional[str] = None):
        if custom_presets_dir:
            self.custom_dir = Path(custom_presets_dir)
        else:
            # Default to ~/.mem_llm/presets
            self.custom_dir = Path.home() / ".mem_llm" / "presets"

        self.custom_dir.mkdir(parents=True, exist_ok=True)

    def list_presets(self) -> List[str]:
        """List all available presets (built-in + custom)"""
        builtin = list(self.BUILTIN_PRESETS.keys())
        custom = self._list_custom_presets()
        return sorted(list(set(builtin + custom)))

    def get_preset(self, name: str) -> Dict[str, Any]:
        """Get preset configuration by name"""
        # Check built-in first
        if name in self.BUILTIN_PRESETS:
            return self.BUILTIN_PRESETS[name].copy()

        # Check custom
        custom_path_yaml = self.custom_dir / f"{name}.yaml"
        custom_path_json = self.custom_dir / f"{name}.json"

        if custom_path_yaml.exists():
            with open(custom_path_yaml, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)

        if custom_path_json.exists():
            with open(custom_path_json, "r", encoding="utf-8") as f:
                return json.load(f)

        raise ValueError(f"Preset '{name}' not found")

    def save_custom_preset(self, name: str, config: Dict[str, Any], format: str = "yaml"):
        """Save a custom preset"""
        if name in self.BUILTIN_PRESETS:
            raise ValueError(f"Cannot override built-in preset '{name}'")

        if format.lower() not in ["yaml", "json"]:
            raise ValueError("Format must be 'yaml' or 'json'")

        file_path = self.custom_dir / f"{name}.{format.lower()}"

        with open(file_path, "w", encoding="utf-8") as f:
            if format.lower() == "yaml":
                yaml.dump(config, f, default_flow_style=False)
            else:
                json.dump(config, f, indent=2)

    def delete_custom_preset(self, name: str):
        """Delete a custom preset"""
        if name in self.BUILTIN_PRESETS:
            raise ValueError(f"Cannot delete built-in preset '{name}'")

        yaml_path = self.custom_dir / f"{name}.yaml"
        json_path = self.custom_dir / f"{name}.json"

        deleted = False
        if yaml_path.exists():
            os.remove(yaml_path)
            deleted = True

        if json_path.exists():
            os.remove(json_path)
            deleted = True

        if not deleted:
            raise ValueError(f"Custom preset '{name}' not found")

    def _list_custom_presets(self) -> List[str]:
        """List custom presets found in the custom directory"""
        if not self.custom_dir.exists():
            return []

        presets = []
        for file in os.listdir(self.custom_dir):
            if file.endswith(".yaml") or file.endswith(".json"):
                presets.append(os.path.splitext(file)[0])
        return presets
