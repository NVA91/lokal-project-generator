"""Preview command."""

import click
from pathlib import Path

from lokal.core.template import Template
from lokal.cli.utils.formatters import format_info, format_error


@click.command("preview")
@click.argument("template", type=click.Path(exists=True))
@click.pass_context
def preview(ctx, template):
    """Preview template structure and configuration."""
    verbose = ctx.obj.get("verbose")

    try:
        template_path = Path(template)
        template_obj = Template.from_path(template_path)

        click.echo(format_info(f"Template: {template_obj.config.name}"))
        click.echo(f"Description: {template_obj.config.description}")
        click.echo(f"Version: {template_obj.config.version}")
        click.echo(f"Author: {template_obj.config.author or 'N/A'}")
        click.echo()

        click.echo(format_info("Files in template:"))
        files = list(template_obj.get_files())
        for f in files:
            rel_path = f.relative_to(template_path)
            click.echo(f"  - {rel_path}")

        if template_obj.config.hooks:
            click.echo()
            click.echo(format_info("Hooks:"))
            for stage, commands in template_obj.config.hooks.items():
                click.echo(f"  {stage}:")
                for cmd in commands:
                    click.echo(f"    - {cmd}")

    except Exception as e:
        click.echo(format_error(f"Error: {e}"))
        if verbose:
            raise
        raise click.Exit(1)
