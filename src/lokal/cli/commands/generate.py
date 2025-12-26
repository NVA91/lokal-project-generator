"""Generate command."""

import asyncio
import click
import logging
from pathlib import Path

from lokal.core.template import Template
from lokal.core.generator import Generator
from lokal.core.hooks import HookManager, HookStage
from lokal.cli.utils.validators import validate_project_name, validate_path
from lokal.cli.utils.formatters import format_success, format_error, format_info

logger = logging.getLogger(__name__)


@click.command("generate")
@click.argument("template", type=click.Path(exists=True))
@click.argument("project_name", type=str)
@click.option(
    "-o",
    "--output",
    type=click.Path(),
    default=None,
    help="Output directory",
)
@click.option(
    "--skip-hooks",
    is_flag=True,
    help="Skip post-generation hooks",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Preview generation without creating files",
)
@click.pass_context
def generate(ctx, template, project_name, output, skip_hooks, dry_run):
    """Generate new project from template.

    TEMPLATE: Path to template directory
    PROJECT_NAME: Name for your new project
    """
    global_config = ctx.obj.get("global_config")
    verbose = ctx.obj.get("verbose")

    try:
        validate_project_name(project_name)
        template_path = Path(template)

        if not template_path.exists():
            raise click.BadParameter(f"Template not found: {template}")

        if output:
            output_path = Path(output) / project_name
        else:
            output_path = Path(global_config.default_project_path) / project_name

        validate_path(output_path, allow_existing=False)

        template_obj = Template.from_path(template_path)

        generator = Generator(template_obj, project_name, output_path)

        mode = "DRY RUN" if dry_run else "GENERATION"
        with click.progressbar(
            generator.generate(dry_run=dry_run),
            label=f"{mode} project",
            show_pos=True,
        ) as bar:
            for _ in bar:
                pass

        if not skip_hooks:
            hook_manager = HookManager()
            hook_manager.load_from_config(template_obj.config.hooks)

            context = {
                "project_name": project_name,
                "project_path": str(output_path),
                "template_name": template_obj.config.name,
            }

            success = asyncio.run(
                hook_manager.execute_stage(HookStage.POST_GENERATE, context)
            )

            if not success and verbose:
                logger.warning("Some hooks failed, but project was created")

        click.echo(format_success(f"✅ Project '{project_name}' created successfully!"))

        if not dry_run:
            click.echo(format_info(f"Location: {output_path}"))
            click.echo("\n📝 Next steps:")
            click.echo(f"  cd {output_path}")
            click.echo(f"  python -m venv .venv")
            click.echo(
                f"  source .venv/bin/activate  # Windows: .venv\\\\Scripts\\\\activate"
            )
            click.echo(f"  pip install -r requirements.txt")

    except click.BadParameter as e:
        click.echo(format_error(f"Invalid parameter: {e}"))
        raise click.Exit(1)
    except Exception as e:
        click.echo(format_error(f"Error: {e}"))
        if verbose:
            logger.exception("Detailed error:")
        raise click.Exit(1)
