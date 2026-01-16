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


def test_netconf_use_libssh_default():
    """Test that use_libssh option defaults to False"""
    pc = PlayContext()
    conn = connection_loader.get("netconf", pc, "/dev/null")

    assert conn.get_option("use_libssh") is False


@patch("ansible_collections.ansible.netcommon.plugins.connection.netconf.netconf_loader")
def test_netconf_connect_with_libssh_enabled(mock_netconf_loader):
    """Test _connect() with use_libssh=True sets use_libssh parameter"""
    pc = PlayContext()
    pc.remote_addr = "test.example.com"
    pc.remote_user = "testuser"
    pc.password = "testpass"
    pc.port = 830

    conn = connection_loader.get("ansible.netcommon.netconf", pc, "/dev/null")

    # Mock get_option after connection is created
    original_get_option = conn.get_option

    def get_option_side_effect(option):
        options = {
            "use_libssh": True,
            "host_key_checking": False,
            "persistent_connect_timeout": 30,
            "look_for_keys": True,
            "netconf_ssh_config": None,
        }
        if option in options:
            return options[option]
        return original_get_option(option)

    conn.get_option = MagicMock(side_effect=get_option_side_effect)

    mock_manager = MagicMock()
    mock_manager.session_id = "test-session-123"
    netconf.manager.connect = MagicMock(return_value=mock_manager)

    rc, out, err = conn._connect()

    # Verify connection was successful
    assert rc == 0
    assert out == b"test-session-123"
    assert err == b""
    assert conn._connected is True

    # Verify manager.connect was called with correct parameters
    call_args = netconf.manager.connect.call_args
    assert call_args is not None
    params = call_args[1]  # keyword arguments

    # When use_libssh is True, only use_libssh should be set
    assert params["use_libssh"] is True
    assert "look_for_keys" not in params
    assert "ssh_config" not in params
    assert params["host"] == "test.example.com"
    assert params["username"] == "testuser"
    assert params["password"] == "testpass"
    assert params["port"] == 830


@patch("ansible_collections.ansible.netcommon.plugins.connection.netconf.netconf_loader")
def test_netconf_connect_with_libssh_disabled(mock_netconf_loader):
    """Test _connect() with use_libssh=False sets use_libssh parameter to False"""
    pc = PlayContext()
    pc.remote_addr = "test.example.com"
    pc.remote_user = "testuser"
    pc.password = "testpass"
    pc.port = 830

    conn = connection_loader.get("ansible.netcommon.netconf", pc, "/dev/null")

    # Mock get_option after connection is created
    original_get_option = conn.get_option

    def get_option_side_effect(option):
        options = {
            "use_libssh": False,
            "host_key_checking": False,
            "persistent_connect_timeout": 30,
            "look_for_keys": True,
            "netconf_ssh_config": None,
        }
        if option in options:
            return options[option]
        return original_get_option(option)

    conn.get_option = MagicMock(side_effect=get_option_side_effect)

    mock_manager = MagicMock()
    mock_manager.session_id = "test-session-456"
    netconf.manager.connect = MagicMock(return_value=mock_manager)

    rc, out, err = conn._connect()

    # Verify connection was successful
    assert rc == 0
    assert out == b"test-session-456"
    assert err == b""
    assert conn._connected is True

    # Verify manager.connect was called with correct parameters
    call_args = netconf.manager.connect.call_args
    assert call_args is not None
    params = call_args[1]  # keyword arguments

    # When use_libssh is False, look_for_keys and ssh_config should be set
    assert "use_libssh" not in params
    assert params["look_for_keys"] is True
    assert params["ssh_config"] is None
    assert params["host"] == "test.example.com"
    assert params["username"] == "testuser"
    assert params["password"] == "testpass"
    assert params["port"] == 830
