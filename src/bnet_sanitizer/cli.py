"""Command-line interface for Battle.net sanitizer."""
import typer
from rich.console import Console

from bnet_sanitizer.tasks import (
    clear_shader_caches,
    enforce_bnet_config,
    terminate_zombies,
)

app = typer.Typer(
    name="bnet-sanitizer",
    help="Pre-flight maintenance sanitizer for Battle.net on Linux",
    add_completion=False,
)
console = Console()

@app.command()
def run(
    purge_shaders: bool = typer.Option(
        False, "--purge-shaders", "-s", help="Purge Mesa and Vulkan shader caches"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Show actions without executing changes"
    ),
) -> None:
    """Run pre-flight checks, terminate background zombies, and enforce stable configs."""
    console.print("\n[bold blue]=== Starting Battle.net Pre-Flight Sanitizer ===[/bold blue]")

    if dry_run:
        console.print("[bold magenta]*** DRY RUN MODE ENABLED ***[/bold magenta]\n")

    # Task 1: Terminate Zombies
    killed = terminate_zombies(dry_run=dry_run)
    if killed == 0:
        console.print("[green]✔ No zombie Battle.net/Wine processes found.[/green]")

    # Task 2: Enforce Configuration
    enforce_bnet_config(dry_run=dry_run)

    # Task 3: Optional Shader Purge
    if purge_shaders:
        clear_shader_caches(dry_run=dry_run)

    console.print("[bold green]=== Sanitization Complete. Environment Pristine! ===[/bold green]\n")

if __name__ == "__main__":
    app()
