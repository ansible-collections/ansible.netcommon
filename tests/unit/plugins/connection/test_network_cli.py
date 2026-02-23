#
# (c) 2016 Red Hat Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import json
import re

from unittest.mock import MagicMock, patch

import pytest

from ansible.errors import AnsibleConnectionFailure, AnsibleError
from ansible.module_utils._text import to_text
from ansible.playbook.play_context import PlayContext
from ansible.plugins.loader import cache_loader, connection_loader

from ansible_collections.ansible.netcommon.plugins.connection.network_cli import terminal_loader


def _make_terminal_mock(
    ansi_re=None,
    terminal_initial_prompt=None,
    terminal_initial_answer=None,
    terminal_inital_prompt_newline=True,
    terminal_stdout_re=None,
    terminal_stderr_re=None,
):
    """Build a terminal mock with attributes used by network_cli."""
    terminal = MagicMock()
    terminal.ansi_re = ansi_re if ansi_re is not None else []
    terminal.terminal_initial_prompt = terminal_initial_prompt or []
    terminal.terminal_initial_answer = terminal_initial_answer or []
    terminal.terminal_inital_prompt_newline = terminal_inital_prompt_newline
    terminal.terminal_stdout_re = terminal_stdout_re or [re.compile(rb"device#")]
    terminal.terminal_stderr_re = terminal_stderr_re or []
    return terminal


@pytest.fixture(name="conn")
def plugin_fixture(monkeypatch):
    pc = PlayContext()
    pc.network_os = "fakeos"

    def get(*args, **kwargs):
        return MagicMock()

    monkeypatch.setattr(terminal_loader, "get", get)
    conn = connection_loader.get("ansible.netcommon.network_cli", pc, "/dev/null")
    return conn


@pytest.mark.parametrize("network_os", [None, "invalid"])
def test_network_cli_invalid_os(network_os):
    pc = PlayContext()
    pc.network_os = network_os

    with pytest.raises(AnsibleConnectionFailure):
        connection_loader.get("ansible.netcommon.network_cli", pc, "/dev/null")


@pytest.mark.parametrize("look_for_keys", [True, False, None])
@pytest.mark.parametrize("password", ["password", None])
@pytest.mark.parametrize("private_key_file", ["/path/to/key/file", None])
@pytest.mark.parametrize("ssh_type", ["paramiko", "libssh", "auto"])
def test_look_for_keys(conn, look_for_keys, password, private_key_file, ssh_type):
    conn.set_options(
        direct={
            "ssh_type": ssh_type,
            "password": password,
            "private_key_file": private_key_file,
        }
    )
    if look_for_keys is not None:
        conn.set_options(direct={"look_for_keys": look_for_keys})
        assert conn.ssh_type_conn.get_option("look_for_keys") is look_for_keys

    # We automagically set look_for_keys based on the state of password and
    # private_key_file. Make sure that setting is preserved if the option
    # is not set manually.
    elif private_key_file:
        assert conn.ssh_type_conn.get_option("look_for_keys") is True
    elif password:
        assert conn.ssh_type_conn.get_option("look_for_keys") is False
    else:
        assert conn.ssh_type_conn.get_option("look_for_keys") is True


@pytest.mark.parametrize("ssh_type", ["paramiko", "libssh", "auto"])
def test_options_pass_through(conn, ssh_type):
    conn.set_options(
        direct={
            "ssh_type": ssh_type,
            "host_key_checking": False,
            "proxy_command": "do a proxy",
        }
    )
    # Options not found in underlying connection plugin are not set
    assert conn.get_option("ssh_type") == ssh_type
    with pytest.raises(KeyError):
        conn.ssh_type_conn.get_option("ssh_type")
    # Options which are shared do pass through
    # At some point these options should be able to be dropped from network_cli
    assert conn.get_option("host_key_checking") is False
    assert conn.ssh_type_conn.get_option("host_key_checking") is False
    # Options not found in network_cli are not saved there
    with pytest.raises(KeyError):
        conn.get_option("proxy_command")
    assert conn.ssh_type_conn.get_option("proxy_command") == "do a proxy"


@pytest.mark.parametrize("has_libssh", (True, False))
def test_network_cli_ssh_type_auto(conn, has_libssh):
    """Test that ssh_type: auto resolves to the correct option."""
    from ansible_collections.ansible.netcommon.plugins.connection import network_cli

    network_cli.HAS_PYLIBSSH = has_libssh

    conn.set_options(
        direct={
            "ssh_type": "auto",
        }
    )
    if has_libssh:
        assert conn.ssh_type == "libssh"
    else:
        assert conn.ssh_type == "paramiko"


@pytest.mark.parametrize("become_method,become_pass", [("enable", "password"), (None, None)])
def test_network_cli__connect(conn, become_method, become_pass):
    conn.ssh = MagicMock()
    conn.receive = MagicMock()
    conn._terminal = MagicMock()
    conn._ssh_type_conn = MagicMock()

    if become_method:
        conn._play_context.become = True
        conn._play_context.become_method = become_method
        conn._play_context.become_pass = become_pass

    conn._connect()
    assert conn._ssh_type_conn._connect.called is True
    assert conn._terminal.on_open_shell.called is True
    if become_method:
        conn._terminal.on_become.assert_called_with(passwd=become_pass)
    else:
        assert conn._terminal.on_become.called is False


@pytest.mark.parametrize("command", ["command", json.dumps({"command": "command"})])
def test_network_cli_exec_command(conn, command):
    mock_send = MagicMock(return_value=b"command response")
    conn.send = mock_send
    conn._ssh_shell = MagicMock()
    conn._ssh_type_conn = MagicMock()

    out = conn.exec_command(command)

    mock_send.assert_called_with(command=b"command")
    assert out == b"command response"


@pytest.mark.parametrize(
    "response",
    [
        [b"device#command\ncommand response\n\ndevice#"],
        [b"device#command\ncommand ", b"response\n\ndevice#"],
        pytest.param(
            [b"ERROR: error message device#"],
            marks=pytest.mark.xfail(raises=AnsibleConnectionFailure),
        ),
    ],
)
@pytest.mark.parametrize("ssh_type", ["paramiko", "libssh", "auto"])
def test_network_cli_send(conn, response, ssh_type):
    conn.set_options(
        direct={
            "ssh_type": ssh_type,
            "terminal_stderr_re": [{"pattern": "^ERROR"}],
            "terminal_stdout_re": [{"pattern": "device#"}],
        }
    )
    mock__shell = MagicMock()

    conn._terminal = MagicMock()
    conn._ssh_shell = mock__shell
    conn._connected = True

    if conn.ssh_type == "paramiko":
        mock__shell.recv.side_effect = [*response, None]
    elif conn.ssh_type == "libssh":
        mock__shell.read_bulk_response.side_effect = [*response, None]
    conn.send(b"command")

    mock__shell.sendall.assert_called_with(b"command\r")
    assert to_text(conn._command_response) == "command response"


def test_network_cli_close(conn):
    conn._terminal = MagicMock()
    conn._ssh_shell = MagicMock()
    conn._ssh_type_conn = MagicMock()
    conn._connected = True

    conn.close()

    assert conn._connected is False
    assert conn._terminal.on_close_shell.called is True
    assert conn._ssh_shell is None
    assert conn._ssh_type_conn is None


# ---- Note - Added as part of parammiko implicit PR - remove post 2028
def test_network_cli_close_when_not_connected(conn):
    """close() when _connected is False should not call terminal or close ssh_type_conn."""
    conn._terminal = MagicMock()
    conn._ssh_shell = MagicMock()
    conn._ssh_type_conn = MagicMock()
    conn._connected = False

    conn.close()

    conn._terminal.on_close_shell.assert_not_called()
    conn._ssh_type_conn.close.assert_not_called()


# ---- ssh_type and paramiko_conn ----
def test_network_cli_ssh_type_invalid(conn):
    # set_options validates choices, so set internal _ssh_type to trigger the runtime check
    conn._ssh_type = "invalid"

    with pytest.raises(AnsibleConnectionFailure) as excinfo:
        conn.ssh_type

    assert "Invalid value 'invalid'" in str(excinfo.value)


def test_network_cli_paramiko_conn_returns_ssh_type_conn(conn):
    conn.set_options(direct={"ssh_type": "libssh"})
    assert conn.paramiko_conn is conn.ssh_type_conn


# ---- get_prompt ----
def test_network_cli_get_prompt(conn):
    conn._connected = True
    conn._matched_prompt = b"device#"
    conn.update_cli_prompt_context = MagicMock()

    assert conn.get_prompt() == b"device#"
    conn.update_cli_prompt_context.assert_called_once()


def test_network_cli_get_prompt_ensures_connect(conn):
    """get_prompt triggers _connect when not connected."""
    conn._connected = False
    conn._matched_prompt = b"device#"
    conn._connect = MagicMock()
    conn.update_cli_prompt_context = MagicMock()

    conn.get_prompt()

    conn._connect.assert_called_once()


# ---- exec_command ----
def test_network_cli_exec_command_json_with_keys(conn):
    """exec_command with JSON cmd and prompt/answer/sendonly passes kwargs to send."""
    conn._ssh_shell = MagicMock()
    conn.send = MagicMock(return_value=b"output")
    conn._connected = True

    cmd = json.dumps(
        {
            "command": "show run",
            "prompt": r"\[y/N\]",
            "answer": "y",
            "sendonly": False,
        }
    )
    out = conn.exec_command(cmd)

    conn.send.assert_called_once()
    call_kw = conn.send.call_args[1]
    assert call_kw.get("command") == b"show run"
    assert "prompt" in call_kw
    assert "answer" in call_kw
    assert call_kw.get("sendonly") is False
    assert out == b"output"


def test_network_cli_exec_command_value_error_falls_back_to_bytes(conn):
    """Invalid JSON in cmd is treated as raw bytes command."""
    conn._ssh_shell = MagicMock()
    conn.send = MagicMock(return_value=b"output")
    conn._connected = True

    out = conn.exec_command(b"show version")

    conn.send.assert_called_once_with(command=b"show version")
    assert out == b"output"


# ---- _get_terminal_std_re ----
def test_network_cli_get_terminal_std_re_from_option(conn):
    conn.set_options(
        direct={
            "ssh_type": "libssh",
            "terminal_stdout_re": [{"pattern": r"hostname#"}],
        }
    )
    conn._terminal = _make_terminal_mock()

    result = conn._get_terminal_std_re("terminal_stdout_re")

    assert len(result) == 1
    assert result[0].pattern == rb"hostname#"


def test_network_cli_get_terminal_std_re_missing_pattern_raises(conn):
    conn.set_options(
        direct={
            "ssh_type": "libssh",
            "terminal_stdout_re": [{"flags": "re.I"}],
        }
    )
    conn._terminal = _make_terminal_mock()

    with pytest.raises(AnsibleConnectionFailure) as excinfo:
        conn._get_terminal_std_re("terminal_stdout_re")

    assert "pattern" in str(excinfo.value).lower()


def test_network_cli_get_terminal_std_re_with_flags(conn):
    conn.set_options(
        direct={
            "ssh_type": "libssh",
            "terminal_stdout_re": [{"pattern": r"prompt", "flags": "re.I"}],
        }
    )
    conn._terminal = _make_terminal_mock()

    result = conn._get_terminal_std_re("terminal_stdout_re")

    assert len(result) == 1
    assert result[0].flags & re.I


def test_network_cli_get_terminal_std_re_fallback_to_terminal(conn):
    conn.set_options(direct={"ssh_type": "libssh"})
    terminal = _make_terminal_mock()
    terminal.terminal_stdout_re = [re.compile(rb"fallback#")]
    conn._terminal = terminal

    result = conn._get_terminal_std_re("terminal_stdout_re")

    assert result == [re.compile(rb"fallback#")]


# ---- _strip, _sanitize, _find_prompt, _find_error ----
def test_network_cli_strip(conn):
    terminal = _make_terminal_mock(ansi_re=[re.compile(rb"\x1b\[[\d;]*m")])
    conn._terminal = terminal

    data = b"\x1b[32mdevice#\x1b[0m"
    out = conn._strip(data)

    assert out == b"device#"


def test_network_cli_sanitize(conn):
    conn._matched_prompt = b"device#"
    resp = b"line1\ncommand\nline2\ndevice#"
    out = conn._sanitize(resp, command=b"command", strip_prompt=True)

    assert b"line1" in out
    assert b"line2" in out
    assert b"command" not in out


def test_network_cli_find_prompt(conn):
    conn._terminal_stdout_re = [re.compile(rb"device#")]
    conn._log_messages = MagicMock()

    found = conn._find_prompt(b"output\ndevice#")

    assert found is True
    assert conn._matched_prompt == b"device#"


def test_network_cli_find_prompt_no_match(conn):
    conn._terminal_stdout_re = [re.compile(rb"device#")]

    found = conn._find_prompt(b"no prompt here")

    assert found is False


def test_network_cli_find_error(conn):
    conn._terminal_stderr_re = [re.compile(rb"^ERROR")]
    conn._matched_pattern = b"device#"
    conn._log_messages = MagicMock()

    found = conn._find_error(b"ERROR: something failed")

    assert found is True


def test_network_cli_find_error_no_match(conn):
    conn._terminal_stderr_re = [re.compile(rb"^ERROR")]

    found = conn._find_error(b"output ok")

    assert found is False


# ---- _validate_timeout_value ----
def test_network_cli_validate_timeout_value_negative_raises(conn):
    with pytest.raises(AnsibleConnectionFailure) as excinfo:
        conn._validate_timeout_value(-1, "test_timer")

    assert "invalid" in str(excinfo.value).lower()
    assert "test_timer" in str(excinfo.value)


def test_network_cli_validate_timeout_value_non_negative(conn):
    conn._validate_timeout_value(0, "test_timer")
    conn._validate_timeout_value(30, "test_timer")


# ---- _handle_prompt ----
def test_network_cli_handle_prompt_single_match(conn):
    conn._ssh_shell = MagicMock()
    conn._log_messages = MagicMock()
    conn._matched_cmd_prompt = None

    found = conn._handle_prompt(
        b"device#",
        prompts=[b"device#"],
        answer=[b""],
        newline=True,
        check_all=False,
    )

    assert found is True
    conn._ssh_shell.sendall.assert_called_once()


def test_network_cli_handle_prompt_regex_compile_error(conn):
    with pytest.raises(ConnectionError) as excinfo:
        conn._handle_prompt(
            b"data",
            prompts=["[invalid"],
            answer=[""],
            newline=True,
            check_all=False,
        )
    assert "compile" in str(excinfo.value).lower() or "regex" in str(excinfo.value).lower()


# ---- get_cache ----
def test_network_cli_get_cache(conn):
    conn._cache = None
    with patch.object(cache_loader, "get", return_value=MagicMock()) as mock_get:
        cache = conn.get_cache()
        assert cache is mock_get.return_value
        mock_get.assert_called_once_with("ansible.netcommon.memory")
    assert conn._cache is cache


def test_network_cli_get_cache_reuses_existing(conn):
    existing = MagicMock()
    conn._cache = existing
    assert conn.get_cache() is existing


# ---- _is_in_config_mode ----
def test_network_cli_is_in_config_mode_true(conn):
    conn._matched_prompt = b"(config)#"
    conn.get_prompt = lambda: conn._matched_prompt
    conn._terminal = MagicMock()
    conn._terminal.terminal_config_prompt = re.compile(r"\(config\)#")

    assert conn._is_in_config_mode() is True


def test_network_cli_is_in_config_mode_false(conn):
    conn._matched_prompt = b"device#"
    conn.get_prompt = lambda: conn._matched_prompt
    conn._terminal = MagicMock()
    conn._terminal.terminal_config_prompt = re.compile(r"\(config\)#")

    assert conn._is_in_config_mode() is False


def test_network_cli_is_in_config_mode_no_config_prompt_attr(conn):
    conn._matched_prompt = b"device#"
    conn.get_prompt = lambda: conn._matched_prompt
    conn._terminal = MagicMock(spec=[])  # no terminal_config_prompt

    assert conn._is_in_config_mode() is False


# ---- send check_all validation ----
def test_network_cli_send_check_all_prompt_answer_length_mismatch(conn):
    conn._connected = True
    conn._ssh_shell = MagicMock()
    conn._terminal_stdout_re = [re.compile(rb"#")]
    conn._terminal_stderr_re = []
    conn._terminal = _make_terminal_mock()
    conn.receive = MagicMock(return_value=b"device#")
    conn._single_user_mode = False

    with pytest.raises(AnsibleConnectionFailure) as excinfo:
        conn.send(
            b"cmd",
            prompt=[b"p1", b"p2"],
            answer=[b"a1"],
            check_all=True,
        )
    assert "not same" in str(excinfo.value) or "prompts" in str(excinfo.value).lower()


# ---- transport_test ----
def test_network_cli_transport_test(conn):
    conn.close = MagicMock()
    conn._connect = MagicMock()

    conn.transport_test(connect_timeout=10)

    assert conn.close.call_count == 2
    conn._connect.assert_called_once()


# ---- _on_become ----
@pytest.mark.parametrize(
    "become_errors,should_raise", [("fail", True), ("warn", False), ("ignore", False)]
)
def test_network_cli_on_become_errors(conn, become_errors, should_raise):
    conn._terminal = MagicMock()
    conn._terminal.on_become.side_effect = AnsibleConnectionFailure("auth failed")
    conn.set_options(direct={"ssh_type": "libssh", "become_errors": become_errors})

    if should_raise:
        with pytest.raises(AnsibleConnectionFailure):
            conn._on_become(become_pass="secret")
    else:
        conn._on_become(become_pass="secret")
    conn._terminal.on_become.assert_called_once_with(passwd="secret")


# ---- _on_open_shell ----
@pytest.mark.parametrize(
    "terminal_errors,should_raise", [("fail", True), ("warn", False), ("ignore", False)]
)
def test_network_cli_on_open_shell_errors(conn, terminal_errors, should_raise):
    conn._terminal = MagicMock()
    conn._terminal.on_open_shell.side_effect = AnsibleConnectionFailure("terminal failed")
    conn.set_options(direct={"ssh_type": "libssh", "terminal_errors": terminal_errors})

    if should_raise:
        with pytest.raises(AnsibleConnectionFailure):
            conn._on_open_shell()
    else:
        conn._on_open_shell()
    conn._terminal.on_open_shell.assert_called_once()


# ---- _connect retry ----
def test_network_cli_connect_retries_then_succeeds(conn):
    mock_ssh = MagicMock()
    mock_ssh.ssh.invoke_shell.return_value = MagicMock()
    conn.set_options(direct={"ssh_type": "libssh", "network_cli_retries": 2})
    conn._ssh_type_conn = MagicMock()
    conn._ssh_type_conn._connect = MagicMock(
        side_effect=[Exception("first"), Exception("second"), mock_ssh]
    )
    conn._ssh_type_conn._set_log_channel = MagicMock()
    conn._ssh_type_conn.force_persistence = False
    conn._play_context.become = False
    conn._terminal = _make_terminal_mock()
    conn._ssh_shell = None
    conn.receive = MagicMock()

    conn._connect()

    assert conn._ssh_type_conn._connect.call_count == 3


def test_network_cli_connect_retries_exhausted_raises(conn):
    conn.set_options(direct={"ssh_type": "libssh", "network_cli_retries": 1})
    conn._ssh_type_conn = MagicMock()
    conn._ssh_type_conn._connect = MagicMock(side_effect=Exception("connect failed"))
    conn._ssh_type_conn._set_log_channel = MagicMock()
    conn._ssh_type_conn.force_persistence = False

    with pytest.raises(AnsibleConnectionFailure) as excinfo:
        conn._connect()
    assert "connect failed" in str(excinfo.value)


def test_network_cli_connect_ansible_error_propagates(conn):
    conn.set_options(direct={"ssh_type": "libssh"})
    conn._ssh_type_conn = MagicMock()
    conn._ssh_type_conn._connect = MagicMock(side_effect=AnsibleError("ansible error"))
    conn._ssh_type_conn._set_log_channel = MagicMock()
    conn._ssh_type_conn.force_persistence = False

    with pytest.raises(AnsibleError) as excinfo:
        conn._connect()
    assert "ansible error" in str(excinfo.value)


# ---- _ParamikoConnection ----
def test_paramiko_connection_get_option_from_defaults():
    from ansible_collections.ansible.netcommon.plugins.connection.network_cli import (
        _ParamikoConnection,
    )

    pc = PlayContext()
    pc.remote_addr = "192.168.1.1"
    pc.remote_user = "admin"
    paramiko_conn = _ParamikoConnection(pc, "/dev/null", parent_connection=None)

    assert paramiko_conn.get_option("remote_addr") == "192.168.1.1"
    assert paramiko_conn.get_option("port") == 22
    assert paramiko_conn.get_option("host_key_checking") is True


def test_paramiko_connection_get_option_unknown_raises():
    from ansible_collections.ansible.netcommon.plugins.connection.network_cli import (
        _ParamikoConnection,
    )

    pc = PlayContext()
    paramiko_conn = _ParamikoConnection(pc, "/dev/null", parent_connection=None)

    with pytest.raises(KeyError):
        paramiko_conn.get_option("ssh_type")


def test_paramiko_connection_set_option_get_option():
    from ansible_collections.ansible.netcommon.plugins.connection.network_cli import (
        _ParamikoConnection,
    )

    pc = PlayContext()
    paramiko_conn = _ParamikoConnection(pc, "/dev/null", parent_connection=None)
    paramiko_conn.set_option("port", 2222)

    assert paramiko_conn.get_option("port") == 2222


def test_paramiko_connection_set_options_only_stores_known():
    from ansible_collections.ansible.netcommon.plugins.connection.network_cli import (
        _ParamikoConnection,
    )

    pc = PlayContext()
    paramiko_conn = _ParamikoConnection(pc, "/dev/null", parent_connection=None)
    paramiko_conn.set_options(
        direct={"port": 2222, "ssh_type": "libssh", "proxy_command": "nc %h %p"}
    )

    assert paramiko_conn.get_option("port") == 2222
    assert paramiko_conn.get_option("proxy_command") == "nc %h %p"
    with pytest.raises(KeyError):
        paramiko_conn.get_option("ssh_type")


def test_paramiko_connection_cache_key():
    from ansible_collections.ansible.netcommon.plugins.connection.network_cli import (
        _ParamikoConnection,
    )

    pc = PlayContext()
    pc.remote_addr = "host1"
    pc.remote_user = "user1"
    paramiko_conn = _ParamikoConnection(pc, "/dev/null", parent_connection=None)

    key = paramiko_conn._cache_key()
    assert "host1" in key
    assert "user1" in key


def test_paramiko_connection_connect_uncached_without_paramiko():
    from ansible_collections.ansible.netcommon.plugins.connection import network_cli

    orig_has = network_cli.HAS_PARAMIKO
    orig_err = network_cli.PARAMIKO_IMPORT_ERR
    try:
        network_cli.HAS_PARAMIKO = False
        network_cli.PARAMIKO_IMPORT_ERR = Exception("paramiko not installed")

        pc = PlayContext()
        pc.remote_addr = "host1"
        pc.remote_user = "user1"
        paramiko_conn = network_cli._ParamikoConnection(pc, "/dev/null", parent_connection=None)

        with pytest.raises(AnsibleError) as excinfo:
            paramiko_conn._connect_uncached()
        assert "paramiko is not installed" in str(excinfo.value)
    finally:
        network_cli.HAS_PARAMIKO = orig_has
        network_cli.PARAMIKO_IMPORT_ERR = orig_err
