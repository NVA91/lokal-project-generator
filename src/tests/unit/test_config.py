"""Unit tests for configuration."""

import pytest
import json
from pathlib import Path
from lokal.core.config import GlobalConfig, TemplateConfig
from lokal.core.exceptions import ConfigError


class TestGlobalConfig:
    """Test GlobalConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = GlobalConfig()
        assert config.author == "Developer"
        assert config.license == "MIT"
        assert config.verbose is False

    def test_save_config(self, temp_dir):
        """Test saving config to file."""
        config = GlobalConfig(author="Test Author", email="test@example.com")
        config_file = temp_dir / "config.json"
        config.save(config_file)

        assert config_file.exists()
        with open(config_file) as f:
            data = json.load(f)
        assert data["author"] == "Test Author"
        assert data["email"] == "test@example.com"

    def test_load_config(self, temp_dir):
        """Test loading config from file."""
        config_file = temp_dir / "config.json"
        config_data = {
            "author": "Loaded Author",
            "email": "loaded@example.com",
            "license": "Apache-2.0",
        }
        with open(config_file, "w") as f:
            json.dump(config_data, f)

        loaded_config = GlobalConfig.from_file(config_file)
        assert loaded_config.author == "Loaded Author"
        assert loaded_config.email == "loaded@example.com"
        assert loaded_config.license == "Apache-2.0"

    def test_load_nonexistent_config(self, temp_dir):
        """Test loading nonexistent config returns defaults."""
        config = GlobalConfig.from_file(temp_dir / "nonexistent.json")
        assert config.author == "Developer"


class TestTemplateConfig:
    """Test TemplateConfig."""

    def test_default_template_config(self):
        """Test default template configuration."""
        config = TemplateConfig(name="test", description="Test template")
        assert config.name == "test"
        assert config.version == "1.0.0"
