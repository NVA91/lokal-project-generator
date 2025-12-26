"""Project generation logic."""

import logging
import shutil
from pathlib import Path
from typing import Generator, Optional

from lokal.core.template import Template
from lokal.core.exceptions import InvalidTemplate

logger = logging.getLogger(__name__)


class Generator:
    """Generate projects from templates."""

    def __init__(
        self,
        template: Template,
        project_name: str,
        output_path: Path,
        variables: Optional[dict] = None,
    ):
        self.template = template
        self.project_name = project_name
        self.output_path = output_path
        self.variables = variables or {}
        self._setup_variables()

    def _setup_variables(self) -> None:
        """Setup default variables."""
        defaults = {
            "project_name": self.project_name,
            "project_path": str(self.output_path),
        }
        self.variables = {**defaults, **self.variables}

    def generate(
        self, dry_run: bool = False
    ) -> Generator[Path, None, None]:
        """Generate project from template.

        Yields created files.
        """
        if not self.template.validate():
            raise InvalidTemplate("Template validation failed")

        logger.info(
            f"Starting generation for project '{self.project_name}' "
            f"from template '{self.template.config.name}'"
        )

        if not dry_run:
            self.output_path.mkdir(parents=True, exist_ok=True)
        else:
            logger.info("DRY RUN MODE - No files will be created")

        for template_file in self.template.get_files():
            rel_path = template_file.relative_to(self.template.path)

            rendered_filename = rel_path.name
            for key, value in self.variables.items():
                rendered_filename = rendered_filename.replace(
                    f"{{{{{key}}}}}", str(value)
                )

            output_file = self.output_path / rel_path.parent / rendered_filename

            logger.debug(f"Processing: {rel_path}")

            try:
                if template_file.suffix in [
                    ".py",
                    ".md",
                    ".txt",
                    ".json",
                    ".yaml",
                    ".yml",
                    ".toml",
                ]:
                    if not dry_run:
                        output_file.parent.mkdir(parents=True, exist_ok=True)
                        rendered_content = self.template.render_file(
                            template_file, self.variables
                        )
                        output_file.write_text(rendered_content, encoding="utf-8")
                        logger.debug(f"Created (rendered): {output_file}")
                else:
                    if not dry_run:
                        output_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(template_file, output_file)
                        logger.debug(f"Created (copied): {output_file}")

                yield output_file

            except Exception as e:
                logger.error(f"Error processing file {rel_path}: {e}")
                raise

        logger.info(
            f"Project generation completed for '{self.project_name}'"
        )
