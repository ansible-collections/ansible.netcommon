# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.netcommon.plugins.plugin_utils.type5_pw import type5_pw
from tests.unit.plugins.plugin_utils.test_do_encrypt_utils import get_expected_md5_crypt


class TestType5_pw(TestCase):
    def setUp(self):
        pass

    def test_type5_pw_plugin_1(self):
        password = "cisco"
        salt = "nTc1"
        args = [password, salt]
        result = type5_pw(*args)
        # Uses helper to abstract passlib->do_encrypt swap (core PR 85970)
        expected = get_expected_md5_crypt(password, salt)

        self.assertEqual(result, expected)

    def test_type5_pw_plugin_2(self):
        password = "cisco"
        args = [password]
        result = type5_pw(*args)
        self.assertEqual(
            len(result),
            30,
        )
