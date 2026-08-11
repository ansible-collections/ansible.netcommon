# (c) 2016 Red Hat Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import MagicMock, patch

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    config as network_common_config,
)
from ansible_collections.ansible.netcommon.plugins.modules import cli_config
from ansible_collections.ansible.netcommon.tests.unit.modules.utils import set_module_args

from .cli_module import TestCliModule


# NetworkConfig(ignore_lines=[...]) permanently adds the supplied patterns to
# the module-level DEFAULT_IGNORE_LINES_RE set (see module_utils/network/common
# /config.py). Snapshot/restore it around each test the same way
# tests/unit/module_utils/network/common/test_config.py does, so a custom
# diff_ignore_lines pattern used in one test can't leak into another.
ORIGINAL_DEFAULT_IGNORE_LINES_RE = network_common_config.DEFAULT_IGNORE_LINES_RE.copy()


class TestCliConfigModule(TestCliModule):
    module = cli_config

    def setUp(self):
        super(TestCliConfigModule, self).setUp()

        self.mock_connection = patch(
            "ansible_collections.ansible.netcommon.plugins.modules.cli_config.Connection"
        )
        self.get_connection = self.mock_connection.start()

        self.conn = self.get_connection()
        # A well-formed capabilities payload where the platform explicitly
        # declares support for neither onbox diff nor generate diff (mirroring
        # what ansible.netcommon's own "default" cliconf plugin returns). Tests
        # that need other capabilities override this in-test.
        self.conn.get_capabilities.return_value = (
            '{"rpc": [], "device_operations":'
            ' {"supports_onbox_diff": false, "supports_generate_diff": false}}'
        )

    def tearDown(self):
        super(TestCliConfigModule, self).tearDown()

        self.mock_connection.stop()
        network_common_config.DEFAULT_IGNORE_LINES_RE = ORIGINAL_DEFAULT_IGNORE_LINES_RE.copy()

    @patch("ansible_collections.ansible.netcommon.plugins.modules.cli_config.run")
    def test_cli_config_backup_returns__backup__(self, run_mock):
        args = dict(backup=True)
        set_module_args(args)

        run_mock.return_value = {}

        result = self.execute_module()
        self.assertIn("__backup__", result)

    def test_cli_config_onbox_diff(self):
        self.conn.get_capabilities.return_value = (
            '{"device_operations": {"supports_onbox_diff": true}}'
        )
        set_module_args({"config": "set interface eth0 ip address dhcp"})
        self.execute_module()
        self.conn.edit_config.assert_called_once_with(
            candidate=["set interface eth0 ip address dhcp"],
            commit=True,
            replace=None,
            comment=None,
        )

    def test_cli_config_generate_diff(self):
        self.conn.get_capabilities.return_value = (
            '{"device_operations": {"supports_generate_diff": true}}'
        )
        diff = MagicMock()
        diff.get.side_effect = ["set interface eth0 ip address dhcp", None]
        self.conn.get_diff.return_value = diff
        set_module_args({"config": "set interface eth0 ip address dhcp"})
        self.execute_module(changed=True, commands=["set interface eth0 ip address dhcp"])
        self.conn.edit_config.assert_called_once_with(
            candidate=["set interface eth0 ip address dhcp"],
            commit=True,
            replace=None,
            comment=None,
        )

        diff.get.side_effect = [None, "new banner"]
        self.conn.get_diff.return_value = diff
        set_module_args({"config": "set banner\nnew banner"})
        self.execute_module(changed=True)
        self.conn.edit_banner.assert_called_once_with(candidate='"new banner"', commit=True)

    def test_cli_config_replace(self):
        self.conn.get_capabilities.return_value = """{
            "device_operations": {
                "supports_onbox_diff": true,
                "supports_replace": true
            }
        }"""
        self.conn.edit_config.return_value = {"diff": "set interface eth0 ip address dhcp"}

        args = {"config": "set interface eth0 ip address dhcp"}

        args["replace"] = True
        set_module_args(args)
        self.execute_module(changed=True)
        self.conn.edit_config.assert_called_with(
            candidate=["set interface eth0 ip address dhcp"],
            commit=True,
            replace=True,
            comment=None,
        )

        args["replace"] = False
        set_module_args(args)
        self.execute_module(changed=True)
        self.conn.edit_config.assert_called_with(
            candidate=["set interface eth0 ip address dhcp"],
            commit=True,
            replace=False,
            comment=None,
        )

    def test_cli_config_replace_unsupported(self):
        self.conn.get_capabilities.return_value = """{
            "device_operations": {
                "supports_onbox_diff": true,
                "supports_replace": false
            }
        }"""

        args = {
            "config": "set interface eth0 ip address dhcp",
            "replace": True,
        }
        set_module_args(args)
        result = self.execute_module(failed=True)
        self.assertEqual(result["msg"], "Option replace is not supported on this platform")

    def test_cli_config_replace_unspecified(self):
        self.conn.get_capabilities.return_value = """{
            "device_operations": {
                "supports_onbox_diff": true
            }
        }"""

        args = {
            "config": "set interface eth0 ip address dhcp",
            "replace": True,
        }
        set_module_args(args)
        result = self.execute_module(failed=True)
        self.assertEqual(
            result["msg"],
            "This platform does not specify whether replace is supported or not. Please report an issue against this platform's cliconf plugin.",
        )

    def test_cli_config_rollback(self):
        self.conn.get_capabilities.return_value = """{
            "device_operations": {
                "supports_rollback": true
            }
        }"""
        self.conn.rollback.return_value = {"diff": "set interface eth0 ip address dhcp"}

        args = {"rollback": 123456}
        set_module_args(args)
        self.execute_module(changed=True)

        self.conn.rollback.return_value = {}
        set_module_args(args)
        self.execute_module(changed=False)

    def test_cli_config_no_diff_support_changed(self):
        self.conn.get_config.side_effect = ["running before", "running after"]

        set_module_args({"config": "hostname foo"})
        self.execute_module(changed=True)
        self.conn.edit_config.assert_called_once_with(
            candidate=["hostname foo"],
            commit=True,
            replace=None,
            comment=None,
        )

    def test_cli_config_no_diff_support_unchanged(self):
        self.conn.get_config.side_effect = ["same config", "same config"]

        set_module_args({"config": "hostname foo"})
        self.execute_module(changed=False)
        self.conn.edit_config.assert_called_once_with(
            candidate=["hostname foo"],
            commit=True,
            replace=None,
            comment=None,
        )

    def test_cli_config_no_diff_support_check_mode(self):
        self.conn.get_config.return_value = "running config"

        args = {"config": "hostname foo", "_ansible_check_mode": True}
        set_module_args(args)
        self.execute_module(changed=False)
        self.conn.edit_config.assert_not_called()

    def test_cli_config_no_diff_support_returns_diff(self):
        self.conn.get_config.side_effect = ["running before", "running after"]

        args = {"config": "hostname foo", "_ansible_diff": True}
        set_module_args(args)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["diff"],
            {"before": "running before", "after": "running after"},
        )

    # --- Hardening: capabilities that couldn't be retrieved/parsed must not
    # be treated the same as a platform explicitly declaring no diff support.

    def test_cli_config_capabilities_empty_fails(self):
        self.conn.get_capabilities.return_value = "{}"

        set_module_args({"config": "hostname foo"})
        result = self.execute_module(failed=True)
        self.assertIn("Unable to retrieve device capabilities", result["msg"])
        self.conn.edit_config.assert_not_called()

    def test_cli_config_capabilities_null_fails(self):
        self.conn.get_capabilities.return_value = "null"

        set_module_args({"config": "hostname foo"})
        result = self.execute_module(failed=True)
        self.assertIn("Unable to retrieve device capabilities", result["msg"])
        self.conn.edit_config.assert_not_called()

    def test_cli_config_capabilities_not_a_dict_fails(self):
        self.conn.get_capabilities.return_value = "[]"

        set_module_args({"config": "hostname foo"})
        result = self.execute_module(failed=True)
        self.assertIn("Unable to retrieve device capabilities", result["msg"])
        self.conn.edit_config.assert_not_called()

    def test_cli_config_capabilities_missing_device_operations_fails(self):
        # A non-empty, well-formed dict that is nonetheless missing
        # device_operations entirely is just as malformed as an empty "{}"
        # response and must not be treated as a "no diff support" declaration.
        self.conn.get_capabilities.return_value = '{"rpc": [], "network_api": "cliconf"}'

        set_module_args({"config": "hostname foo"})
        result = self.execute_module(failed=True)
        self.assertIn("Unable to retrieve device capabilities", result["msg"])
        self.conn.edit_config.assert_not_called()

    # --- Regression: diff_ignore_lines validation must still be enforced
    # for code paths that don't actually reach the local-filtering fallback
    # branch, even when the platform supports neither onbox nor generate diff.

    def test_cli_config_rollback_with_unsupported_diff_ignore_lines_fails(self):
        # rollback takes priority over device_operations in run(), so
        # diff_ignore_lines is neither delegated nor applied locally here;
        # the platform's (non-)declaration must still be enforced.
        self.conn.get_capabilities.return_value = """{
            "device_operations": {
                "supports_rollback": true
            }
        }"""

        args = {"rollback": 123456, "diff_ignore_lines": ["foo"]}
        set_module_args(args)
        result = self.execute_module(failed=True)
        self.assertEqual(
            result["msg"],
            "This platform does not specify whether diff_ignore_lines is supported or not. "
            "Please report an issue against this platform's cliconf plugin.",
        )
        self.conn.rollback.assert_not_called()

    def test_cli_config_onbox_diff_with_unsupported_diff_ignore_lines_fails(self):
        self.conn.get_capabilities.return_value = """{
            "device_operations": {
                "supports_onbox_diff": true
            }
        }"""

        args = {
            "config": "hostname foo",
            "diff_ignore_lines": ["foo"],
        }
        set_module_args(args)
        result = self.execute_module(failed=True)
        self.assertEqual(
            result["msg"],
            "This platform does not specify whether diff_ignore_lines is supported or not. "
            "Please report an issue against this platform's cliconf plugin.",
        )
        self.conn.edit_config.assert_not_called()

    # --- Hardening: the before/after snapshot comparison must apply
    # diff_ignore_lines (and the built-in default ignore patterns), the same
    # way the supports_generate_diff branch already does, instead of a raw
    # string comparison that would flag volatile lines as a real change.

    def test_cli_config_no_diff_support_ignores_default_volatile_lines(self):
        # "Current configuration : N bytes" is one of the built-in ignore
        # patterns applied by NetworkConfig even without diff_ignore_lines set.
        self.conn.get_config.side_effect = [
            "hostname foo\nCurrent configuration : 100 bytes",
            "hostname foo\nCurrent configuration : 104 bytes",
        ]

        set_module_args({"config": "hostname foo"})
        self.execute_module(changed=False)

    def test_cli_config_no_diff_support_diff_ignore_lines_filters_custom_pattern(self):
        self.conn.get_config.side_effect = [
            "hostname foo\nLast configuration change at 10:00:00",
            "hostname foo\nLast configuration change at 10:00:05",
        ]

        args = {
            "config": "hostname foo",
            "diff_ignore_lines": ["Last configuration change"],
        }
        set_module_args(args)
        self.execute_module(changed=False)

    def test_cli_config_no_diff_support_detects_real_change_with_diff_ignore_lines(self):
        self.conn.get_config.side_effect = [
            "hostname foo\nLast configuration change at 10:00:00",
            "hostname bar\nLast configuration change at 10:00:05",
        ]

        args = {
            "config": "hostname bar",
            "diff_ignore_lines": ["Last configuration change"],
            "_ansible_diff": True,
        }
        set_module_args(args)
        result = self.execute_module(changed=True)
        self.assertEqual(
            result["diff"],
            {
                "before": "hostname foo\nLast configuration change at 10:00:00",
                "after": "hostname bar\nLast configuration change at 10:00:05",
            },
        )
