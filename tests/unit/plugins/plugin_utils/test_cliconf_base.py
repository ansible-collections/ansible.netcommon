# (c) 2026 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import MagicMock, call

import pytest

from ansible_collections.ansible.netcommon.plugins.plugin_utils.cliconf_base import CliconfBase


class ConcreteCliconf(CliconfBase):
    def get_config(self, source="running", flags=None, format=None):
        pass

    def edit_config(self, candidate=None, commit=True, replace=None, comment=None):
        pass

    def get_capabilities(self):
        pass

    def get_device_info(self):
        return {}


@pytest.fixture()
def cliconf():
    obj = ConcreteCliconf.__new__(ConcreteCliconf)
    obj.send_command = MagicMock(return_value="ok")
    return obj


class TestSendConfigCommands:
    def test_string_candidate(self, cliconf):
        results, requests = cliconf._send_config_commands("interface loopback0")
        assert results == ["ok"]
        assert requests == ["interface loopback0"]
        cliconf.send_command.assert_any_call(command="interface loopback0")
        cliconf.send_command.assert_any_call("end")

    def test_list_candidate(self, cliconf):
        cmds = ["interface loopback0", "description test"]
        results, requests = cliconf._send_config_commands(cmds)
        assert results == ["ok", "ok"]
        assert requests == ["interface loopback0", "description test"]

    def test_list_of_dicts(self, cliconf):
        cmds = [
            {"command": "interface loopback0", "prompt": "#"},
            {"command": "description test"},
        ]
        results, requests = cliconf._send_config_commands(cmds)
        assert results == ["ok", "ok"]
        assert requests == ["interface loopback0", "description test"]
        cliconf.send_command.assert_any_call(command="interface loopback0", prompt="#")

    def test_custom_exit_command(self, cliconf):
        cliconf._send_config_commands("hostname R1", exit_command="exit")
        assert cliconf.send_command.call_args_list[-1] == call("exit")

    def test_cmd_filter_skips(self, cliconf):
        cmds = ["interface loopback0", "!", "description test"]
        results, requests = cliconf._send_config_commands(cmds, cmd_filter=lambda cmd: cmd != "!")
        assert requests == ["interface loopback0", "description test"]
        assert len(results) == 2

    def test_cmd_filter_none_sends_all(self, cliconf):
        cmds = ["a", "b", "c"]
        results, requests = cliconf._send_config_commands(cmds, cmd_filter=None)
        assert requests == ["a", "b", "c"]
        assert len(results) == 3

    def test_exit_command_sent_on_success(self, cliconf):
        cliconf._send_config_commands("hostname R1")
        assert cliconf.send_command.call_args_list[-1] == call("end")

    def test_exit_command_sent_on_exception(self, cliconf):
        cliconf.send_command = MagicMock(side_effect=[Exception("device error"), "ok"])
        with pytest.raises(Exception, match="device error"):
            cliconf._send_config_commands("bad command")
        assert cliconf.send_command.call_args_list[-1] == call("end")

    def test_empty_candidate(self, cliconf):
        results, requests = cliconf._send_config_commands([])
        assert results == []
        assert requests == []
        cliconf.send_command.assert_called_once_with("end")

    def test_mixed_string_and_dict_in_list(self, cliconf):
        cmds = ["interface loopback0", {"command": "shutdown"}]
        results, requests = cliconf._send_config_commands(cmds)
        assert requests == ["interface loopback0", "shutdown"]
        assert len(results) == 2
