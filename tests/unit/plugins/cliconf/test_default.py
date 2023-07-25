#
# (c) 2016 Red Hat Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import json

from unittest.mock import MagicMock

import pytest

from ansible.errors import AnsibleConnectionFailure
from ansible.plugins.loader import cliconf_loader


INFO = dict(network_os="default")
OPERATIONS = {
    "supports_diff_replace": False,
    "supports_commit": False,
    "supports_rollback": False,
    "supports_defaults": False,
    "supports_onbox_diff": False,
    "supports_commit_comment": False,
    "supports_multiline_delimiter": False,
    "supports_diff_match": False,
    "supports_diff_ignore_lines": False,
    "supports_generate_diff": False,
    "supports_replace": False,
}
RPC = [
    "edit_config",
    "enable_response_logging",
    "get",
    "get_capabilities",
    "get_config",
    "disable_response_logging",
    "run_commands",
]


@pytest.fixture(name="cliconf")
def plugin_fixture():
    cliconf = cliconf_loader.get("ansible.netcommon.default", None)
    return cliconf


def test_get_device_info(cliconf):
    info = cliconf.get_device_info()
    assert info == INFO

    # Test cached info works
    assert info == cliconf.get_device_info()


def test_get_device_operations(cliconf):
    ops = cliconf.get_device_operations()
    assert ops == OPERATIONS


def test_get_capabilities(cliconf):
    cap = json.loads(cliconf.get_capabilities())
    assert cap == dict(
        rpc=RPC,
        device_info=INFO,
        network_api="cliconf",
        device_operations=OPERATIONS,
    )


@pytest.mark.parametrize("method", ["get_config", "edit_config", "commit", "discard_changes"])
def test_unsupported_method(cliconf, method):
    cliconf._play_context = MagicMock()
    cliconf._play_context.network_os = "default"

    with pytest.raises(
        AnsibleConnectionFailure, match=f"{method} is not supported by network_os default"
    ):
        getattr(cliconf, method)()


def test_get(cliconf):
    return_value = "ABC FakeOS v1.23.4"
    conn = MagicMock()
    conn.send.return_value = return_value
    cliconf._connection = conn
    resp = cliconf.get("show version")
    assert resp == return_value


def test_get_no_command(cliconf):
    with pytest.raises(ValueError, match="must provide value of command to execute"):
        cliconf.get()


@pytest.mark.parametrize("commands", ["show version", {"command": "show version"}])
def test_run_commands(cliconf, commands):
    return_value = "ABC FakeOS v1.23.4"
    conn = MagicMock()
    conn.send.return_value = return_value
    cliconf._connection = conn
    resp = cliconf.run_commands([commands])
    assert resp == [return_value]


@pytest.mark.parametrize("check_rc", [True, False])
def test_run_commands_check_rc(cliconf, check_rc):
    error = AnsibleConnectionFailure("Invalid command: [sow]")
    cliconf.send_command = MagicMock(side_effect=error)

    if check_rc:
        with pytest.raises(AnsibleConnectionFailure):
            resp = cliconf.run_commands(["sow version"], check_rc=check_rc)
    else:
        resp = cliconf.run_commands(["sow version"], check_rc=check_rc)
        assert resp == [error]


def test_run_commands_no_commands(cliconf):
    with pytest.raises(ValueError, match="'commands' value is required"):
        cliconf.run_commands()
