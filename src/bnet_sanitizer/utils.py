"""Utility functions for Battle.net sanitizer."""
import shutil
import subprocess

from rich.console import Console

console = Console()

def kill_wineserver() -> None:
    """Send kill signal to wineserver to clear locked IPC sockets."""
    wineserver_path = shutil.which("wineserver")
    if not wineserver_path:
        # wineserver is not in host PATH (e.g. running inside flatpak)
        return
    try:
        subprocess.run([wineserver_path, "-k"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=False)
        console.print("[dim]✔ Sent kill signal to wineserver[/dim]")
    except FileNotFoundError:
        # wineserver disappeared between which() and execution
        pass
