# (c) 2025 Red Hat Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from lxml.etree import fromstring

from ansible_collections.ansible.netcommon.plugins.modules import netconf_rpc
from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleExitJson,
    ModuleTestCase,
    set_module_args,
)


SAMPLE_RPC_REPLY = b'<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><data/></rpc-reply>'


class TestNetconfRpcOutputType(ModuleTestCase):
    def _run(self, args):
        set_module_args(args)
        with self.assertRaises(AnsibleExitJson) as exc:
            netconf_rpc.main()
        return exc.exception.args[0]

    @patch("ansible_collections.ansible.netcommon.plugins.modules.netconf_rpc.dispatch")
    def test_output_and_stdout_are_str_with_display_pretty(self, mock_dispatch):
        """output and stdout must be str, not bytes, when display=pretty (GH#791)."""
        mock_dispatch.return_value = fromstring(SAMPLE_RPC_REPLY)
        result = self._run({"rpc": "get-config", "display": "pretty"})
        self.assertIsInstance(result["output"], str, "output should be str, not bytes")
        self.assertIsInstance(result["stdout"], str, "stdout should be str, not bytes")

    @patch("ansible_collections.ansible.netcommon.plugins.modules.netconf_rpc.dispatch")
    def test_stdout_is_str_with_display_xml(self, mock_dispatch):
        """stdout must be str, not bytes, when display=xml (GH#791)."""
        mock_dispatch.return_value = fromstring(SAMPLE_RPC_REPLY)
        result = self._run({"rpc": "get-config", "display": "xml"})
        self.assertIsInstance(result["stdout"], str, "stdout should be str, not bytes")
