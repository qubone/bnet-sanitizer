"""Tests for shader task."""
from pathlib import Path
from unittest.mock import MagicMock, patch

from bnet_sanitizer.tasks.shader_task import clear_shader_caches


class TestClearShaderCaches:
    """Tests for clear_shader_caches function."""

    @patch("bnet_sanitizer.tasks.shader_task.shutil.rmtree")
    @patch("bnet_sanitizer.tasks.shader_task.console.print")
    def test_clear_shader_caches_dry_run(self, mock_print: MagicMock, mock_rmtree: MagicMock) -> None:
        """Test dry run mode does not delete directories."""
        with patch("bnet_sanitizer.tasks.shader_task.LUTRIS_FLATPAK_CACHE") as mock_cache1, patch(
            "bnet_sanitizer.tasks.shader_task.LOCAL_MESA_CACHE"
        ) as mock_cache2, patch("bnet_sanitizer.tasks.shader_task.PREFIX_SHADER_CACHE") as mock_cache3:
            mock_cache1.exists.return_value = True
            mock_cache2.exists.return_value = False
            mock_cache3.exists.return_value = False
            mock_cache1.is_dir.return_value = True

            clear_shader_caches(dry_run=True)

            mock_rmtree.assert_not_called()

    @patch("bnet_sanitizer.tasks.shader_task.shutil.rmtree")
    @patch("bnet_sanitizer.tasks.shader_task.console.print")
    def test_clear_shader_caches_remove_directory(self, mock_print: MagicMock, mock_rmtree: MagicMock) -> None:
        """Test removing directory shader cache."""
        with patch("bnet_sanitizer.tasks.shader_task.LUTRIS_FLATPAK_CACHE") as mock_cache1, patch(
            "bnet_sanitizer.tasks.shader_task.LOCAL_MESA_CACHE"
        ) as mock_cache2, patch("bnet_sanitizer.tasks.shader_task.PREFIX_SHADER_CACHE") as mock_cache3:
            mock_cache1.exists.return_value = True
            mock_cache2.exists.return_value = False
            mock_cache3.exists.return_value = False
            mock_cache1.is_dir.return_value = True

            clear_shader_caches(dry_run=False)

            mock_rmtree.assert_called_once_with(mock_cache1)

    @patch("bnet_sanitizer.tasks.shader_task.console.print")
    def test_clear_shader_caches_remove_file(self, mock_print: MagicMock) -> None:
        """Test removing file shader cache."""
        with patch("bnet_sanitizer.tasks.shader_task.LUTRIS_FLATPAK_CACHE") as mock_cache1, patch(
            "bnet_sanitizer.tasks.shader_task.LOCAL_MESA_CACHE"
        ) as mock_cache2, patch("bnet_sanitizer.tasks.shader_task.PREFIX_SHADER_CACHE") as mock_cache3:
            mock_cache1.exists.return_value = True
            mock_cache2.exists.return_value = False
            mock_cache3.exists.return_value = False
            mock_cache1.is_dir.return_value = False
            mock_cache1.unlink = MagicMock()

            clear_shader_caches(dry_run=False)

            mock_cache1.unlink.assert_called_once()

    @patch("bnet_sanitizer.tasks.shader_task.shutil.rmtree")
    @patch("bnet_sanitizer.tasks.shader_task.console.print")
    def test_clear_shader_caches_no_caches_exist(self, mock_print: MagicMock, mock_rmtree: MagicMock) -> None:
        """Test when no shader caches exist."""
        with patch("bnet_sanitizer.tasks.shader_task.LUTRIS_FLATPAK_CACHE") as mock_cache1, patch(
            "bnet_sanitizer.tasks.shader_task.LOCAL_MESA_CACHE"
        ) as mock_cache2, patch("bnet_sanitizer.tasks.shader_task.PREFIX_SHADER_CACHE") as mock_cache3:
            mock_cache1.exists.return_value = False
            mock_cache2.exists.return_value = False
            mock_cache3.exists.return_value = False

            clear_shader_caches(dry_run=False)

            mock_rmtree.assert_not_called()

    @patch("bnet_sanitizer.tasks.shader_task.shutil.rmtree")
    @patch("bnet_sanitizer.tasks.shader_task.console.print")
    def test_clear_shader_caches_rmtree_error(self, mock_print: MagicMock, mock_rmtree: MagicMock) -> None:
        """Test handling of OSError during rmtree."""
        with patch("bnet_sanitizer.tasks.shader_task.LUTRIS_FLATPAK_CACHE") as mock_cache1, patch(
            "bnet_sanitizer.tasks.shader_task.LOCAL_MESA_CACHE"
        ) as mock_cache2, patch("bnet_sanitizer.tasks.shader_task.PREFIX_SHADER_CACHE") as mock_cache3:
            mock_cache1.exists.return_value = True
            mock_cache2.exists.return_value = False
            mock_cache3.exists.return_value = False
            mock_cache1.is_dir.return_value = True
            mock_rmtree.side_effect = OSError("Permission denied")

            clear_shader_caches(dry_run=False)

            assert any("Failed" in str(call) for call in mock_print.call_args_list)

    @patch("bnet_sanitizer.tasks.shader_task.console.print")
    def test_clear_shader_caches_unlink_error(self, mock_print: MagicMock) -> None:
        """Test handling of OSError during unlink."""
        with patch("bnet_sanitizer.tasks.shader_task.LUTRIS_FLATPAK_CACHE") as mock_cache1, patch(
            "bnet_sanitizer.tasks.shader_task.LOCAL_MESA_CACHE"
        ) as mock_cache2, patch("bnet_sanitizer.tasks.shader_task.PREFIX_SHADER_CACHE") as mock_cache3:
            mock_cache1.exists.return_value = True
            mock_cache2.exists.return_value = False
            mock_cache3.exists.return_value = False
            mock_cache1.is_dir.return_value = False
            mock_cache1.unlink.side_effect = OSError("Read-only file system")

            clear_shader_caches(dry_run=False)

            assert any("Failed" in str(call) for call in mock_print.call_args_list)

    @patch("bnet_sanitizer.tasks.shader_task.shutil.rmtree")
    @patch("bnet_sanitizer.tasks.shader_task.console.print")
    def test_clear_shader_caches_multiple_paths(self, mock_print: MagicMock, mock_rmtree: MagicMock) -> None:
        """Test clearing multiple shader cache paths."""
        with patch("bnet_sanitizer.tasks.shader_task.LUTRIS_FLATPAK_CACHE") as mock_cache1, patch(
            "bnet_sanitizer.tasks.shader_task.LOCAL_MESA_CACHE"
        ) as mock_cache2, patch("bnet_sanitizer.tasks.shader_task.PREFIX_SHADER_CACHE") as mock_cache3:
            mock_cache1.exists.return_value = True
            mock_cache2.exists.return_value = True
            mock_cache3.exists.return_value = True
            mock_cache1.is_dir.return_value = True
            mock_cache2.is_dir.return_value = True
            mock_cache3.is_dir.return_value = True

            clear_shader_caches(dry_run=False)

            assert mock_rmtree.call_count == 3
