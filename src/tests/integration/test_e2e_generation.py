"""End-to-end tests for generation."""

import pytest
import asyncio
from pathlib import Path

from lokal.core.generator import Generator
from lokal.core.hooks import HookManager, HookStage
from lokal.core.template import Template


class TestFullGeneration:
    """Test full generation workflow."""

    def test_generate_project_from_template(self, sample_template, temp_dir):
        """Test generating project from template."""
        output_path = temp_dir / "my-project"
        generator = Generator(sample_template, "my-project", output_path)

        files = list(generator.generate(dry_run=False))
        assert len(files) > 0
        assert output_path.exists()
        assert (output_path / "README.md").exists()
        assert (output_path / "main.py").exists()
        assert (output_path / "requirements.txt").exists()

    def test_dry_run_generation(self, sample_template, temp_dir):
        """Test dry-run generation (no files created)."""
        output_path = temp_dir / "dry-run-project"
        generator = Generator(sample_template, "dry-run-project", output_path)

        files = list(generator.generate(dry_run=True))
        assert len(files) > 0
        assert not output_path.exists()

    @pytest.mark.asyncio
    async def test_generation_with_hooks(self, sample_template, temp_dir):
        """Test generation with post-generation hooks."""
        output_path = temp_dir / "my-project"
        generator = Generator(sample_template, "my-project", output_path)

        files = list(generator.generate(dry_run=False))
        assert len(files) > 0

        hook_manager = HookManager()
        hook_manager.load_from_config(sample_template.config.hooks)

        context = {
            "project_name": "my-project",
            "project_path": str(output_path),
        }

        success = await hook_manager.execute_stage(
            HookStage.POST_GENERATE, context
        )
        assert success is True
