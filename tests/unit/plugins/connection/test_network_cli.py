#
# (c) 2016 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible_collections.ansible.netcommon.tests.unit.compat.mock import (
    patch,
    MagicMock,
)
from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils._text import to_text
from ansible.playbook.play_context import PlayContext
from ansible.plugins.loader import connection_loader
import pytest


SSH_TYPES = [
    ("paramiko", "ansible.plugins.connection.paramiko_ssh.Connection"),
    (
        "libssh",
        "ansible_collections.ansible.netcommon.plugins.connection.libssh.Connection",
    ),
]


@pytest.fixture(name="conn")
def plugin_fixture():
    pc = PlayContext()
    pc.network_os = "ios"
    conn = connection_loader.get(
        "ansible.netcommon.network_cli", pc, "/dev/null"
    )
    return conn


@pytest.mark.parametrize("network_os", [None, "invalid"])
def test_network_cli_invalid_os(network_os):
    pc = PlayContext()
    pc.network_os = network_os

    with pytest.raises(AnsibleConnectionFailure):
        connection_loader.get("ansible.netcommon.network_cli", pc, "/dev/null")


@pytest.mark.parametrize("password", ["password", None])
@pytest.mark.parametrize("private_key_file", ["/path/to/key/file", None])
@pytest.mark.parametrize("ssh_type", ["paramiko", "libssh"])
def test_look_for_keys(conn, password, private_key_file, ssh_type):
    conn.set_options(
        direct={
            "ssh_type": ssh_type,
            "password": password,
            "private_key_file": private_key_file,
        }
    )

    # We automagically set look_for_keys based on the state of password and
    # private_key_file. Make sure that setting is preserved
    if private_key_file:
        assert conn.ssh_type_conn.get_option("look_for_keys") is True
    elif password:
        assert conn.ssh_type_conn.get_option("look_for_keys") is False
    else:
        assert conn.ssh_type_conn.get_option("look_for_keys") is True


@pytest.mark.parametrize("ssh_type", ["paramiko", "libssh"])
def test_options_pass_through(conn, ssh_type):
    conn.set_options(direct={"ssh_type": ssh_type, "host_key_checking": False})
    # Options not found in underlying connection plugin are not set
    assert conn.get_option("ssh_type") == ssh_type
    with pytest.raises(KeyError):
        conn.ssh_type_conn.get_option("ssh_type")
    # Options which are shared do pass through
    # At some point these options should be able to be dropped from network_cli
    assert conn.get_option("host_key_checking") is False
    assert conn.ssh_type_conn.get_option("host_key_checking") is False


@pytest.mark.parametrize("ssh_type,ssh_implementation", SSH_TYPES)
@pytest.mark.parametrize(
    "become_method,become_pass", [("enable", "password"), (None, None)]
)
def test_network_cli__connect(
    conn, ssh_type, ssh_implementation, become_method, become_pass
):
    conn.ssh = MagicMock()
    conn.receive = MagicMock()
    conn._terminal = MagicMock()

    if become_method:
        conn._play_context.become = True
        conn._play_context.become_method = become_method
        conn._play_context.become_pass = become_pass

    conn.set_options(direct={"ssh_type": ssh_type})

    with patch("%s._connect" % ssh_implementation) as mocked_super:
        conn._connect()
        assert mocked_super.called is True

    assert conn._terminal.on_open_shell.called is True
    if become_method:
        conn._terminal.on_become.assert_called_with(passwd=become_pass)
    else:
        assert conn._terminal.on_become.called is False


@pytest.mark.parametrize("ssh_type,ssh_implementation", SSH_TYPES)
@pytest.mark.parametrize(
    "command", ["command", json.dumps({"command": "command"})]
)
def test_network_cli_exec_command(conn, ssh_type, ssh_implementation, command):
    conn._ssh_type = ssh_type

    mock_send = MagicMock(return_value=b"command response")
    conn.send = mock_send
    conn._ssh_shell = MagicMock()

    with patch("%s._connect" % ssh_implementation):
        out = conn.exec_command(command)

    mock_send.assert_called_with(command=b"command")
    assert out == b"command response"


@pytest.mark.parametrize(
    "response",
    [
        b"device#command\ncommand response\n\ndevice#",
        pytest.param(
            b"ERROR: error message device#",
            marks=pytest.mark.xfail(raises=AnsibleConnectionFailure),
        ),
    ],
)
def test_network_cli_send(conn, response):
    conn.set_options(
        direct={
            "terminal_stderr_re": [{"pattern": "^ERROR"}],
            "terminal_stdout_re": [{"pattern": "device#"}],
        }
    )
    mock__shell = MagicMock()

    conn._terminal = MagicMock()
    conn._ssh_shell = mock__shell
    conn._connected = True

    mock__shell.recv.side_effect = [response, None]
    conn.send(b"command")

    mock__shell.sendall.assert_called_with(b"command\r")
    assert to_text(conn._command_response) == "command response"


@pytest.mark.parametrize("ssh_type,ssh_implementation", SSH_TYPES)
def test_network_cli_close(conn, ssh_type, ssh_implementation):
    conn._ssh_type = ssh_type

    terminal = MagicMock(supports_multiplexing=False)
    conn._terminal = terminal
    conn._ssh_shell = MagicMock()
    conn._ssh_type_conn = MagicMock()
    conn._connected = True
    with patch("%s.close" % ssh_implementation):
        conn.close()

    assert conn._connected is False
    assert terminal.on_close_shell.called is True
    assert conn._ssh_shell is None
    assert conn._ssh_type_conn is None
