"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock
import json
from dataclasses import asdict

from lokal.core.config import GlobalConfig, TemplateConfig
from lokal.core.template import Template
from lokal.core.hooks import HookManager


@pytest.fixture
def temp_dir():
    """Temporary directory for tests."""
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_template_config():
    """Sample template configuration."""
    return TemplateConfig(
        name="sample-project",
        description="A sample template",
        author="Test Author",
        dependencies={"python": ">=3.8"},
        hooks={
            "post_generate": ["echo 'Post-generate hook'"],
            "post_install": ["echo 'Post-install hook'"],
        },
    )


@pytest.fixture
def sample_template(temp_dir, sample_template_config):
    """Create a sample template."""
    template_dir = temp_dir / "sample-template"
    template_dir.mkdir()

    config_file = template_dir / "template.json"
    with open(config_file, "w") as f:
        json.dump(asdict(sample_template_config), f)

    (template_dir / "README.md").write_text(
        "# {{project_name}}\n\nThis is {{project_name}}", encoding="utf-8"
    )
    (template_dir / "main.py").write_text(
        '"""Main module for {{project_name}}."""\nprint("Hello {{project_name}}!")',
        encoding="utf-8",
    )
    (template_dir / "requirements.txt").write_text("click>=8.0\njinja2>=3.0")

    return Template.from_path(template_dir)


@pytest.fixture
def mock_global_config():
    """Mock GlobalConfig."""
    config = MagicMock(spec=GlobalConfig)
    config.author = "Test Author"
    config.default_project_path = "/tmp/projects"
    config.verbose = False
    return config


@pytest.fixture
def mock_hook_manager():
    """Mock HookManager."""
    manager = MagicMock(spec=HookManager)
    manager.execute_stage = MagicMock(return_value=True)
    return manager
