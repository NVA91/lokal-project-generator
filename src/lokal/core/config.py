"""Configuration management for lokal."""

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict
import json
import logging

from lokal.core.exceptions import ConfigError

logger = logging.getLogger(__name__)


@dataclass
class GlobalConfig:
    """Global configuration (~/.lokal/config.json)."""

    author: str = "Developer"
    email: str = ""
    license: str = "MIT"
    default_project_path: str = str(Path.home() / "projects")
    template_paths: list = field(default_factory=list)
    remote_template_sources: list = field(
        default_factory=lambda: [
            "https://github.com/yourusername/lokal-templates"
        ]
    )
    verbose: bool = False

    @classmethod
    def from_file(cls, config_path: Path) -> "GlobalConfig":
        """Load config from JSON file."""
        if not config_path.exists():
            logger.debug(f"Config file not found, using defaults: {config_path}")
            return cls()

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(
                **{
                    k: v
                    for k, v in data.items()
                    if k in cls.__dataclass_fields__
                }
            )
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid config format: {e}")
        except Exception as e:
            raise ConfigError(f"Error loading config: {e}")

    def save(self, config_path: Path) -> None:
        """Save config to JSON file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2)
        logger.info(f"Config saved to {config_path}")


@dataclass
class TemplateConfig:
    """Template-specific configuration (template.json)."""

    name: str
    description: str
    version: str = "1.0.0"
    author: str = ""
    dependencies: Dict[str, str] = field(default_factory=dict)
    ignore_patterns: list = field(
        default_factory=lambda: [
            "*.pyc",
            "__pycache__",
            ".git",
            ".venv",
            "node_modules",
        ]
    )
    hooks: Dict[str, list] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_file(cls, config_path: Path) -> "TemplateConfig":
        """Load template config from JSON."""
        if not config_path.exists():
            raise ConfigError(f"Template config not found: {config_path}")

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(
                **{
                    k: v
                    for k, v in data.items()
                    if k in cls.__dataclass_fields__
                }
            )
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid template config format: {e}")
        except KeyError as e:
            raise ConfigError(f"Missing required field in template config: {e}")

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
