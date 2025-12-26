"""Config command."""

import click
import json
from pathlib import Path

from lokal.core.config import GlobalConfig
from lokal.cli.utils.formatters import format_success, format_info, format_error


@click.group("config")
def config():
    """Manage global configuration."""
    pass


@config.command("show")
@click.pass_context
def show_config(ctx):
    """Show current configuration."""
    config_path = ctx.obj.get("config_path")
    global_config = ctx.obj.get("global_config")

    click.echo(format_info(f"Config file: {config_path}"))
    click.echo()
    click.echo(json.dumps(global_config.__dict__, indent=2))


@config.command("set")
@click.argument("key", type=str)
@click.argument("value", type=str)
@click.pass_context
def set_config(ctx, key, value):
    """Set configuration value."""
    config_path = ctx.obj.get("config_path")
    global_config = ctx.obj.get("global_config")

    if not hasattr(global_config, key):
        click.echo(format_error(f"Unknown config key: {key}"))
        raise click.Exit(1)

    setattr(global_config, key, value)
    global_config.save(config_path)

    click.echo(format_success(f"Set {key}={value}"))


@config.command("reset")
@click.confirmation_option(
    prompt="Are you sure you want to reset config to defaults?"
)
@click.pass_context
def reset_config(ctx):
    """Reset configuration to defaults."""
    config_path = ctx.obj.get("config_path")
    default_config = GlobalConfig()
    default_config.save(config_path)

    click.echo(format_success("Config reset to defaults"))
