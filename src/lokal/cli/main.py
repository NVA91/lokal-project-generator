"""Main CLI entry point with Click."""

import click
import logging
from pathlib import Path

from lokal.core.config import GlobalConfig
from lokal.cli.commands import generate, list_cmd, preview, config_cmd
from lokal.utils.logging import setup_logging


@click.group(invoke_without_command=True, context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "-v", "--verbose", is_flag=True, help="Enable verbose output"
)
@click.option(
    "--config",
    type=click.Path(),
    default=None,
    help="Path to global config file",
)
@click.version_option()
@click.pass_context
def cli(ctx, verbose, config):
    """Lokal Project Generator - Professional scaffolding tool.

    Create standardized projects with templates, hooks, and automation.
    """
    setup_logging(verbose=verbose)

    config_path = (
        Path(config)
        if config
        else Path.home() / ".lokal" / "config.json"
    )
    global_config = GlobalConfig.from_file(config_path)

    ctx.ensure_object(dict)
    ctx.obj["global_config"] = global_config
    ctx.obj["config_path"] = config_path
    ctx.obj["verbose"] = verbose

    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


cli.add_command(generate.generate)
cli.add_command(list_cmd.list_templates)
cli.add_command(preview.preview)
cli.add_command(config_cmd.config)

if __name__ == "__main__":
    cli(obj={})
