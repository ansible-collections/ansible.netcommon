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

import sys
from unittest.mock import MagicMock, PropertyMock, patch

import pytest
from ansible.playbook.play_context import PlayContext

pytest.importorskip("ncclient")


builtin_import = __import__
mock_ncclient = MagicMock(name="ncclient")
mock_ncclient.__version__ = "0.6.10"


def import_mock(name, *args):
    if name.startswith("ncclient"):
        return mock_ncclient
    return builtin_import(name, *args)


PY3 = sys.version_info[0] == 3
if PY3:
    with patch("builtins.__import__", side_effect=import_mock):
        from ansible.plugins.loader import connection_loader
        from ansible_collections.ansible.netcommon.plugins.connection import (
            netconf,
        )
else:
    with patch("__builtin__.__import__", side_effect=import_mock):
        from ansible.plugins.loader import connection_loader
        from ansible_collections.ansible.netcommon.plugins.connection import (
            netconf,
        )


def test_netconf_init():
    pc = PlayContext()
    conn = connection_loader.get("netconf", pc, "/dev/null")

    assert conn._network_os == "auto"
    assert conn._manager is None
    assert conn._connected is False


@patch(
    "ansible_collections.ansible.netcommon.plugins.connection.netconf.netconf_loader"
)
def test_netconf__connect(mock_netconf_loader):
    pc = PlayContext()
    conn = connection_loader.get("ansible.netcommon.netconf", pc, "/dev/null")

    mock_manager = MagicMock()
    mock_manager.session_id = "123456789"
    netconf.manager.connect = MagicMock(return_value=mock_manager)

    rc, out, err = conn._connect()

    assert rc == 0
    assert out == b"123456789"
    assert err == b""
    assert conn._connected is True


@pytest.mark.parametrize(
    "proxy_command,proxy_response",
    [
        ('ssh -W "%h:%p" bastion', ["ssh", "-W", "example.com:22", "bastion"]),
        (None, None),
    ],
)
def test_netconf_proxy_command(proxy_command, proxy_response):
    pc = PlayContext()
    pc.remote_addr = "example.com"
    conn = connection_loader.get("ansible.netcommon.netconf", pc, "/dev/null")
    conn.set_option("proxy_command", proxy_command)

    response = conn._get_proxy_command()
    if proxy_command is None:
        assert response is proxy_response
    else:
        assert response.cmd == proxy_response


def test_netconf_exec_command():
    pc = PlayContext()
    conn = connection_loader.get("ansible.netcommon.netconf", pc, "/dev/null")

    conn._connected = True

    mock_manager = MagicMock(name="self._manager")
    conn._manager = mock_manager

    mock_reply = MagicMock(name="reply")
    type(mock_reply).data_xml = PropertyMock(return_value="<test/>")
    mock_manager.rpc.return_value = mock_reply

    out = conn.exec_command("<test/>")

    assert out == "<test/>"


def test_netconf_exec_command_invalid_request():
    pc = PlayContext()
    conn = connection_loader.get("ansible.netcommon.netconf", pc, "/dev/null")

    conn._connected = True

    mock_manager = MagicMock(name="self._manager")
    conn._manager = mock_manager

    netconf.to_ele.return_value = None

    out = conn.exec_command("test string")

    assert out == "unable to parse request"


def test_netconf_close():
    pc = PlayContext()
    conn = connection_loader.get("ansible.netcommon.netconf", pc, "/dev/null")

    conn._manager = MagicMock()
    conn._connected = True

    conn.close()

    assert conn._connected is False
    assert conn._manager.close_session.called is True
