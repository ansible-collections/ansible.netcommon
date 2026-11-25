# (c) 2025 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import os

from unittest.mock import MagicMock

import pytest

from ansible.module_utils.connection import ConnectionError

from ansible_collections.ansible.netcommon.plugins.action.net_get import ActionModule


@pytest.fixture(name="net_get_action")
def net_get_action_fixture(tmp_path):
    action = object.__new__(ActionModule)
    action._loader = MagicMock()
    action._loader.get_basedir.return_value = str(tmp_path)
    return action, tmp_path


def test_handle_existing_file_same_checksum(net_get_action):
    """Idempotent path: remote file matches local -> False."""
    action, tmp_path = net_get_action
    dest = tmp_path / "running.cfg"
    dest.write_text("identical-bytes\n")

    conn = MagicMock()

    def _get_file(source=None, destination=None, **kwargs):
        with open(destination, "w") as fp:
            fp.write("identical-bytes\n")

    conn.get_file.side_effect = _get_file

    result = ActionModule._handle_existing_file(
        action, conn, "/remote/running.cfg", str(dest), "sftp", 99
    )
    assert result is False
    conn.get_file.assert_called_once()


def test_handle_existing_file_missing_local_returns_true(net_get_action):
    """Local dest missing -> True (must download)."""
    action, tmp_path = net_get_action
    dest = tmp_path / "missing.cfg"

    conn = MagicMock()

    result = ActionModule._handle_existing_file(
        action, conn, "/remote/running.cfg", str(dest), "scp", 10
    )
    assert result is True


def test_handle_existing_file_checksum_mismatch_returns_true(net_get_action):
    """Remote file differs from local -> return True (download needed)."""
    action, tmp_path = net_get_action
    dest = tmp_path / "running.cfg"
    dest.write_text("old-content\n", encoding="utf-8")

    conn = MagicMock()

    def _get_file(source=None, destination=None, **kwargs):
        with open(destination, "w", encoding="utf-8") as fp:
            fp.write("new-content\n")

    conn.get_file.side_effect = _get_file
    result = ActionModule._handle_existing_file(
        action, conn, "/remote/running.cfg", str(dest), "sftp", 30
    )
    assert result is True


def test_handle_existing_file_binary_files_same_checksum(net_get_action):
    """Binary files with non-UTF-8 bytes are handled gracefully."""
    action, tmp_path = net_get_action
    binary_data = b"\x88\x89\x8a\x8b"
    dest = tmp_path / "local.bin"
    dest.write_bytes(binary_data)

    conn = MagicMock()

    def _get_file(source=None, destination=None, **kwargs):
        with open(destination, "wb") as fp:
            fp.write(binary_data)

    conn.get_file.side_effect = _get_file
    result = ActionModule._handle_existing_file(
        action, conn, "/remote/binary.bin", str(dest), "sftp", 30
    )
    assert result is False


def test_handle_existing_file_binary_files_different_checksum(net_get_action):
    """Binary files with different content trigger download."""
    action, tmp_path = net_get_action
    dest = tmp_path / "local.bin"
    dest.write_bytes(b"\x77\x78\x79\x7a")

    conn = MagicMock()

    def _get_file(source=None, destination=None, **kwargs):
        with open(destination, "wb") as fp:
            fp.write(b"\x88\x89\x8a\x8b")

    conn.get_file.side_effect = _get_file
    result = ActionModule._handle_existing_file(
        action, conn, "/remote/binary.bin", str(dest), "sftp", 30
    )
    assert result is True


def test_handle_existing_file_mixed_text_and_binary_returns_true(net_get_action):
    """Local side is valid UTF-8, remote side is not -> True (download needed)."""
    action, tmp_path = net_get_action
    dest = tmp_path / "local.bin"
    dest.write_bytes(b"plain-ascii\n")

    conn = MagicMock()

    def _get_file(source=None, destination=None, **kwargs):
        with open(destination, "wb") as fp:
            fp.write(b"plain-ascii\n\x88")

    conn.get_file.side_effect = _get_file
    result = ActionModule._handle_existing_file(
        action, conn, "/remote/binary.bin", str(dest), "sftp", 30
    )
    assert result is True


def test_handle_existing_file_crlf_difference_is_a_change(net_get_action):
    """Line endings are compared byte for byte, regardless of file encoding."""
    action, tmp_path = net_get_action
    dest = tmp_path / "running.cfg"
    dest.write_bytes(b"line1\nline2\n")

    conn = MagicMock()

    def _get_file(source=None, destination=None, **kwargs):
        with open(destination, "wb") as fp:
            fp.write(b"line1\r\nline2\r\n")

    conn.get_file.side_effect = _get_file
    result = ActionModule._handle_existing_file(
        action, conn, "/remote/running.cfg", str(dest), "sftp", 30
    )
    assert result is True


def test_handle_existing_file_removes_tmp_file(net_get_action):
    """The uuid-named temp copy is cleaned up once the comparison is done."""
    action, tmp_path = net_get_action
    dest = tmp_path / "running.cfg"
    dest.write_bytes(b"\x88\x89\x8a\x8b")
    before = set(os.listdir(str(tmp_path)))

    conn = MagicMock()

    def _get_file(source=None, destination=None, **kwargs):
        with open(destination, "wb") as fp:
            fp.write(b"\x88\x89\x8a\x8b")

    conn.get_file.side_effect = _get_file
    result = ActionModule._handle_existing_file(
        action, conn, "/remote/running.cfg", str(dest), "sftp", 30
    )
    assert result is False
    assert set(os.listdir(str(tmp_path))) == before


@pytest.mark.skipif(
    hasattr(os, "geteuid") and os.geteuid() == 0,
    reason="root bypasses file permission checks",
)
def test_handle_existing_file_removes_tmp_file_on_read_error(net_get_action):
    """A read failure propagates but still cleans up the uuid-named temp copy."""
    action, tmp_path = net_get_action
    dest = tmp_path / "unreadable.cfg"
    dest.write_bytes(b"\x88\x89")
    dest.chmod(0o000)
    before = set(os.listdir(str(tmp_path)))

    conn = MagicMock()

    def _get_file(source=None, destination=None, **kwargs):
        with open(destination, "wb") as fp:
            fp.write(b"\x88\x89")

    conn.get_file.side_effect = _get_file
    try:
        with pytest.raises((IOError, OSError)):
            ActionModule._handle_existing_file(
                action, conn, "/remote/running.cfg", str(dest), "sftp", 30
            )
        assert set(os.listdir(str(tmp_path))) == before
    finally:
        dest.chmod(0o644)


def test_handle_existing_file_remote_missing_returns_true(net_get_action):
    """Remote file missing -> get_file fails with expected message -> True."""
    action, tmp_path = net_get_action
    dest = tmp_path / "local.txt"
    dest.write_text("existing")

    conn = MagicMock()
    conn.get_file.side_effect = ConnectionError("No such file or directory")

    result = ActionModule._handle_existing_file(
        action, conn, "/remote/missing", str(dest), "scp", 10
    )
    assert result is True
