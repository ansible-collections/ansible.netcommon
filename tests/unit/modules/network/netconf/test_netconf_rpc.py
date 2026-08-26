# (c) 2025 Red Hat Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import MagicMock, patch

from lxml.etree import fromstring

from ansible_collections.ansible.netcommon.plugins.modules import netconf_rpc
from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    ModuleTestCase,
    fail_json,
    set_module_args,
)


SAMPLE_RPC_REPLY = b'<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"><data/></rpc-reply>'


class TestNetconfRpcOutputType(ModuleTestCase):
    def _run(self, args):
        set_module_args(args)
        with self.assertRaises(AnsibleExitJson) as exc:
            netconf_rpc.main()
        return exc.exception.args[0]

    def _fail(self, args):
        set_module_args(args)
        with self.assertRaises(AnsibleFailJson) as exc:
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
        self.assertIsInstance(result["output"], str, "output should be str, not bytes")

    @patch("ansible_collections.ansible.netcommon.plugins.modules.netconf_rpc.dispatch")
    def test_stdout_without_display(self, mock_dispatch):
        mock_dispatch.return_value = fromstring(SAMPLE_RPC_REPLY)
        result = self._run({"rpc": "get-config"})
        self.assertIsInstance(result["stdout"], str)
        self.assertIsNone(result["output"])
        mock_dispatch.assert_called_once_with(
            mock_dispatch.call_args[0][0],
            "<get-config/>",
        )

    @patch("ansible_collections.ansible.netcommon.plugins.modules.netconf_rpc.HAS_JXMLEASE", True)
    @patch("ansible_collections.ansible.netcommon.plugins.modules.netconf_rpc.jxmlease")
    @patch("ansible_collections.ansible.netcommon.plugins.modules.netconf_rpc.dispatch")
    def test_display_json(self, mock_dispatch, mock_jxmlease):
        mock_dispatch.return_value = fromstring(SAMPLE_RPC_REPLY)
        mock_jxmlease.parse.return_value = {"data": None}
        result = self._run({"rpc": "get-config", "display": "json"})
        self.assertIsInstance(result["stdout"], str)
        self.assertEqual(result["output"], {"data": None})

    @patch("ansible_collections.ansible.netcommon.plugins.modules.netconf_rpc.HAS_JXMLEASE", True)
    @patch("ansible_collections.ansible.netcommon.plugins.modules.netconf_rpc.jxmlease")
    @patch("ansible_collections.ansible.netcommon.plugins.modules.netconf_rpc.dispatch")
    def test_rpc_with_xmlns_and_dict_content(self, mock_dispatch, mock_jxmlease):
        mock_dispatch.return_value = fromstring(SAMPLE_RPC_REPLY)
        mock_jxmlease.XMLDictNode.return_value.emit_xml.return_value = (
            "<target><candidate/></target>"
        )
        result = self._run(
            {
                "rpc": "lock",
                "xmlns": "urn:ietf:params:xml:ns:netconf:base:1.0",
                "content": {"target": {"candidate": None}},
            }
        )
        self.assertIsInstance(result["stdout"], str)
        mock_dispatch.assert_called_once()
        self.assertIn(
            'xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"', mock_dispatch.call_args[0][1]
        )
        self.assertIn("<target>", mock_dispatch.call_args[0][1])

    @patch("ansible_collections.ansible.netcommon.plugins.modules.netconf_rpc.dispatch")
    def test_rpc_with_xml_content_string(self, mock_dispatch):
        mock_dispatch.return_value = fromstring(SAMPLE_RPC_REPLY)
        self._run(
            {
                "rpc": "get",
                "content": "<filter><data/></filter>",
            }
        )
        mock_dispatch.assert_called_once_with(
            mock_dispatch.call_args[0][0],
            "<get><filter><data/></filter></get>",
        )

    def test_empty_rpc_fails(self):
        result = self._fail({"rpc": "   "})
        self.assertEqual(result["msg"], "argument `rpc` must not be empty")

    def test_close_session_fails(self):
        result = self._fail({"rpc": "close-session"})
        self.assertEqual(result["msg"], "unsupported operation `close-session`")

    @patch("ansible_collections.ansible.netcommon.plugins.modules.netconf_rpc.HAS_JXMLEASE", False)
    def test_display_json_without_jxmlease_fails(self):
        result = self._fail({"rpc": "get-config", "display": "json"})
        self.assertIn("jxmlease is required to display response in json format", result["msg"])


class TestNetconfRpcGetXmlRequest(ModuleTestCase):
    def _module(self):
        module = MagicMock()
        module.fail_json.side_effect = fail_json
        return module

    def test_no_content_no_xmlns(self):
        result = netconf_rpc.get_xml_request(self._module(), "lock", None, None)
        self.assertEqual(result, "<lock/>")

    def test_no_content_with_xmlns(self):
        result = netconf_rpc.get_xml_request(
            self._module(),
            "lock",
            "urn:ietf:params:xml:ns:netconf:base:1.0",
            None,
        )
        self.assertEqual(
            result,
            '<lock xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"/>',
        )

    def test_xml_content_no_xmlns(self):
        result = netconf_rpc.get_xml_request(
            self._module(),
            "get",
            None,
            "<filter><data/></filter>",
        )
        self.assertEqual(result, "<get><filter><data/></filter></get>")

    def test_xml_content_with_xmlns(self):
        result = netconf_rpc.get_xml_request(
            self._module(),
            "get",
            "urn:ietf:params:xml:ns:netconf:base:1.0",
            "<filter><data/></filter>",
        )
        self.assertEqual(
            result,
            '<get xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">'
            "<filter><data/></filter></get>",
        )

    def test_dict_string_content(self):
        result = netconf_rpc.get_xml_request(
            self._module(),
            "lock",
            None,
            "{'target': {'candidate': None}}",
        )
        self.assertEqual(result, "<lock><target><candidate></candidate></target></lock>")

    def test_dict_content(self):
        result = netconf_rpc.get_xml_request(
            self._module(),
            "lock",
            "urn:ietf:params:xml:ns:netconf:base:1.0",
            {"target": {"candidate": None}},
        )
        self.assertEqual(
            result,
            '<lock xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">'
            "<target><candidate></candidate></target></lock>",
        )

    def test_unsupported_content_string_fails(self):
        module = self._module()
        with self.assertRaises(AnsibleFailJson) as exc:
            netconf_rpc.get_xml_request(module, "lock", None, "not-valid-content")
        self.assertEqual(
            exc.exception.args[0]["msg"], "unsupported content value `not-valid-content`"
        )

    def test_unsupported_content_type_fails(self):
        module = self._module()
        with self.assertRaises(AnsibleFailJson) as exc:
            netconf_rpc.get_xml_request(module, "lock", None, [1, 2, 3])
        self.assertEqual(exc.exception.args[0]["msg"], "unsupported content data-type `list`")

    @patch("ansible_collections.ansible.netcommon.plugins.modules.netconf_rpc.HAS_JXMLEASE", False)
    def test_dict_content_without_jxmlease_fails(self):
        module = self._module()
        with self.assertRaises(AnsibleFailJson) as exc:
            netconf_rpc.get_xml_request(
                module,
                "lock",
                None,
                {"target": {"candidate": None}},
            )
        self.assertIn(
            "jxmlease is required to convert RPC content to XML", exc.exception.args[0]["msg"]
        )
