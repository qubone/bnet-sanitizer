"""Task to terminate zombie processes and wineserver."""
import psutil
from rich.console import Console

from bnet_sanitizer.config import TARGET_PROCESSES
from bnet_sanitizer.utils import kill_wineserver

console = Console()

def terminate_zombies(dry_run: bool = False) -> int:
    """Find and terminate leftover Battle.net and Wine processes."""
    killed_count = 0
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pname = proc.info['name']
            if pname and pname.lower() in TARGET_PROCESSES:
                console.print(f"[yellow]Terminating target process:[/yellow] {pname} (PID: {proc.info['pid']})")
                if not dry_run:
                    p = psutil.Process(proc.info['pid'])
                    p.kill()
                killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if not dry_run and killed_count > 0:
        kill_wineserver()

    return killed_count
