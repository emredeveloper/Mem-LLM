import pytest
import shutil
import uuid
from pathlib import Path

from mem_llm.config_presets import ConfigPresets


class TestConfigPresets:
    @pytest.fixture
    def preset_dir(self):
        root = Path(__file__).resolve().parents[1] / ".tmp"
        root.mkdir(parents=True, exist_ok=True)
        d = root / f"presets_{uuid.uuid4().hex[:8]}"
        d.mkdir(parents=True, exist_ok=True)
        yield d
        shutil.rmtree(d, ignore_errors=True)

    @pytest.fixture
    def presets(self, preset_dir):
        return ConfigPresets(custom_presets_dir=str(preset_dir))

    def test_list_builtin_presets(self, presets):
        """Test listing built-in presets"""
        available = presets.list_presets()

        assert "chatbot" in available
        assert "code_assistant" in available
        assert "creative_writer" in available
        assert len(available) >= 8

    def test_get_builtin_preset(self, presets):
        """Test getting built-in preset"""
        config = presets.get_preset("chatbot")

        assert config["temperature"] == 0.7
        assert config["tools_enabled"] is True
        assert "system_prompt" in config

    def test_get_preset_not_found(self, presets):
        """Test getting non-existent preset"""
        with pytest.raises(ValueError):
            presets.get_preset("non_existent_preset_123")

    def test_save_custom_preset_yaml(self, presets, preset_dir):
        """Test saving custom preset in YAML format"""
        config = {"temperature": 0.8, "max_tokens": 100, "system_prompt": "Custom prompt"}

        presets.save_custom_preset("my_custom_preset", config, format="yaml")

        # Check file exists
        assert (preset_dir / "my_custom_preset.yaml").exists()

        # Check loading
        loaded = presets.get_preset("my_custom_preset")
        assert loaded["temperature"] == 0.8
        assert loaded["system_prompt"] == "Custom prompt"

    def test_save_custom_preset_json(self, presets, preset_dir):
        """Test saving custom preset in JSON format"""
        config = {"temperature": 0.5, "max_tokens": 200}

        presets.save_custom_preset("json_preset", config, format="json")

        # Check file exists
        assert (preset_dir / "json_preset.json").exists()

        # Check loading
        loaded = presets.get_preset("json_preset")
        assert loaded["temperature"] == 0.5

    def test_delete_custom_preset(self, presets, preset_dir):
        """Test deleting custom preset"""
        config = {"test": True}
        presets.save_custom_preset("to_delete", config)

        assert (preset_dir / "to_delete.yaml").exists()

        presets.delete_custom_preset("to_delete")

        assert not (preset_dir / "to_delete.yaml").exists()

    def test_cannot_override_builtin(self, presets):
        """Test that built-in presets cannot be overridden"""
        with pytest.raises(ValueError):
            presets.save_custom_preset("chatbot", {})

    def test_cannot_delete_builtin(self, presets):
        """Test that built-in presets cannot be deleted"""
        with pytest.raises(ValueError):
            presets.delete_custom_preset("chatbot")

    def test_list_custom_presets(self, presets):
        """Test listing custom presets"""
        presets.save_custom_preset("custom1", {})
        presets.save_custom_preset("custom2", {})

        available = presets.list_presets()

        assert "custom1" in available
        assert "custom2" in available
        assert "chatbot" in available
