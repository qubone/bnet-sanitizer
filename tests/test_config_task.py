"""Tests for config task."""
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from bnet_sanitizer.tasks.config_task import enforce_bnet_config


class TestEnforceBnetConfig:
    """Tests for enforce_bnet_config function."""

    @patch("bnet_sanitizer.tasks.config_task.APPDATA_ROAMING")
    @patch("bnet_sanitizer.tasks.config_task.console.print")
    def test_config_file_does_not_exist(
        self, mock_print: MagicMock, mock_appdata: MagicMock
    ) -> None:
        """Test when config file does not exist."""
        mock_appdata.exists.return_value = False
        mock_config_file = MagicMock()
        mock_config_file.exists.return_value = False
        mock_appdata.__truediv__ = MagicMock(return_value=mock_config_file)

        result = enforce_bnet_config(dry_run=False)

        assert result is False
        mock_print.assert_called_once()
        assert "does not exist" in str(mock_print.call_args)

    @patch("builtins.open")
    @patch("bnet_sanitizer.tasks.config_task.APPDATA_ROAMING")
    @patch("bnet_sanitizer.tasks.config_task.console.print")
    def test_config_already_disabled(
        self, mock_print: MagicMock, mock_appdata: MagicMock, mock_open: MagicMock
    ) -> None:
        """Test when hardware acceleration is already disabled."""
        mock_appdata.exists.return_value = True
        mock_config_file = MagicMock()
        mock_config_file.exists.return_value = True
        mock_appdata.__truediv__ = MagicMock(return_value=mock_config_file)

        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_open.return_value = mock_file
        mock_file.read.return_value = '{"Client": {"HardwareAcceleration": "false"}}'
        mock_file.__iter__ = MagicMock(return_value=iter([]))

        with patch("json.load", return_value={"Client": {"HardwareAcceleration": "false"}}):
            result = enforce_bnet_config(dry_run=False)

        assert result is True
        assert any("already disabled" in str(call) for call in mock_print.call_args_list)

    @patch("builtins.open")
    @patch("bnet_sanitizer.tasks.config_task.APPDATA_ROAMING")
    @patch("bnet_sanitizer.tasks.config_task.console.print")
    def test_config_hardware_acceleration_disabled(
        self, mock_print: MagicMock, mock_appdata: MagicMock, mock_open: MagicMock
    ) -> None:
        """Test successfully disabling hardware acceleration."""
        mock_appdata.exists.return_value = True
        mock_config_file = MagicMock()
        mock_config_file.exists.return_value = True
        mock_appdata.__truediv__ = MagicMock(return_value=mock_config_file)

        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_open.return_value = mock_file

        with patch("json.load", return_value={"Client": {}}), patch("json.dump") as mock_dump:
            result = enforce_bnet_config(dry_run=False)

        assert result is True
        mock_dump.assert_called_once()
        assert any("Disabled" in str(call) for call in mock_print.call_args_list)

    @patch("builtins.open")
    @patch("bnet_sanitizer.tasks.config_task.APPDATA_ROAMING")
    @patch("bnet_sanitizer.tasks.config_task.console.print")
    def test_config_dry_run(
        self, mock_print: MagicMock, mock_appdata: MagicMock, mock_open: MagicMock
    ) -> None:
        """Test dry run mode does not write file."""
        mock_appdata.exists.return_value = True
        mock_config_file = MagicMock()
        mock_config_file.exists.return_value = True
        mock_appdata.__truediv__ = MagicMock(return_value=mock_config_file)

        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_open.return_value = mock_file

        with patch("json.load", return_value={"Client": {}}), patch("json.dump") as mock_dump:
            result = enforce_bnet_config(dry_run=True)

        assert result is True
        mock_dump.assert_not_called()

    @patch("builtins.open")
    @patch("bnet_sanitizer.tasks.config_task.APPDATA_ROAMING")
    @patch("bnet_sanitizer.tasks.config_task.console.print")
    def test_config_json_decode_error(
        self, mock_print: MagicMock, mock_appdata: MagicMock, mock_open: MagicMock
    ) -> None:
        """Test handling of JSON decode error."""
        mock_appdata.exists.return_value = True
        mock_config_file = MagicMock()
        mock_config_file.exists.return_value = True
        mock_appdata.__truediv__ = MagicMock(return_value=mock_config_file)

        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_open.return_value = mock_file

        with patch("json.load", side_effect=json.JSONDecodeError("", "", 0)), patch("json.dump") as mock_dump:
            result = enforce_bnet_config(dry_run=False)

        assert result is True
        mock_dump.assert_called_once()

    @patch("builtins.open")
    @patch("bnet_sanitizer.tasks.config_task.APPDATA_ROAMING")
    @patch("bnet_sanitizer.tasks.config_task.console.print")
    def test_config_oserror(
        self, mock_print: MagicMock, mock_appdata: MagicMock, mock_open: MagicMock
    ) -> None:
        """Test handling of OSError."""
        mock_appdata.exists.return_value = True
        mock_config_file = MagicMock()
        mock_config_file.exists.return_value = True
        mock_appdata.__truediv__ = MagicMock(return_value=mock_config_file)

        mock_open.side_effect = OSError("Permission denied")

        result = enforce_bnet_config(dry_run=False)

        assert result is False
        assert any("Failed" in str(call) for call in mock_print.call_args_list)

    @patch("bnet_sanitizer.tasks.config_task.APPDATA_ROAMING")
    @patch("bnet_sanitizer.tasks.config_task.console.print")
    def test_config_creates_directory(self, mock_print: MagicMock, mock_appdata: MagicMock) -> None:
        """Test directory creation when it does not exist."""
        mock_appdata.exists.return_value = False
        mock_config_file = MagicMock()
        mock_config_file.exists.return_value = False
        mock_appdata.__truediv__ = MagicMock(return_value=mock_config_file)

        result = enforce_bnet_config(dry_run=False)

        mock_appdata.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        assert result is False
