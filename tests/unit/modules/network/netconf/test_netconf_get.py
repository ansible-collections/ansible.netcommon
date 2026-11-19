# (c) 2026 Red Hat Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import patch

from lxml.etree import fromstring

from ansible_collections.ansible.netcommon.plugins.modules import netconf_get
from ansible_collections.ansible.netcommon.tests.unit.modules.utils import (
    AnsibleExitJson,
    ModuleTestCase,
    set_module_args,
)


NC_NS = "urn:ietf:params:xml:ns:netconf:base:1.0"
SR_NS = "http://cisco.com/ns/yang/Cisco-IOS-XR-segment-routing-ms-cfg"
ISIS_NS = "http://cisco.com/ns/yang/Cisco-IOS-XR-um-router-isis-cfg"
SAMPLE_REPLY = b'<data xmlns="urn:ietf:params:xml:ns:netconf:base:1.0"/>'
CAPABILITIES = {"device_operations": {"supports_xpath": True}}


@patch("ansible_collections.ansible.netcommon.plugins.modules.netconf_get.get_capabilities")
class TestNetconfGetFilter(ModuleTestCase):
    def _filter_spec(self, args):
        """Run the module and return the filter argument passed to get/get_config."""
        set_module_args(args)
        target = "get_config" if "source" in args else "get"
        with patch(
            "ansible_collections.ansible.netcommon.plugins.modules.netconf_get." + target,
        ) as mock_rpc:
            mock_rpc.return_value = fromstring(SAMPLE_REPLY)
            with self.assertRaises(AnsibleExitJson):
                netconf_get.main()
        args, _kwargs = mock_rpc.call_args
        return args[2] if target == "get_config" else args[1]

    def _assert_single_filter(self, spec):
        """spec must be one <filter type="subtree"> element holding both subtrees (GH#790)."""
        self.assertIsInstance(spec, str, "a wrapped filter must not be passed as a tuple")
        root = fromstring(spec)
        self.assertEqual(root.tag, "{%s}filter" % NC_NS)
        self.assertEqual(root.get("type"), "subtree")
        self.assertEqual(
            [child.tag for child in root],
            ["{%s}sr" % SR_NS, "{%s}router" % ISIS_NS],
        )

    def test_wrapped_subtree_filter_is_not_wrapped_again(self, mock_caps):
        mock_caps.return_value = CAPABILITIES
        spec = self._filter_spec(
            {
                "source": "running",
                "filter": '<filter type="subtree"><sr xmlns="%s"/><router xmlns="%s"/></filter>'
                % (SR_NS, ISIS_NS),
            },
        )
        self._assert_single_filter(spec)

    def test_wrapped_filter_with_base_namespace_and_get(self, mock_caps):
        mock_caps.return_value = CAPABILITIES
        spec = self._filter_spec(
            {
                "filter": '<filter xmlns="%s"><sr xmlns="%s"/><router xmlns="%s"/></filter>'
                % (NC_NS, SR_NS, ISIS_NS),
            },
        )
        self._assert_single_filter(spec)

    def test_plain_subtree_filter_is_unchanged(self, mock_caps):
        mock_caps.return_value = CAPABILITIES
        xml = '<router xmlns="%s"/>' % ISIS_NS
        spec = self._filter_spec({"source": "running", "filter": xml})
        self.assertEqual(spec, ("subtree", xml))

    def test_xpath_filter_is_unchanged(self, mock_caps):
        mock_caps.return_value = CAPABILITIES
        spec = self._filter_spec({"source": "running", "filter": "/router"})
        self.assertEqual(spec, ("xpath", "/router"))
