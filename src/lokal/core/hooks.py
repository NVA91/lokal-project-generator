"""Hook system for post-generation actions."""

import asyncio
import logging
import subprocess
from enum import Enum
from typing import List, Optional

logger = logging.getLogger(__name__)


class HookStage(Enum):
    """Hook execution stages."""

    PRE_GENERATE = "pre_generate"
    POST_GENERATE = "post_generate"
    POST_INSTALL = "post_install"


class Hook:
    """Single hook command."""

    def __init__(
        self,
        name: str,
        stage: HookStage,
        command: str,
        async_execution: bool = False,
    ):
        self.name = name
        self.stage = stage
        self.command = command
        self.async_execution = async_execution

    async def execute(self, context: dict) -> bool:
        """Execute the hook."""
        logger.info(f"Executing hook: {self.name}")

        try:
            interpolated_cmd = self._interpolate(self.command, context)
            logger.debug(f"Command: {interpolated_cmd}")

            if self.async_execution:
                proc = await asyncio.create_subprocess_shell(
                    interpolated_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
            else:
                result = subprocess.run(
                    interpolated_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                )
                stdout, stderr = result.stdout, result.stderr

                if result.returncode != 0:
                    logger.error(f"Hook {self.name} failed: {stderr}")
                    return False

            if stdout:
                logger.debug(f"Hook output: {stdout}")
            return True

        except Exception as e:
            logger.error(f"Hook execution error: {e}")
            return False

    @staticmethod
    def _interpolate(command: str, context: dict) -> str:
        """Interpolate variables in command."""
        result = command
        for key, value in context.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))
        return result


class HookManager:
    """Manage and execute hooks."""

    def __init__(self):
        self.hooks: dict[HookStage, List[Hook]] = {stage: [] for stage in HookStage}

    def register(self, hook: Hook) -> None:
        """Register a hook."""
        self.hooks[hook.stage].append(hook)
        logger.debug(f"Registered hook: {hook.name}")

    async def execute_stage(
        self, stage: HookStage, context: dict
    ) -> bool:
        """Execute all hooks for a stage."""
        if not self.hooks[stage]:
            logger.debug(f"No hooks for stage: {stage.value}")
            return True

        logger.info(f"Executing hooks for stage: {stage.value}")

        results = await asyncio.gather(
            *[hook.execute(context) for hook in self.hooks[stage]]
        )

        success = all(results)
        if success:
            logger.info(f"All hooks for {stage.value} completed successfully")
        else:
            logger.warning(f"Some hooks for {stage.value} failed")

        return success

    def load_from_config(self, config: dict) -> None:
        """Load hooks from template config."""
        for stage_name, commands in config.items():
            try:
                stage = HookStage(stage_name)
                for i, cmd in enumerate(commands):
                    hook = Hook(
                        name=f"{stage_name}_{i}",
                        stage=stage,
                        command=cmd,
                    )
                    self.register(hook)
            except ValueError:
                logger.warning(f"Unknown hook stage: {stage_name}")
