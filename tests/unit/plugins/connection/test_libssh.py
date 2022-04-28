# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from ansible.module_utils._text import to_bytes
from ansible.errors import (
    AnsibleError,
    AnsibleFileNotFound,
    AnsibleConnectionFailure,
)
from ansible.playbook.play_context import PlayContext
from ansible.plugins.loader import connection_loader
import unittest
from unittest.mock import (
    patch,
    MagicMock,
)

from ansible_collections.ansible.netcommon.plugins.connection import libssh

pylibsshext = pytest.importorskip("pylibsshext")


def test_libssh_connect(monkeypatch):
    """Test the libssh connection plugin.

    :param monkeypatch: pytest fixture
    """
    pc = PlayContext()
    pc.remote_addr = "localhost"
    pc.password = "test"
    pc.port = 8080
    pc.timeout = 60
    pc.remote_user = "user1"

    conn = connection_loader.get("ansible.netcommon.libssh", pc, "/dev/null")
    conn.set_options(
        direct={
            "host_key_checking": False,
        }
    )

    all_args = {"call_args": {}, "call_kwargs": {}}

    class Session(libssh.Session):
        """A session object used to patch libssh.Session"""

        def connect(self, *args, **kwargs):
            """Stores the arguments and keyword arguments for later use.

            :param args: Positional arguments
            :param kwargs: Keyword arguments
            :raises AnsibleConnectionFailure: Always
            """
            all_args["call_args"] = args
            all_args["call_kwargs"] = kwargs
            raise AnsibleConnectionFailure

    monkeypatch.setattr(libssh, "Session", Session)

    with pytest.raises(AnsibleConnectionFailure):
        conn._connect()

    assert all_args["call_kwargs"] == {
        "host": "localhost",
        "host_key_checking": False,
        "look_for_keys": True,
        "password": "test",
        "port": 8080,
        "timeout": 60,
        "user": "user1",
        "private_key": None,
    }


class TestConnectionClass(unittest.TestCase):
    def test_libssh_close(self):
        pc = PlayContext()
        conn = connection_loader.get(
            "ansible.netcommon.libssh", pc, "/dev/null"
        )
        conn.ssh = MagicMock()
        conn.sftp = MagicMock()
        conn.chan = MagicMock()

        conn.close()

        conn.sftp.close.assert_called_with()
        conn.chan.close.assert_called_with()
        conn.sftp.close.assert_called_with()

    @patch("ansible.plugins.connection.ConnectionBase.exec_command")
    def test_libssh_exec_command(self, mocked_super):
        pc = PlayContext()
        conn = connection_loader.get(
            "ansible.netcommon.libssh", pc, "/dev/null"
        )
        with self.assertRaises(AnsibleError):
            conn.exec_command(cmd="ls", in_data=True)

        mock_chan = MagicMock()
        mock_chan.request_shell = MagicMock()
        mock_chan.exec_command = MagicMock()
        mock_chan.exec_command.return_value = MagicMock(
            returncode=0, stdout="echo hello", stderr=""
        )

        attr = {"new_channel.return_value": mock_chan}
        mock_ssh = MagicMock(**attr)
        conn.ssh = mock_ssh

        rc, out, err = conn.exec_command(cmd="echo hello")

        self.assertEqual((rc, out, err), (0, "echo hello", ""))

    @patch("ansible.plugins.connection.ConnectionBase.put_file")
    def test_libssh_put_file_not_exist(self, mocked_super):
        pc = PlayContext()
        conn = connection_loader.get(
            "ansible.netcommon.libssh", pc, "/dev/null"
        )
        with self.assertRaises(AnsibleFileNotFound):
            conn.put_file(in_path="", out_path="")

    @patch("os.path.exists")
    @patch("ansible.plugins.connection.ConnectionBase.put_file")
    def test_libssh_put_file(self, mocked_super, mock_exists):
        pc = PlayContext()
        conn = connection_loader.get(
            "ansible.netcommon.libssh", pc, "/dev/null"
        )

        mock_sftp = MagicMock()
        attr = {"sftp.return_value": mock_sftp}
        mock_ssh = MagicMock(**attr)
        conn.ssh = mock_ssh

        file_path = "test_libssh.py"
        conn.put_file(in_path=file_path, out_path=file_path)
        mock_sftp.put.assert_called_with(
            to_bytes(file_path), to_bytes(file_path)
        )


def test_libssh_fetch_file(monkeypatch):
    pc = PlayContext()
    pc.remote_addr = "localhost"
    conn = connection_loader.get("ansible.netcommon.libssh", pc, "/dev/null")

    class Session(libssh.Session):
        """A session object used to patch libssh.Session"""

        def connect(self, *args, **kwargs):
            """Stores the arguments and keyword arguments for later use.

            :param args: Positional arguments
            :param kwargs: Keyword arguments
            :return: True indicating a successful connection
            """
            return True

    monkeypatch.setattr(libssh, "Session", Session)

    all_args = {"call_args": {}, "call_kwargs": {}}

    def fetch_file(*args, **kwargs):
        """Stores the arguments and keyword arguments for later use.

        :param args: Positional arguments
        :param kwargs: Keyword arguments
        :raises AnsibleFileNotFound: Always
        """
        all_args["call_args"] = args
        all_args["call_kwargs"] = kwargs
        raise AnsibleFileNotFound

    file_path = "test_libssh.py"
    monkeypatch.setattr(conn, "fetch_file", fetch_file)

    with pytest.raises(AnsibleFileNotFound):
        conn.fetch_file(in_path=file_path, out_path=file_path)

    assert all_args["call_kwargs"] == {
        "in_path": file_path,
        "out_path": file_path,
    }
