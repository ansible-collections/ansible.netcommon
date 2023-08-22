# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import unittest

from ansible_collections.ansible.netcommon.plugins.plugin_utils.type5_pw import type5_pw


class TestType5_pw(unittest.TestCase):
    def setUp(self):
        pass

    def test_type5_pw_plugin_1(self):
        password = "cisco"
        salt = "nTc1"
        args = [password, salt]
        result = type5_pw(*args)
        self.assertEqual(
            "$1$nTc1$Z28sUTcWfXlvVe2x.3XAa.TESTPASS",
            result + "TESTPASS",
        )

    def test_type5_pw_plugin_2(self):
        password = "cisco"
        args = [password]
        result = type5_pw(*args)
        self.assertEqual(
            len(result),
            30,
        )
