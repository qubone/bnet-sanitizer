"""Tests for configuration module."""
from pathlib import Path

from bnet_sanitizer.config import (
    APPDATA_ROAMING,
    LOCAL_MESA_CACHE,
    LUTRIS_FLATPAK_CACHE,
    PREFIX_SHADER_CACHE,
    TARGET_PROCESSES,
    WINEPREFIX,
)


class TestConfig:
    """Tests for configuration constants."""

    def test_target_processes_is_set(self) -> None:
        """Test TARGET_PROCESSES is defined."""
        assert isinstance(TARGET_PROCESSES, set)
        assert len(TARGET_PROCESSES) > 0

    def test_target_processes_contains_expected_values(self) -> None:
        """Test TARGET_PROCESSES contains expected process names."""
        assert "battle.net.exe" in TARGET_PROCESSES
        assert "agent.exe" in TARGET_PROCESSES
        assert "systemsurvey.exe" in TARGET_PROCESSES
        assert "blizzarderror.exe" in TARGET_PROCESSES

    def test_paths_are_path_objects(self) -> None:
        """Test all path configuration are Path objects."""
        assert isinstance(WINEPREFIX, Path)
        assert isinstance(APPDATA_ROAMING, Path)
        assert isinstance(LUTRIS_FLATPAK_CACHE, Path)
        assert isinstance(LOCAL_MESA_CACHE, Path)
        assert isinstance(PREFIX_SHADER_CACHE, Path)

    def test_wineprefix_path_contains_games_battlenet(self) -> None:
        """Test WINEPREFIX contains Games/battlenet."""
        assert "Games" in str(WINEPREFIX) or "games" in str(WINEPREFIX.as_posix().lower())

    def test_appdata_roaming_path_contains_battle_net(self) -> None:
        """Test APPDATA_ROAMING contains Battle.net."""
        assert "Battle.net" in str(APPDATA_ROAMING)

    def test_lutris_flatpak_cache_path_format(self) -> None:
        """Test LUTRIS_FLATPAK_CACHE has expected format."""
        assert ".var/app/net.lutris.Lutris" in str(LUTRIS_FLATPAK_CACHE) or "var" in str(LUTRIS_FLATPAK_CACHE).lower()

    def test_local_mesa_cache_path_format(self) -> None:
        """Test LOCAL_MESA_CACHE has expected format."""
        assert ".cache" in str(LOCAL_MESA_CACHE) or "cache" in str(LOCAL_MESA_CACHE).lower()

    def test_prefix_shader_cache_path_format(self) -> None:
        """Test PREFIX_SHADER_CACHE has expected format."""
        assert "shadercache" in str(PREFIX_SHADER_CACHE).lower()
