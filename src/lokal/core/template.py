"""Template class and management."""

from dataclasses import dataclass
from pathlib import Path
import logging
from typing import Generator

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from lokal.core.config import TemplateConfig
from lokal.core.exceptions import InvalidTemplate, TemplateNotFound

logger = logging.getLogger(__name__)


@dataclass
class Template:
    """Represents a template."""

    path: Path
    config: TemplateConfig

    @classmethod
    def from_path(cls, template_path: Path) -> "Template":
        """Load template from directory."""
        if not template_path.exists():
            raise TemplateNotFound(f"Template not found: {template_path}")

        config_path = template_path / "template.json"
        if not config_path.exists():
            raise InvalidTemplate(
                f"template.json not found in {template_path}"
            )

        config = TemplateConfig.from_file(config_path)
        logger.info(f"Loaded template: {config.name} from {template_path}")
        return cls(path=template_path, config=config)

    def render_file(self, file_path: Path, variables: dict) -> str:
        """Render file with Jinja2 variables."""
        jinja_env = Environment(
            loader=FileSystemLoader(self.path),
            undefined=StrictUndefined,
        )
        rel_path = file_path.relative_to(self.path)
        template = jinja_env.get_template(str(rel_path))
        return template.render(**variables)

    def validate(self) -> bool:
        """Validate template structure."""
        required_files = [
            self.path / "template.json",
        ]

        for file in required_files:
            if not file.exists():
                logger.error(f"Required file missing: {file}")
                return False

        logger.info(f"Template validation passed for {self.config.name}")
        return True

    def get_files(self) -> Generator[Path, None, None]:
        """Get all files in template (excluding ignored patterns and template.json)."""
        import fnmatch

        for item in self.path.rglob("*"):
            if item.is_file():
                if item.name == "template.json":
                    continue

                rel_path = item.relative_to(self.path)
                should_ignore = any(
                    fnmatch.fnmatch(str(rel_path), pattern)
                    for pattern in self.config.ignore_patterns
                )

                if not should_ignore:
                    yield item
