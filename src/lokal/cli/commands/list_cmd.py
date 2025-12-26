"""List command."""

import click
from pathlib import Path

from lokal.core.template import Template
from lokal.cli.utils.formatters import format_info

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None


@click.command("list")
@click.option(
    "-p",
    "--path",
    type=click.Path(exists=True),
    default=None,
    help="Template directory path",
)
@click.pass_context
def list_templates(ctx, path):
    """List available templates."""
    global_config = ctx.obj.get("global_config")

    if path:
        template_paths = [Path(path)]
    else:
        template_paths = [
            Path(global_config.default_project_path).parent / "templates"
        ]

    templates = []

    for template_dir in template_paths:
        if not template_dir.exists():
            click.echo(f"Template directory not found: {template_dir}")
            continue

        for item in template_dir.iterdir():
            if item.is_dir():
                try:
                    template = Template.from_path(item)
                    templates.append(
                        {
                            "Name": template.config.name,
                            "Description": template.config.description,
                            "Version": template.config.version,
                            "Author": template.config.author or "N/A",
                        }
                    )
                except Exception:
                    continue

    if not templates:
        click.echo(format_info("No templates found."))
        return

    click.echo(format_info(f"Found {len(templates)} template(s):"))
    click.echo()
    if tabulate:
        click.echo(tabulate(templates, headers="keys"))
    else:
        for t in templates:
            click.echo(f"  {t['Name']}: {t['Description']}")
