# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.netcommon.plugins.plugin_utils.type5_pw import type5_pw


class TestType5_pw(TestCase):
    def setUp(self):
        pass

    def check_version_and_get_expected_md5_crypt(self, password, salt):
        from ansible import release as ansible_release

        version_str = getattr(ansible_release, "__version__", "0.0")

        def _cmp_version(ver, thresh_major, thresh_minor):
            parts = ver.split(".")
            try:
                major = int(parts[0]) if len(parts) > 0 else 0
            except ValueError:
                major = 0
            try:
                minor = int(parts[1]) if len(parts) > 1 else 0
            except ValueError:
                minor = 0
            return (major, minor) >= (thresh_major, thresh_minor)

        use_do_encrypt = _cmp_version(version_str, 2, 20)
        try:
            from ansible.utils.encrypt import do_encrypt

            return do_encrypt(password, "md5_crypt", salt=salt)
        except ImportError:
            # Unexpected for core >= 2.20; fall back to stdlib crypt
            try:
                import crypt

                return crypt.crypt(password, "$1$%s$" % salt)
            except Exception as crypt_exc:
                raise RuntimeError("No suitable hashing backend available for tests") from crypt_exc

    def test_type5_pw_plugin_1(self):
        password = "cisco"
        salt = "nTc1"
        args = [password, salt]
        result = type5_pw(*args)
        # Uses helper to abstract passlib->do_encrypt swap (core PR 85970)
        expected = self.check_version_and_get_expected_md5_crypt(password, salt)

        self.assertEqual(result, expected)

    def test_type5_pw_plugin_2(self):
        password = "cisco"
        args = [password]
        result = type5_pw(*args)
        self.assertEqual(
            len(result),
            30,
        )
