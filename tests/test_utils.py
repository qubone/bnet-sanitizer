"""Tests for utility functions."""
from unittest.mock import MagicMock, patch

import pytest

from bnet_sanitizer.utils import kill_wineserver


class TestKillWineserver:
    """Tests for kill_wineserver function."""

    @patch("bnet_sanitizer.utils.shutil.which")
    @patch("bnet_sanitizer.utils.subprocess.run")
    @patch("bnet_sanitizer.utils.console.print")
    def test_kill_wineserver_success(
        self, mock_print: MagicMock, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        """Test successful wineserver kill."""
        import subprocess

        mock_which.return_value = "/usr/bin/wineserver"
        kill_wineserver()
        mock_which.assert_called_once_with("wineserver")
        mock_run.assert_called_once_with(
            ["/usr/bin/wineserver", "-k"], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL, check=False
        )
        mock_print.assert_called_once_with("[dim]\u2714 Sent kill signal to wineserver[/dim]")

    @patch("bnet_sanitizer.utils.shutil.which")
    @patch("bnet_sanitizer.utils.subprocess.run")
    @patch("bnet_sanitizer.utils.console.print")
    def test_kill_wineserver_not_found(
        self, mock_print: MagicMock, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        """Test wineserver not found in PATH."""
        mock_which.return_value = None
        kill_wineserver()
        mock_run.assert_not_called()
        mock_print.assert_not_called()

    @patch("bnet_sanitizer.utils.shutil.which")
    @patch("bnet_sanitizer.utils.subprocess.run")
    @patch("bnet_sanitizer.utils.console.print")
    def test_kill_wineserver_file_not_found_error(
        self, mock_print: MagicMock, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        """Test FileNotFoundError during subprocess execution."""
        mock_which.return_value = "/usr/bin/wineserver"
        mock_run.side_effect = FileNotFoundError("wineserver disappeared")
        kill_wineserver()
        mock_run.assert_called_once()
        mock_print.assert_not_called()

    @patch("bnet_sanitizer.utils.shutil.which")
    @patch("bnet_sanitizer.utils.subprocess.run")
    @patch("bnet_sanitizer.utils.console.print")
    def test_kill_wineserver_subprocess_error(
        self, mock_print: MagicMock, mock_run: MagicMock, mock_which: MagicMock
    ) -> None:
        """Test subprocess raises other exceptions."""
        mock_which.return_value = "/usr/bin/wineserver"
        mock_run.side_effect = Exception("Some error")
        with pytest.raises(Exception):
            kill_wineserver()
