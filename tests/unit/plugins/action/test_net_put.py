# (c) 2025 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest

from ansible.errors import AnsibleError
from ansible.module_utils.connection import ConnectionError
from ansible.plugins.action import ActionBase

from ansible_collections.ansible.netcommon.plugins.action.net_put import ActionModule


@pytest.fixture(name="net_put_action")
def net_put_action_fixture(tmp_path):
    action = object.__new__(ActionModule)
    action._loader = MagicMock()
    action._loader.get_basedir.return_value = str(tmp_path)
    return action, tmp_path


def test_handle_existing_file_calls_get_file_same_checksum(net_put_action):
    """Idempotent path: get_file pulls remote copy; matching checksums -> False."""
    action, tmp_path = net_put_action
    src = tmp_path / "local.txt"
    src.write_text("identical-bytes\n")

    conn = MagicMock()

    def _get_file(source=None, destination=None, **kwargs):
        with open(destination, "w") as fp:
            fp.write("identical-bytes\n")

    conn.get_file.side_effect = _get_file

    result = ActionModule._handle_existing_file(
        action, conn, str(src), "/remote/running.cfg", "sftp", 99
    )
    assert result is False
    conn.get_file.assert_called_once()
    call_kw = conn.get_file.call_args[1]
    assert call_kw["source"] == "/remote/running.cfg"
    assert call_kw["proto"] == "sftp"
    assert call_kw["timeout"] == 99


def test_handle_existing_file_missing_remote_returns_true(net_put_action):
    """Remote dest missing -> get_file fails with expected message -> True (must copy)."""
    action, tmp_path = net_put_action
    src = tmp_path / "local.txt"
    src.write_text("new")

    conn = MagicMock()
    conn.get_file.side_effect = AnsibleError("No such file or directory on device")

    result = ActionModule._handle_existing_file(
        action, conn, str(src), "/remote/missing", "scp", 10
    )
    assert result is True


def test_handle_existing_file_connection_error_missing_remote(net_put_action):
    """ConnectionError with File doesn't exist substring -> True."""
    action, tmp_path = net_put_action
    src = tmp_path / "local.txt"
    src.write_text("x")
    conn = MagicMock()
    conn.get_file.side_effect = ConnectionError("File doesn't exist")

    result = ActionModule._handle_existing_file(action, conn, str(src), "/r/x", "sftp", 5)
    assert result is True


def test_net_put_run_iosxr_no_response_from_server_warns(tmp_path):
    """IOSXR copy_file can raise 'No response from server'; emit specific warning."""
    src = tmp_path / "payload.bin"
    src.write_bytes(b"x")

    mock_conn = MagicMock()
    mock_conn.get_option.return_value = 30
    mock_conn.copy_file.side_effect = Exception("No response from server")

    action = object.__new__(ActionModule)
    action._play_context = MagicMock()
    action._play_context.connection = "ansible.netcommon.network_cli"
    action._task = MagicMock()
    action._task.args = {"src": str(src)}
    action._connection = MagicMock()
    action._connection.socket_path = "/fake/socket"
    action._loader = MagicMock()
    action._loader.get_basedir.return_value = str(tmp_path)

    with patch(
        "ansible_collections.ansible.netcommon.plugins.action.net_put.Connection",
        return_value=mock_conn,
    ):
        with patch.object(ActionBase, "run", return_value={}):
            with patch.object(ActionModule, "_handle_existing_file", return_value=True):
                with patch.object(ActionModule, "_get_network_os", return_value="cisco.iosxr"):
                    result = ActionModule.run(action, task_vars={})

    assert "iosxr scp server pre close" in result.get("msg", "")
    mock_conn.copy_file.assert_called_once()


def test_handle_existing_file_checksum_mismatch_returns_true(net_put_action):
    """Remote file differs from local -> return True (upload needed)."""
    action, tmp_path = net_put_action
    src = tmp_path / "local.txt"
    src.write_text("new-content\n", encoding="utf-8")
    conn = MagicMock()

    def _get_file(source=None, destination=None, **kwargs):
        with open(destination, "w", encoding="utf-8") as fp:
            fp.write("old-content\n")

    conn.get_file.side_effect = _get_file
    assert (
        ActionModule._handle_existing_file(action, conn, str(src), "/remote/cfg", "sftp", 30)
        is True
    )
