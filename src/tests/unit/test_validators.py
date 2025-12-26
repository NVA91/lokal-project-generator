"""Unit tests for validators."""

import pytest
from lokal.cli.utils.validators import validate_project_name, validate_path
from pathlib import Path


class TestProjectNameValidation:
    """Test project name validation."""

    @pytest.mark.parametrize(
        "name,valid",
        [
            ("my-project", True),
            ("my_project", True),
            ("MyProject", True),
            ("project123", True),
            ("a", True),
            ("-invalid", False),
            ("invalid-", False),
            ("invalid space", False),
        ],
    )
    def test_project_name_validation(self, name, valid):
        """Test project name validation."""
        if valid:
            validate_project_name(name)
        else:
            with pytest.raises(ValueError):
                validate_project_name(name)
