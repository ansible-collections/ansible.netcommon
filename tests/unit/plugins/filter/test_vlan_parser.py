# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.netcommon.plugins.plugin_utils.vlan_parser import vlan_parser


class TestVlanParser(unittest.TestCase):
    def setUp(self):
        pass

    def test_vlan_parser_plugin_1(self):
        data = [
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
        ]
        args = [data]
        result = vlan_parser(*args)
        self.assertEqual(
            result[0],
            "1,13-19,24,26,34-56",
        )

    def test_vlan_parser_plugin_2(self):
        data = [1, 2, 3]
        args = [data]
        result = vlan_parser(*args)
        self.assertEqual(
            result[0],
            "1-3",
        )

    def test_vlan_parser_fail_wrong_data(self):
        data = "13"
        args = [data]
        with self.assertRaises(AnsibleFilterError) as error:
            vlan_parser(*args)
        self.assertIn(
            "Input is not valid for vlan_parser",
            str(error.exception),
        )

    def test_vlan_parser_fail_out_range(self):
        data = [
            1,
            2013,
            2014,
            2015,
            2016,
            2017,
            2018,
            2019,
            2024,
            2026,
            4034,
            4035,
            4036,
            4037,
            4038,
            4039,
            4040,
            4041,
            4042,
            4311,
        ]
        args = [data]
        with self.assertRaises(AnsibleFilterError) as error:
            vlan_parser(*args)
        self.assertIn(
            "Valid VLAN range is 1-4094",
            str(error.exception),
        )
