"""Tests for CLI module."""
from unittest.mock import MagicMock, patch

from bnet_sanitizer.cli import run


class TestCLI:
    """Tests for CLI functions."""

    @patch("bnet_sanitizer.cli.terminate_zombies")
    @patch("bnet_sanitizer.cli.enforce_bnet_config")
    @patch("bnet_sanitizer.cli.clear_shader_caches")
    @patch("bnet_sanitizer.cli.console.print")
    def test_run_all_tasks(
        self,
        mock_print: MagicMock,
        mock_clear_shaders: MagicMock,
        mock_enforce_config: MagicMock,
        mock_terminate: MagicMock,
    ) -> None:
        """Test run command executes all tasks."""
        mock_terminate.return_value = 1
        mock_enforce_config.return_value = True

        run(purge_shaders=True, dry_run=False)

        mock_terminate.assert_called_once_with(dry_run=False)
        mock_enforce_config.assert_called_once_with(dry_run=False)
        mock_clear_shaders.assert_called_once_with(dry_run=False)

    @patch("bnet_sanitizer.cli.terminate_zombies")
    @patch("bnet_sanitizer.cli.enforce_bnet_config")
    @patch("bnet_sanitizer.cli.clear_shader_caches")
    @patch("bnet_sanitizer.cli.console.print")
    def test_run_without_purge_shaders(
        self,
        mock_print: MagicMock,
        mock_clear_shaders: MagicMock,
        mock_enforce_config: MagicMock,
        mock_terminate: MagicMock,
    ) -> None:
        """Test run command without purge shaders flag."""
        mock_terminate.return_value = 0
        mock_enforce_config.return_value = True

        run(purge_shaders=False, dry_run=False)

        mock_terminate.assert_called_once_with(dry_run=False)
        mock_enforce_config.assert_called_once_with(dry_run=False)
        mock_clear_shaders.assert_not_called()

    @patch("bnet_sanitizer.cli.terminate_zombies")
    @patch("bnet_sanitizer.cli.enforce_bnet_config")
    @patch("bnet_sanitizer.cli.clear_shader_caches")
    @patch("bnet_sanitizer.cli.console.print")
    def test_run_dry_run_mode(
        self,
        mock_print: MagicMock,
        mock_clear_shaders: MagicMock,
        mock_enforce_config: MagicMock,
        mock_terminate: MagicMock,
    ) -> None:
        """Test run command with dry run flag."""
        mock_terminate.return_value = 0
        mock_enforce_config.return_value = True

        run(purge_shaders=False, dry_run=True)

        mock_terminate.assert_called_once_with(dry_run=True)
        mock_enforce_config.assert_called_once_with(dry_run=True)

    @patch("bnet_sanitizer.cli.terminate_zombies")
    @patch("bnet_sanitizer.cli.enforce_bnet_config")
    @patch("bnet_sanitizer.cli.clear_shader_caches")
    @patch("bnet_sanitizer.cli.console.print")
    def test_run_with_killed_processes(
        self,
        mock_print: MagicMock,
        mock_clear_shaders: MagicMock,
        mock_enforce_config: MagicMock,
        mock_terminate: MagicMock,
    ) -> None:
        """Test run command when processes are killed."""
        mock_terminate.return_value = 5
        mock_enforce_config.return_value = True

        run(purge_shaders=False, dry_run=False)

        assert not any("No zombie" in str(call) for call in mock_print.call_args_list)

    @patch("bnet_sanitizer.cli.terminate_zombies")
    @patch("bnet_sanitizer.cli.enforce_bnet_config")
    @patch("bnet_sanitizer.cli.clear_shader_caches")
    @patch("bnet_sanitizer.cli.console.print")
    def test_run_no_zombie_processes(
        self,
        mock_print: MagicMock,
        mock_clear_shaders: MagicMock,
        mock_enforce_config: MagicMock,
        mock_terminate: MagicMock,
    ) -> None:
        """Test run command when no zombie processes found."""
        mock_terminate.return_value = 0
        mock_enforce_config.return_value = True

        run(purge_shaders=False, dry_run=False)

        assert any("No zombie" in str(call) for call in mock_print.call_args_list)

    @patch("bnet_sanitizer.cli.terminate_zombies")
    @patch("bnet_sanitizer.cli.enforce_bnet_config")
    @patch("bnet_sanitizer.cli.clear_shader_caches")
    @patch("bnet_sanitizer.cli.console.print")
    def test_run_dry_run_and_purge_shaders(
        self,
        mock_print: MagicMock,
        mock_clear_shaders: MagicMock,
        mock_enforce_config: MagicMock,
        mock_terminate: MagicMock,
    ) -> None:
        """Test run command with both dry run and purge shaders flags."""
        mock_terminate.return_value = 0
        mock_enforce_config.return_value = True

        run(purge_shaders=True, dry_run=True)

        mock_clear_shaders.assert_called_once_with(dry_run=True)
