"""Unit tests for hook system."""

import pytest
import asyncio
from lokal.core.hooks import Hook, HookManager, HookStage


class TestHook:
    """Test Hook class."""

    def test_hook_creation(self):
        """Test creating a hook."""
        hook = Hook(
            name="test",
            stage=HookStage.POST_GENERATE,
            command="echo 'test'",
        )
        assert hook.name == "test"
        assert hook.stage == HookStage.POST_GENERATE

    @pytest.mark.asyncio
    async def test_execute_simple_command(self):
        """Test executing a simple command."""
        hook = Hook(
            name="test",
            stage=HookStage.POST_GENERATE,
            command="echo 'hello'",
        )
        result = await hook.execute({})
        assert result is True

    def test_hook_command_interpolation(self):
        """Test command variable interpolation."""
        context = {"project_name": "my-app", "path": "/tmp"}
        cmd = Hook._interpolate("mkdir {{path}}/{{project_name}}", context)
        assert cmd == "mkdir /tmp/my-app"


class TestHookManager:
    """Test HookManager."""

    def test_register_hook(self):
        """Test registering hooks."""
        manager = HookManager()
        hook = Hook(
            name="test",
            stage=HookStage.POST_GENERATE,
            command="echo 'test'",
        )
        manager.register(hook)
        assert len(manager.hooks[HookStage.POST_GENERATE]) == 1

    def test_load_hooks_from_config(self):
        """Test loading hooks from config."""
        manager = HookManager()
        config = {
            "post_generate": ["git init", "git add ."],
            "post_install": ["pip install -r requirements.txt"],
        }
        manager.load_from_config(config)
        assert len(manager.hooks[HookStage.POST_GENERATE]) == 2
        assert len(manager.hooks[HookStage.POST_INSTALL]) == 1
