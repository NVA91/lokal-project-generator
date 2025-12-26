"""Input validators."""

import re
from pathlib import Path


def validate_project_name(name: str) -> None:
    """Validate project name.

    Args:
        name: Project name to validate

    Raises:
        ValueError: If name is invalid
    """
    pattern = r"^[a-z0-9]([a-z0-9-_]*[a-z0-9])?$"

    if not re.match(pattern, name, re.IGNORECASE):
        raise ValueError(
            f"Invalid project name '{name}'. "
            "Use alphanumeric characters, hyphens, and underscores. "
            "Start and end with alphanumeric."
        )


def validate_path(path: Path, allow_existing: bool = True) -> None:
    """Validate output path.

    Args:
        path: Path to validate
        allow_existing: Whether to allow existing paths

    Raises:
        ValueError: If path is invalid
    """
    if path.exists() and not allow_existing:
        raise ValueError(
            f"Path already exists: {path}. "
            "Use --output to specify a different location."
        )
