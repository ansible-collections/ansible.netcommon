# (c) 2025 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import MagicMock

import pytest

from ansible.errors import AnsibleError
from ansible.module_utils.connection import ConnectionError

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

    result = ActionModule._handle_existing_file(
        action, conn, str(src), "/r/x", "sftp", 5
    )
    assert result is True
