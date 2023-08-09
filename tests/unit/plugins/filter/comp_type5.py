# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible_collections.ansible.netcommon.plugins.plugin_utils.comp_type5 import comp_type5


class TestComp_type5(unittest.TestCase):
    def setUp(self):
        pass

    def test_comp_type5_plugin_1(self):
        unencrypted_password = "cisco@123"
        encrypted_password = "$1$avs$uSTOEMh65qzvpb9yBMpzd/"
        args = [unencrypted_password, encrypted_password, False]
        result = comp_type5(*args)
        self.assertEqual(
            True,
            result,
        )

    def test_comp_type5_plugin_2(self):
        unencrypted_password = "cisco@123"
        encrypted_password = "$1$avs$uSTOEMh65qzvpb9yBMpzd/"
        args = [unencrypted_password, encrypted_password, True]
        result = comp_type5(*args)
        self.assertEqual(
            encrypted_password,
            result,
        )
