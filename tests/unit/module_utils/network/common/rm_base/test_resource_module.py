# -*- coding: utf-8 -*-
#
# (c) 2026 Red Hat, Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (
    NetworkTemplate,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.resource_module import (
    ResourceModule,
)


def _render_custom_flag(data):
    if data.get("custom_flag", {}).get("set") is False:
        return "no custom-flag"
    return "custom-flag"


class _CompareTemplate(NetworkTemplate):
    def __init__(self):
        super(_CompareTemplate, self).__init__(tmplt=self)

    PARSERS = [
        {
            "name": "flag",
            "setval": "flag",
            "result": {"flag": {"set": "{{ True }}"}},
        },
        {
            "name": "custom_flag",
            "setval": _render_custom_flag,
            "result": {"custom_flag": {"set": "{{ True }}"}},
        },
        {
            "name": "enabled",
            "setval": "enabled",
            "result": {"enabled": "{{ True }}"},
        },
    ]


class _CompareTester(ResourceModule):
    def __init__(self, tmplt):
        self.want = {}
        self.have = {}
        self.commands = []
        self._tmplt = tmplt
        self.addcmd_calls = []

    def addcmd(self, data, tmplt, negate=False):
        self.addcmd_calls.append((tmplt, negate))


class TestResourceModuleCompare(object):
    def setup_method(self):
        self.tester = _CompareTester(_CompareTemplate())

    def test_dict_set_false_negates_for_static_setval(self):
        self.tester.compare(
            parsers="flag",
            want={"flag": {"set": False}},
            have={"flag": {"set": True}},
        )
        assert self.tester.addcmd_calls == [("flag", True)]

    def test_dict_set_false_skips_when_absent_on_device(self):
        self.tester.compare(
            parsers="flag",
            want={"flag": {"set": False}},
            have={},
        )
        assert self.tester.addcmd_calls == []

    def test_dict_set_false_skips_when_already_disabled(self):
        self.tester.compare(
            parsers="flag",
            want={"flag": {"set": False}},
            have={"flag": {"set": False}},
        )
        assert self.tester.addcmd_calls == []

    def test_dict_set_true_enables_without_negation(self):
        self.tester.compare(
            parsers="flag",
            want={"flag": {"set": True}},
            have={},
        )
        assert self.tester.addcmd_calls == [("flag", False)]

    def test_bool_false_still_negates(self):
        self.tester.compare(
            parsers="enabled",
            want={"enabled": False},
            have={"enabled": True},
        )
        assert self.tester.addcmd_calls == [("enabled", True)]

    def test_dict_set_false_does_not_negate_for_callable_setval(self):
        self.tester.compare(
            parsers="custom_flag",
            want={"custom_flag": {"set": False}},
            have={"custom_flag": {"set": True}},
        )
        assert self.tester.addcmd_calls == [("custom_flag", False)]
