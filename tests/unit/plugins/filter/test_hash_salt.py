# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.netcommon.plugins.filter.hash_salt import _hash_salt
from ansible_collections.ansible.netcommon.plugins.plugin_utils.hash_salt import hash_salt


class Testhash_salt(TestCase):
    def setUp(self):
        pass

    def test_hash_salt_plugin_1(self):
        password = "$1$avs$uSTOEMh65qzvpb9yBMpzd/TESTPASS"
        args = [password[0:-8]]
        result = hash_salt(*args)
        self.assertEqual(
            "avs",
            result,
        )

    def test_hash_salt_filter_wrapper(self):
        """Filter wrapper runs convert_to_native before validation."""
        env = None
        result = _hash_salt(env, "$1$avs$uSTOEMh65qzvpb9yBMpzd/")
        self.assertEqual(result, "avs")
