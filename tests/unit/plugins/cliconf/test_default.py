#
# (c) 2016 Red Hat Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import json

import pytest

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
def plugin_fixture(monkeypatch):
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
