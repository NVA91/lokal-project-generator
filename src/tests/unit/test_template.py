"""Unit tests for Template class."""

import pytest
from pathlib import Path
from lokal.core.template import Template
from lokal.core.exceptions import TemplateNotFound, InvalidTemplate


class TestTemplateLoading:
    """Test template loading."""

    def test_load_valid_template(self, sample_template):
        """Test loading valid template."""
        assert sample_template.config.name == "sample-project"
        assert sample_template.path.exists()

    def test_load_nonexistent_template(self, temp_dir):
        """Test error on nonexistent template."""
        invalid_path = temp_dir / "nonexistent"
        with pytest.raises(TemplateNotFound):
            Template.from_path(invalid_path)

    def test_load_template_without_config(self, temp_dir):
        """Test error when template.json missing."""
        template_dir = temp_dir / "invalid"
        template_dir.mkdir()
        with pytest.raises(InvalidTemplate):
            Template.from_path(template_dir)


class TestTemplateValidation:
    """Test template validation."""

    def test_validate_valid_template(self, sample_template):
        """Test validation of valid template."""
        assert sample_template.validate() is True


class TestTemplateRendering:
    """Test template file rendering."""

    def test_render_file_with_variables(self, sample_template):
        """Test Jinja2 rendering with variables."""
        variables = {"project_name": "my-project"}
        rendered = sample_template.render_file(
            sample_template.path / "README.md", variables
        )
        assert "my-project" in rendered
        assert "{{project_name}}" not in rendered

    def test_render_multiple_variables(self, sample_template):
        """Test rendering with multiple variables."""
        variables = {"project_name": "awesome-app"}
        rendered = sample_template.render_file(
            sample_template.path / "main.py", variables
        )
        assert "awesome-app" in rendered
        assert rendered.count("awesome-app") == 2


class TestTemplateFiles:
    """Test template file listing."""

    def test_get_files(self, sample_template):
        """Test getting template files."""
        files = list(sample_template.get_files())
        assert len(files) > 0
        assert any(f.name == "README.md" for f in files)
        assert any(f.name == "main.py" for f in files)

    def test_get_files_excludes_template_json(self, sample_template):
        """Test that template.json is excluded."""
        files = list(sample_template.get_files())
        assert not any(f.name == "template.json" for f in files)
