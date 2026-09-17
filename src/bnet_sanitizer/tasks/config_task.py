"""Task to enforce Battle.net configuration settings."""
import json

from rich.console import Console

from bnet_sanitizer.config import APPDATA_ROAMING

console = Console()

def enforce_bnet_config(dry_run: bool = False) -> bool:
    """Enforce HardwareAcceleration = false in Battle.net.config."""
    config_file = APPDATA_ROAMING / "Battle.net.config"

    if not APPDATA_ROAMING.exists() and not dry_run:
        APPDATA_ROAMING.mkdir(parents=True, exist_ok=True)

    if not config_file.exists():
        console.print("[dim]Battle.net.config does not exist yet. Skipping config task.[/dim]")
        return False

    try:
        with open(config_file, "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}

            client_cfg = data.setdefault("Client", {})
            if client_cfg.get("HardwareAcceleration") == "false":
                console.print("[green]✔ Hardware acceleration is already disabled in config.[/green]")
                return True

            client_cfg["HardwareAcceleration"] = "false"

            if not dry_run:
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            console.print("[bold green]✔ Disabled Hardware Acceleration in Battle.net.config[/bold green]")
            return True

    except OSError as e:
        console.print(f"[red]Failed to read/write Battle.net.config: {e}[/red]")
        return False
