"""Task to purge shader caches."""
import shutil

from rich.console import Console

from bnet_sanitizer.config import (
    LOCAL_MESA_CACHE,
    LUTRIS_FLATPAK_CACHE,
    PREFIX_SHADER_CACHE,
)

console = Console()

def clear_shader_caches(dry_run: bool = False) -> None:
    """Purge driver and prefix level Mesa/VKD3D shader caches."""
    targets = [LUTRIS_FLATPAK_CACHE, LOCAL_MESA_CACHE, PREFIX_SHADER_CACHE]

    for path in targets:
        if path.exists():
            console.print(f"[yellow]Purging shader cache:[/yellow] {path}")
            if not dry_run:
                try:
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                except OSError as e:
                    console.print(f"[red]Failed to purge {path}: {e}[/red]")
