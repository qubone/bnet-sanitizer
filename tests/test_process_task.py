"""Tests for process task."""
from unittest.mock import MagicMock, patch

import psutil

from bnet_sanitizer.tasks.process_task import terminate_zombies


class TestTerminateZombies:
    """Tests for terminate_zombies function."""

    @patch("bnet_sanitizer.tasks.process_task.kill_wineserver")
    @patch("bnet_sanitizer.tasks.process_task.psutil.process_iter")
    @patch("bnet_sanitizer.tasks.process_task.psutil.Process")
    @patch("bnet_sanitizer.tasks.process_task.console.print")
    def test_terminate_zombies_kill_processes(
        self,
        mock_print: MagicMock,
        mock_process_class: MagicMock,
        mock_process_iter: MagicMock,
        mock_kill_wineserver: MagicMock,
    ) -> None:
        """Test terminating zombie processes."""
        mock_proc1 = MagicMock()
        mock_proc1.info = {"pid": 123, "name": "Battle.Net.exe"}
        mock_proc2 = MagicMock()
        mock_proc2.info = {"pid": 456, "name": "agent.exe"}

        mock_process_iter.return_value = [mock_proc1, mock_proc2]

        mock_killed_proc1 = MagicMock()
        mock_killed_proc2 = MagicMock()
        mock_process_class.side_effect = [mock_killed_proc1, mock_killed_proc2]

        killed = terminate_zombies(dry_run=False)

        assert killed == 2
        assert mock_process_class.call_count == 2
        mock_killed_proc1.kill.assert_called_once()
        mock_killed_proc2.kill.assert_called_once()
        mock_kill_wineserver.assert_called_once()

    @patch("bnet_sanitizer.tasks.process_task.kill_wineserver")
    @patch("bnet_sanitizer.tasks.process_task.psutil.process_iter")
    @patch("bnet_sanitizer.tasks.process_task.console.print")
    def test_terminate_zombies_dry_run(
        self,
        mock_print: MagicMock,
        mock_process_iter: MagicMock,
        mock_kill_wineserver: MagicMock,
    ) -> None:
        """Test dry run mode does not kill processes."""
        mock_proc = MagicMock()
        mock_proc.info = {"pid": 123, "name": "Battle.Net.exe"}
        mock_process_iter.return_value = [mock_proc]

        killed = terminate_zombies(dry_run=True)

        assert killed == 1
        mock_kill_wineserver.assert_not_called()

    @patch("bnet_sanitizer.tasks.process_task.psutil.process_iter")
    @patch("bnet_sanitizer.tasks.process_task.console.print")
    def test_terminate_zombies_no_matching_processes(
        self, mock_print: MagicMock, mock_process_iter: MagicMock
    ) -> None:
        """Test when no matching processes are found."""
        mock_proc = MagicMock()
        mock_proc.info = {"pid": 123, "name": "chrome.exe"}
        mock_process_iter.return_value = [mock_proc]

        killed = terminate_zombies(dry_run=False)

        assert killed == 0

    @patch("bnet_sanitizer.tasks.process_task.psutil.process_iter")
    @patch("bnet_sanitizer.tasks.process_task.console.print")
    def test_terminate_zombies_no_such_process(
        self, mock_print: MagicMock, mock_process_iter: MagicMock
    ) -> None:
        """Test handling of NoSuchProcess exception."""
        mock_proc = MagicMock()
        mock_proc.info = {"pid": 123, "name": "battle.net.exe"}
        mock_process_iter.return_value = [mock_proc]

        with patch("bnet_sanitizer.tasks.process_task.psutil.Process", side_effect=psutil.NoSuchProcess(123)):
            killed = terminate_zombies(dry_run=False)

        # Exception is caught and continue is called, so process is not counted
        assert killed == 0

    @patch("bnet_sanitizer.tasks.process_task.psutil.process_iter")
    @patch("bnet_sanitizer.tasks.process_task.console.print")
    def test_terminate_zombies_access_denied(
        self, mock_print: MagicMock, mock_process_iter: MagicMock
    ) -> None:
        """Test handling of AccessDenied exception."""
        mock_proc = MagicMock()
        mock_proc.info = {"pid": 123, "name": "agent.exe"}
        mock_process_iter.return_value = [mock_proc]

        with patch("bnet_sanitizer.tasks.process_task.psutil.Process", side_effect=psutil.AccessDenied()):
            killed = terminate_zombies(dry_run=False)

        # Exception is caught and continue is called, so process is not counted
        assert killed == 0

    @patch("bnet_sanitizer.tasks.process_task.psutil.process_iter")
    @patch("bnet_sanitizer.tasks.process_task.console.print")
    def test_terminate_zombies_zombie_process(
        self, mock_print: MagicMock, mock_process_iter: MagicMock
    ) -> None:
        """Test handling of ZombieProcess exception."""
        mock_proc = MagicMock()
        mock_proc.info = {"pid": 123, "name": "systemsurvey.exe"}
        mock_process_iter.return_value = [mock_proc]

        with patch("bnet_sanitizer.tasks.process_task.psutil.Process", side_effect=psutil.ZombieProcess(123)):
            killed = terminate_zombies(dry_run=False)

        # Exception is caught and continue is called, so process is not counted
        assert killed == 0

    @patch("bnet_sanitizer.tasks.process_task.psutil.process_iter")
    @patch("bnet_sanitizer.tasks.process_task.console.print")
    def test_terminate_zombies_none_process_name(
        self, mock_print: MagicMock, mock_process_iter: MagicMock
    ) -> None:
        """Test handling of None process name."""
        mock_proc = MagicMock()
        mock_proc.info = {"pid": 123, "name": None}
        mock_process_iter.return_value = [mock_proc]

        killed = terminate_zombies(dry_run=False)

        assert killed == 0

    @patch("bnet_sanitizer.tasks.process_task.kill_wineserver")
    @patch("bnet_sanitizer.tasks.process_task.psutil.process_iter")
    @patch("bnet_sanitizer.tasks.process_task.psutil.Process")
    @patch("bnet_sanitizer.tasks.process_task.console.print")
    def test_terminate_zombies_case_insensitive(
        self,
        mock_print: MagicMock,
        mock_process_class: MagicMock,
        mock_process_iter: MagicMock,
        mock_kill_wineserver: MagicMock,
    ) -> None:
        """Test case-insensitive process name matching."""
        mock_proc = MagicMock()
        mock_proc.info = {"pid": 123, "name": "BATTLE.NET.EXE"}
        mock_process_iter.return_value = [mock_proc]

        mock_killed_proc = MagicMock()
        mock_process_class.return_value = mock_killed_proc

        killed = terminate_zombies(dry_run=False)

        assert killed == 1
        mock_killed_proc.kill.assert_called_once()
