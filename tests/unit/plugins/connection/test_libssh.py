# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import logging
import os

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


def test_libssh_resolve_log_path_new_file_writable_parent(conn, monkeypatch, tmp_path):
    """Log file does not exist yet; parent directory is writable -> return path."""
    logf = tmp_path / "new" / "ansible.log"
    logf.parent.mkdir(parents=True)
    monkeypatch.setattr(libssh.C, "DEFAULT_LOG_PATH", str(logf.resolve()))
    assert conn._pylibssh_resolve_log_path("h") == str(logf.resolve())


def test_libssh_resolve_log_path_skip_not_writable(conn, monkeypatch, tmp_path):
    logf = tmp_path / "ansible.log"
    logf.write_text("")
    abs_path = str(logf.resolve())
    monkeypatch.setattr(libssh.C, "DEFAULT_LOG_PATH", abs_path)
    real_access = os.access

    def _access(path, mode):
        if os.fspath(path) == abs_path and mode == os.W_OK:
            return False
        return real_access(path, mode)

    monkeypatch.setattr(os, "access", _access)
    assert conn._pylibssh_resolve_log_path("h") is None


def test_libssh_resolve_log_path_skip_parent_not_writable(conn, monkeypatch, tmp_path):
    logf = tmp_path / "subdir" / "ansible.log"
    logf.parent.mkdir(parents=True)
    abs_path = str(logf.resolve())
    monkeypatch.setattr(libssh.C, "DEFAULT_LOG_PATH", abs_path)
    real_access = os.access

    def _access(path, mode):
        p = os.fspath(path)
        if p == str(logf.parent.resolve()) and mode == os.W_OK:
            return False
        return real_access(path, mode)

    monkeypatch.setattr(os, "access", _access)
    assert conn._pylibssh_resolve_log_path("h") is None


def test_libssh_resolve_log_path_skip_parent_not_dir(conn, monkeypatch, tmp_path):
    """Parent path component exists but is a file, not a directory."""
    blocker = tmp_path / "notadir"
    blocker.write_text("x", encoding="utf-8")
    nested = tmp_path / "notadir" / "ansible.log"
    monkeypatch.setattr(libssh.C, "DEFAULT_LOG_PATH", str(nested.resolve()))
    assert conn._pylibssh_resolve_log_path("h") is None


def test_libssh_log_handler_updates_level_when_handler_exists(conn, monkeypatch, tmp_path):
    logf = tmp_path / "ansible.log"
    logf.touch()
    abs_path = str(logf.resolve())
    monkeypatch.setattr(libssh.C, "DEFAULT_LOG_PATH", abs_path)
    pylog = logging.getLogger("ansible-pylibssh")
    pylog.handlers = [h for h in pylog.handlers if getattr(h, "baseFilename", None) != abs_path]

    monkeypatch.setattr(libssh.display, "verbosity", 4)
    conn._ensure_pylibssh_log_handler(host="h")
    monkeypatch.setattr(libssh.display, "verbosity", 0)
    conn._ensure_pylibssh_log_handler(host="h")

    for h in pylog.handlers:
        if getattr(h, "baseFilename", None) == abs_path:
            assert h.level == logging.WARNING
            break
    else:
        raise AssertionError("handler not found")


@patch("os.path.exists")
@patch("ansible.plugins.connection.ConnectionBase.put_file")
def test_libssh_put_file_scp(mocked_super, mock_exists, conn, monkeypatch):
    libssh.SSH_CONNECTION_CACHE.clear()
    libssh.SFTP_CONNECTION_CACHE.clear()
    conn._play_context.remote_addr = "put-file-scp-host"
    conn._play_context.remote_user = "u-scp"
    conn.set_options(
        direct={
            "remote_addr": "put-file-scp-host",
            "remote_user": "u-scp",
            "host_key_checking": False,
        }
    )
    mock_scp = MagicMock()
    mock_ssh = MagicMock()
    mock_ssh.scp.return_value = mock_scp
    monkeypatch.setattr(libssh, "Session", lambda: mock_ssh)
    mock_exists.return_value = True

    conn.put_file(in_path="/local/x", out_path="/remote/x", proto="scp")
    mock_scp.put.assert_called_once_with("/local/x", "/remote/x")


@patch("os.path.exists")
@patch("ansible.plugins.connection.ConnectionBase.put_file")
def test_libssh_put_file_unknown_proto(mocked_super, mock_exists, conn, monkeypatch):
    libssh.SSH_CONNECTION_CACHE.clear()
    libssh.SFTP_CONNECTION_CACHE.clear()
    conn._play_context.remote_addr = "put-unknown-proto-host"
    conn._play_context.remote_user = "u-up"
    conn.set_options(
        direct={
            "remote_addr": "put-unknown-proto-host",
            "remote_user": "u-up",
            "host_key_checking": False,
        }
    )
    monkeypatch.setattr(libssh, "Session", MagicMock)
    mock_exists.return_value = True
    with pytest.raises(AnsibleError, match="Don't know how to transfer"):
        conn.put_file("/a", "/b", proto="bogus")


@patch("os.path.exists")
@patch("ansible.plugins.connection.ConnectionBase.put_file")
def test_libssh_put_file_sftp_put_ioerror(mocked_super, mock_exists, conn, monkeypatch):
    libssh.SSH_CONNECTION_CACHE.clear()
    libssh.SFTP_CONNECTION_CACHE.clear()
    mock_sftp = MagicMock()
    mock_sftp.put.side_effect = OSError("disk full")
    mock_ssh = MagicMock()
    mock_ssh.sftp.return_value = mock_sftp
    monkeypatch.setattr(libssh, "Session", lambda: mock_ssh)
    mock_exists.return_value = True
    conn._play_context.remote_addr = "sftp-put-ioerror-host"
    conn._play_context.remote_user = "u-ioe"
    conn.set_options(
        direct={
            "remote_addr": "sftp-put-ioerror-host",
            "remote_user": "u-ioe",
            "host_key_checking": False,
        }
    )
    with pytest.raises(AnsibleError, match="failed to transfer file to"):
        conn.put_file("/a", "/b", proto="sftp")


@patch("ansible.plugins.connection.ConnectionBase.fetch_file")
def test_libssh_fetch_file_sftp_get_ioerror(mocked_super, conn, monkeypatch):
    mock_sftp = MagicMock()
    mock_sftp.get.side_effect = OSError("read fail")
    conn.set_options(
        direct={
            "remote_addr": "localhost",
            "remote_user": "u1",
            "host_key_checking": False,
        }
    )
    conn._connect_sftp = MagicMock(return_value=mock_sftp)
    with pytest.raises(AnsibleError, match="failed to transfer file from"):
        conn.fetch_file("/r", "/l", proto="sftp")


@patch("ansible.plugins.connection.ConnectionBase.fetch_file")
def test_libssh_fetch_file_scp_success(mocked_super, conn, monkeypatch):
    mock_scp = MagicMock()
    mock_ssh = MagicMock()
    mock_ssh.scp.return_value = mock_scp
    conn.ssh = mock_ssh
    conn.fetch_file("/remote/f", "/local/f", proto="scp")
    mock_scp.get.assert_called_once_with("/remote/f", "/local/f")


def test_libssh_invalidate_ssh_close_exception_swallowed(conn):
    mock_ssh = MagicMock()
    mock_ssh.close.side_effect = RuntimeError("close failed")
    conn.ssh = mock_ssh
    conn.set_options(
        direct={
            "remote_addr": "h1",
            "remote_user": "u1",
            "host_key_checking": False,
        }
    )
    conn._invalidate_ssh_session_after_scp_get_failure()
    assert conn.ssh is None
