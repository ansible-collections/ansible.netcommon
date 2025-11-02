# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.netcommon.plugins.plugin_utils.comp_type5 import comp_type5
from tests.unit.plugins.plugin_utils.test_do_encrypt_utils import get_expected_md5_crypt


class TestComp_type5(TestCase):
    def setUp(self):
        pass

    def test_comp_type5_plugin_1(self):
        unencrypted_password = "cisco@123"
        # Uses helper to abstract passlib->do_encrypt swap (core PR 85970)
        encrypted_password = get_expected_md5_crypt(unencrypted_password, "avs")
        args = [unencrypted_password, encrypted_password, False]
        result = comp_type5(*args)
        self.assertEqual(
            True,
            result,
        )

    def test_comp_type5_plugin_2(self):
        unencrypted_password = "cisco@123"
        # Uses helper to abstract passlib->do_encrypt swap (core PR 85970)
        encrypted_password = get_expected_md5_crypt(unencrypted_password, "avs")
        args = [unencrypted_password, encrypted_password, True]
        result = comp_type5(*args)
        self.assertEqual(
            encrypted_password,
            result,
        )
