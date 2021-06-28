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

import re
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


@pytest.mark.parametrize("network_os", [None, "invalid"])
def test_network_cli_invalid_os(network_os):
    pc = PlayContext()
    pc.network_os = network_os

    with pytest.raises(AnsibleConnectionFailure):
        connection_loader.get("ansible.netcommon.network_cli", pc, "/dev/null")


@patch(
    "ansible_collections.ansible.netcommon.plugins.connection.network_cli.terminal_loader"
)
@pytest.mark.parametrize("ssh_type,ssh_implementation", SSH_TYPES)
@pytest.mark.parametrize(
    "become,become_method,become_pass",
    [(True, "enable", "password"), (False, None, None)],
)
def test_network_cli__connect(
    mocked_terminal,
    ssh_type,
    ssh_implementation,
    become,
    become_method,
    become_pass,
):
    pc = PlayContext()
    pc.network_os = "ios"

    with patch("%s._connect" % ssh_implementation) as mocked_super:
        conn = connection_loader.get(
            "ansible.netcommon.network_cli", pc, "/dev/null"
        )

        conn.ssh = MagicMock()
        conn.receive = MagicMock()
        conn._terminal = MagicMock()
        conn.set_options(direct={"ssh_type": ssh_type})

        conn._play_context.become = become
        conn._play_context.become_method = become_method
        conn._play_context.become_pass = become_pass

        conn._connect()
        assert mocked_super.called is True

    assert conn._terminal.on_open_shell.called is True
    if become:
        conn._terminal.on_become.assert_called_with(passwd=become_pass)
    else:
        assert conn._terminal.on_become.called is False


@pytest.mark.parametrize("ssh_type,ssh_implementation", SSH_TYPES)
@pytest.mark.parametrize(
    "command", ["command", json.dumps({"command": "command"})]
)
def test_network_cli_exec_command(ssh_type, ssh_implementation, command):
    pc = PlayContext()
    pc.network_os = "ios"
    conn = connection_loader.get(
        "ansible.netcommon.network_cli", pc, "/dev/null"
    )
    conn._ssh_type = ssh_type

    mock_send = MagicMock(return_value=b"command response")
    conn.send = mock_send
    conn._ssh_shell = MagicMock()

    with patch("%s._connect" % ssh_implementation):
        out = conn.exec_command(command)

    mock_send.assert_called_with(command=b"command")
    assert out == b"command response"


@patch(
    "ansible_collections.ansible.netcommon.plugins.connection.network_cli.Connection._get_terminal_std_re"
)
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
def test_network_cli_send(mocked_terminal_re, response):
    pc = PlayContext()
    pc.network_os = "ios"
    pc.remote_addr = "localhost"
    conn = connection_loader.get(
        "ansible.netcommon.network_cli", pc, "/dev/null"
    )
    conn._connected = True

    mock__terminal = MagicMock()
    mocked_terminal_re.side_effect = [
        [re.compile(b"^ERROR")],
        [re.compile(b"device#")],
    ]
    conn._terminal = mock__terminal

    mock__shell = MagicMock()
    conn._ssh_shell = mock__shell

    mock__shell.recv.side_effect = [response, None]
    conn.send(b"command")

    mock__shell.sendall.assert_called_with(b"command\r")
    assert to_text(conn._command_response) == "command response"


@pytest.mark.parametrize("ssh_type,ssh_implementation", SSH_TYPES)
def test_network_cli_close(ssh_type, ssh_implementation):
    pc = PlayContext()
    pc.network_os = "ios"
    conn = connection_loader.get(
        "ansible.netcommon.network_cli", pc, "/dev/null"
    )
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
