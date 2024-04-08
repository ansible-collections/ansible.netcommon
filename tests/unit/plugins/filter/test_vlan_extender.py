# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.netcommon.plugins.plugin_utils.vlan_expander import vlan_expander


class TestVlanExtender(TestCase):
    def setUp(self):
        pass

    def test_vlan_extender_plugin_1(self):
        data = "1,13-19,24,26,34-56"
        args = [data]
        result = vlan_expander(*args)
        self.assertEqual(
            result,
            [
                1,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                24,
                26,
                34,
                35,
                36,
                37,
                38,
                39,
                40,
                41,
                42,
                43,
                44,
                45,
                46,
                47,
                48,
                49,
                50,
                51,
                52,
                53,
                54,
                55,
                56,
            ],
        )

    def test_vlan_extender_plugin_2(self):
        data = "13-19"
        args = [data]
        result = vlan_expander(*args)
        self.assertEqual(
            result,
            [
                13,
                14,
                15,
                16,
                17,
                18,
                19,
            ],
        )
