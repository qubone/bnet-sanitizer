"""Configuration constants for Battle.net sanitizer."""
import os
from pathlib import Path

# Paths
HOME = Path.home()
WINEPREFIX = HOME / "Games/battlenet"
APPDATA_ROAMING = WINEPREFIX / "drive_c/users" / os.getlogin() / "AppData/Roaming/Battle.net"
LUTRIS_FLATPAK_CACHE = HOME / ".var/app/net.lutris.Lutris/cache/mesa_shader_cache"
LOCAL_MESA_CACHE = HOME / ".cache/mesa_shader_cache"
PREFIX_SHADER_CACHE = WINEPREFIX / "shadercache"

# Target processes to terminate on pre-flight
TARGET_PROCESSES = {
    "battle.net.exe",
    "agent.exe",
    "systemsurvey.exe",
    "blizzarderror.exe"
}
