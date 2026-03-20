# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import logging

from unittest.mock import MagicMock, patch

import pytest

from ansible.errors import AnsibleError, AnsibleFileNotFound
from ansible.module_utils._text import to_bytes
from ansible.playbook.play_context import PlayContext
from ansible.plugins.loader import connection_loader

from ansible_collections.ansible.netcommon.plugins.connection import libssh


pylibsshext = pytest.importorskip("pylibsshext")


@pytest.fixture(name="conn")
def plugin_fixture():
    pc = PlayContext()
    pc.port = 8080
    pc.timeout = 60

    conn = connection_loader.get("ansible.netcommon.libssh", pc, "/dev/null")
    return conn


def test_libssh_connect(conn, monkeypatch):
    """Test the libssh connection plugin.

    :param monkeypatch: pytest fixture
    """
    conn.set_options(
        direct={
            "remote_addr": "localhost",
            "remote_user": "user1",
            "password": "test",
            "host_key_checking": False,
        }
    )

    mock_session = MagicMock()
    monkeypatch.setattr(libssh, "Session", mock_session)
    mock_ssh = MagicMock()
    mock_session.return_value = mock_ssh
    conn._connect()
    mock_ssh.connect.assert_called_with(
        host="localhost",
        host_key_checking=False,
        look_for_keys=True,
        password="test",
        password_prompt=None,
        private_key_password=None,
        port=8080,
        timeout=60,
        user="user1",
        private_key=None,
    )


def test_libssh_close(conn):
    conn.ssh = MagicMock()
    conn.sftp = MagicMock()
    conn.chan = MagicMock()

    conn.close()

    conn.sftp.close.assert_called_with()
    conn.chan.close.assert_called_with()
    conn.ssh.close.assert_called_with()


@patch("ansible.plugins.connection.ConnectionBase.exec_command")
def test_libssh_exec_command(mocked_super, conn):
    with pytest.raises(AnsibleError):
        conn.exec_command(cmd="ls", in_data=True)

    mock_chan = MagicMock()
    mock_chan.request_shell = MagicMock()
    mock_chan.exec_command = MagicMock()
    mock_chan.exec_command.return_value = MagicMock(returncode=0, stdout="echo hello", stderr="")

    attr = {"new_channel.return_value": mock_chan}
    mock_ssh = MagicMock(**attr)
    conn.ssh = mock_ssh

    rc, out, err = conn.exec_command(cmd="echo hello")

    assert (rc, out, err) == (0, "echo hello", "")


@patch("ansible.plugins.connection.ConnectionBase.put_file")
def test_libssh_put_file_not_exist(mocked_super, conn):
    with pytest.raises(AnsibleFileNotFound):
        conn.put_file(in_path="", out_path="")


@patch("os.path.exists")
@patch("ansible.plugins.connection.ConnectionBase.put_file")
def test_libssh_put_file(mocked_super, mock_exists, conn, monkeypatch):
    conn.set_options(
        direct={
            "remote_addr": "localhost",
            "remote_user": "user1",
            "host_key_checking": False,
        }
    )
    mock_sftp = MagicMock()
    attr = {"sftp.return_value": mock_sftp}
    mock_ssh = MagicMock(**attr)
    monkeypatch.setattr(libssh, "Session", lambda: mock_ssh)

    file_path = "test_libssh.py"
    conn.put_file(in_path=file_path, out_path=file_path)
    mock_sftp.put.assert_called_with(to_bytes(file_path), to_bytes(file_path))


@patch("ansible.plugins.connection.ConnectionBase.fetch_file")
def test_libssh_fetch_file(mocked_super, conn, monkeypatch):
    mock_session = MagicMock()
    monkeypatch.setattr(libssh, "Session", mock_session)
    mock_ssh = MagicMock()
    mock_session.return_value = mock_ssh

    file_path = "test_libssh.py"
    conn.fetch_file(in_path=file_path, out_path=file_path)

    conn.sftp.get.assert_called_with(
        to_bytes(file_path),
        to_bytes(file_path),
    )


@pytest.mark.parametrize(
    "verbosity,expected",
    [(0, logging.WARNING), (1, logging.INFO), (2, logging.INFO), (4, logging.DEBUG)],
)
def test_libssh_pylibssh_handler_log_level(conn, monkeypatch, verbosity, expected):
    monkeypatch.setattr(libssh.display, "verbosity", verbosity)
    assert conn._pylibssh_handler_log_level() == expected


def test_libssh_resolve_log_path_skips_when_unset(conn, monkeypatch):
    monkeypatch.setattr(libssh.C, "DEFAULT_LOG_PATH", None)
    assert conn._pylibssh_resolve_log_path("h1") is None


def test_libssh_resolve_log_path_skips_relative(conn, monkeypatch):
    monkeypatch.setattr(libssh.C, "DEFAULT_LOG_PATH", "relative.log")
    assert conn._pylibssh_resolve_log_path("h1") is None


def test_libssh_resolve_log_path_expands_writable_file(conn, monkeypatch, tmp_path):
    logf = tmp_path / "ansible.log"
    logf.write_text("")
    monkeypatch.setattr(libssh.C, "DEFAULT_LOG_PATH", str(logf.resolve()))
    assert conn._pylibssh_resolve_log_path("h1") == str(logf.resolve())


def test_libssh_ensure_pylibssh_log_handler_adds_handler(conn, monkeypatch, tmp_path):
    logf = tmp_path / "ansible.log"
    logf.touch()
    abs_path = str(logf.resolve())
    monkeypatch.setattr(libssh.C, "DEFAULT_LOG_PATH", abs_path)
    monkeypatch.setattr(libssh.display, "verbosity", 3)
    pylog = logging.getLogger("ansible-pylibssh")
    pylog.handlers = [h for h in pylog.handlers if getattr(h, "baseFilename", None) != abs_path]

    conn._ensure_pylibssh_log_handler(host="h1")
    assert any(getattr(h, "baseFilename", None) == abs_path for h in pylog.handlers)


@patch("ansible.plugins.connection.ConnectionBase.fetch_file")
def test_libssh_fetch_file_unknown_proto(mocked_super, conn):
    conn.ssh = MagicMock()
    with pytest.raises(AnsibleError, match="Don't know how to transfer"):
        conn.fetch_file("a", "b", proto="bogus")


@patch("ansible.plugins.connection.ConnectionBase.fetch_file")
def test_libssh_fetch_file_sftp_open_fails(mocked_super, conn):
    conn.set_options(
        direct={
            "remote_addr": "localhost",
            "remote_user": "u1",
            "host_key_checking": False,
        }
    )
    conn._connect_sftp = MagicMock(side_effect=RuntimeError("sftp boom"))
    with pytest.raises(AnsibleError, match="failed to open a SFTP connection"):
        conn.fetch_file("r", "l", proto="sftp")


@patch("ansible.plugins.connection.ConnectionBase.fetch_file")
def test_libssh_fetch_file_scp_failure_invalidates_cache(mocked_super, conn, monkeypatch):
    from pylibsshext.errors import LibsshSCPException

    conn.set_options(
        direct={
            "remote_addr": "host-x",
            "remote_user": "user-x",
            "host_key_checking": False,
        }
    )
    libssh.SSH_CONNECTION_CACHE.clear()
    libssh.SFTP_CONNECTION_CACHE.clear()
    cache_key = conn._cache_key()
    mock_ssh = MagicMock()
    mock_scp = MagicMock()
    mock_scp.get.side_effect = LibsshSCPException("not found")
    mock_ssh.scp.return_value = mock_scp
    conn.ssh = mock_ssh
    libssh.SSH_CONNECTION_CACHE[cache_key] = mock_ssh

    with pytest.raises(AnsibleError, match="Error transferring file"):
        conn.fetch_file("/remote/f", "/local/f", proto="scp")

    assert cache_key not in libssh.SSH_CONNECTION_CACHE
    assert conn.ssh is None
    mock_ssh.close.assert_called_once()
