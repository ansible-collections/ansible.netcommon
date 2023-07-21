#
# (c) 2016 Red Hat Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

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


with patch("builtins.__import__", side_effect=import_mock):
    from ansible.plugins.loader import connection_loader

    from ansible_collections.ansible.netcommon.plugins.connection import netconf


def test_netconf_init():
    pc = PlayContext()
    conn = connection_loader.get("netconf", pc, "/dev/null")

    assert conn._network_os == "auto"
    assert conn._manager is None
    assert conn._connected is False


@patch("ansible_collections.ansible.netcommon.plugins.connection.netconf.netconf_loader")
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
