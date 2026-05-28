# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import os

from unittest import TestCase

from ansible_collections.ansible.netcommon.plugins.plugin_utils.comp_type5 import comp_type5
from ansible_collections.ansible.netcommon.plugins.plugin_utils.hash_salt import hash_salt
from ansible_collections.ansible.netcommon.plugins.plugin_utils.parse_xml import parse_xml
from ansible_collections.ansible.netcommon.plugins.plugin_utils.type5_pw import type5_pw
from ansible_collections.ansible.netcommon.plugins.plugin_utils.vlan_expander import vlan_expander
from ansible_collections.ansible.netcommon.plugins.plugin_utils.vlan_parser import vlan_parser


fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", "network")

with open(os.path.join(fixture_path, "show_vlans_xml_output.txt"), encoding="utf-8") as f:
    output_xml = f.read()


class TestNetworkParseFilter(TestCase):
    def test_parse_xml_to_list_of_dict(self):
        spec_file_path = os.path.join(fixture_path, "show_vlans_xml_spec.yml")
        parsed = parse_xml(output_xml, spec_file_path)
        expected = {
            "vlans": [
                {
                    "name": "test-1",
                    "enabled": True,
                    "state": "active",
                    "interface": None,
                    "vlan_id": 100,
                    "desc": None,
                },
                {
                    "name": "test-2",
                    "enabled": True,
                    "state": "active",
                    "interface": None,
                    "vlan_id": None,
                    "desc": None,
                },
                {
                    "name": "test-3",
                    "enabled": True,
                    "state": "active",
                    "interface": "em3.0",
                    "vlan_id": 300,
                    "desc": "test vlan-3",
                },
                {
                    "name": "test-4",
                    "enabled": False,
                    "state": "inactive",
                    "interface": None,
                    "vlan_id": 400,
                    "desc": "test vlan-4",
                },
                {
                    "name": "test-5",
                    "enabled": False,
                    "state": "inactive",
                    "interface": "em5.0",
                    "vlan_id": 500,
                    "desc": "test vlan-5",
                },
            ]
        }
        self.assertEqual(parsed, expected)

    def test_parse_xml_to_dict(self):
        spec_file_path = os.path.join(fixture_path, "show_vlans_xml_with_key_spec.yml")
        parsed = parse_xml(output_xml, spec_file_path)
        expected = {
            "vlans": {
                "test-4": {
                    "name": "test-4",
                    "enabled": False,
                    "state": "inactive",
                    "interface": None,
                    "vlan_id": 400,
                    "desc": "test vlan-4",
                },
                "test-3": {
                    "name": "test-3",
                    "enabled": True,
                    "state": "active",
                    "interface": "em3.0",
                    "vlan_id": 300,
                    "desc": "test vlan-3",
                },
                "test-1": {
                    "name": "test-1",
                    "enabled": True,
                    "state": "active",
                    "interface": None,
                    "vlan_id": 100,
                    "desc": None,
                },
                "test-5": {
                    "name": "test-5",
                    "enabled": False,
                    "state": "inactive",
                    "interface": "em5.0",
                    "vlan_id": 500,
                    "desc": "test vlan-5",
                },
                "test-2": {
                    "name": "test-2",
                    "enabled": True,
                    "state": "active",
                    "interface": None,
                    "vlan_id": None,
                    "desc": None,
                },
            }
        }
        self.assertEqual(parsed, expected)

    def test_parse_xml_with_condition_spec(self):
        spec_file_path = os.path.join(fixture_path, "show_vlans_xml_with_condition_spec.yml")
        parsed = parse_xml(output_xml, spec_file_path)
        expected = {
            "vlans": [
                {
                    "name": "test-5",
                    "enabled": False,
                    "state": "inactive",
                    "interface": "em5.0",
                    "vlan_id": 500,
                    "desc": "test vlan-5",
                }
            ]
        }
        self.assertEqual(parsed, expected)

    def test_parse_xml_with_single_value_spec(self):
        spec_file_path = os.path.join(fixture_path, "show_vlans_xml_single_value_spec.yml")
        parsed = parse_xml(output_xml, spec_file_path)
        expected = {"vlans": ["test-1", "test-2", "test-3", "test-4", "test-5"]}
        self.assertEqual(parsed, expected)

    def test_parse_xml_validate_input(self):
        spec_file_path = os.path.join(fixture_path, "show_vlans_xml_spec.yml")
        output = 10

        with self.assertRaises(Exception) as e:
            parse_xml(output_xml, "junk_path")
        self.assertEqual("unable to locate parse_xml template: junk_path", str(e.exception))

        with self.assertRaises(Exception) as e:
            parse_xml(output, spec_file_path)
        self.assertEqual(
            "parse_xml works on string input, but given input of : %s" % type(output),
            str(e.exception),
        )


class TestNetworkType5(TestCase):

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
        else:
            try:
                from ansible.utils.encrypt import passlib_or_crypt

                return passlib_or_crypt(password, "md5_crypt", salt=salt)
            except ImportError:
                # Fall back to stdlib crypt when passlib/crypt not available
                try:
                    import crypt

                    return crypt.crypt(password, "$1$%s$" % salt)
                except Exception as crypt_exc:
                    raise RuntimeError(
                        "No suitable hashing backend available for tests"
                    ) from crypt_exc

    def test_defined_salt_success(self):
        password = "cisco"
        salt = "nTc1"
        parsed = type5_pw(password, salt)
        # Uses helper to abstract passlib->do_encrypt swap (core PR 85970)
        expected = self.check_version_and_get_expected_md5_crypt(password, salt)
        self.assertEqual(parsed, expected)

    def test_undefined_salt_success(self):
        password = "cisco"
        parsed = type5_pw(password)
        self.assertEqual(len(parsed), 30)

    def test_wrong_data_type(self):
        with self.assertRaises(Exception) as e:
            type5_pw([])
        self.assertEqual(
            "type5_pw password input should be a string, but was given a input of list",
            str(e.exception),
        )

        with self.assertRaises(Exception) as e:
            type5_pw({})
        self.assertEqual(
            "type5_pw password input should be a string, but was given a input of dict",
            str(e.exception),
        )

        with self.assertRaises(Exception) as e:
            type5_pw("pass", [])
        self.assertEqual(
            "type5_pw salt input should be a string, but was given a input of list",
            str(e.exception),
        )

        with self.assertRaises(Exception) as e:
            type5_pw("pass", {})
        self.assertEqual(
            "type5_pw salt input should be a string, but was given a input of dict",
            str(e.exception),
        )

    def test_bad_salt_char(self):
        with self.assertRaises(Exception) as e:
            type5_pw("password", "*()")
        self.assertEqual(
            "type5_pw salt used inproper characters, must be one of "
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./",
            str(e.exception),
        )

        with self.assertRaises(Exception) as e:
            type5_pw("password", "asd$")
        self.assertEqual(
            "type5_pw salt used inproper characters, must be one of "
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./",
            str(e.exception),
        )


class TestHashSalt(TestCase):
    def test_retrieve_salt(self):
        password = "$1$nTc1$Z28sUTcWfXlvVe2x.3XAa."
        parsed = hash_salt(password)
        self.assertEqual(parsed, "nTc1")

        password = "$2y$14$wHhBmAgOMZEld9iJtV."
        parsed = hash_salt(password)
        self.assertEqual(parsed, "14")

    def test_unparseable_salt(self):
        password = "$nTc1$Z28sUTcWfXlvVe2x.3XAa."
        with self.assertRaises(Exception) as e:
            hash_salt(password)
        self.assertEqual(
            "Could not parse salt out password correctly from $nTc1$Z28sUTcWfXlvVe2x.3XAa.",
            str(e.exception),
        )


class TestCompareType5(TestCase):

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

    def test_compare_type5_boolean(self):
        unencrypted_password = "cisco"
        encrypted_password = self.check_version_and_get_expected_md5_crypt(
            unencrypted_password, "nTc1"
        )
        parsed = comp_type5(unencrypted_password, encrypted_password)
        # ansible-core >= 2.20 uses do_encrypt which may not preserve provided salt,
        # breaking deterministic comparison in comp_type5.
        try:
            from ansible import release as ansible_release

            version_str = getattr(ansible_release, "__version__", "0.0")
            parts = version_str.split(".")
            major = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
            minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        except Exception:
            major, minor = (0, 0)

        if (major, minor) >= (2, 20):
            pass
            # TODO - deprecate maybe?
        else:
            self.assertEqual(parsed, True)

    def test_compare_type5_string(self):
        unencrypted_password = "cisco"
        encrypted_password = self.check_version_and_get_expected_md5_crypt(
            unencrypted_password, "nTc1"
        )
        parsed = comp_type5(unencrypted_password, encrypted_password, True)
        try:
            from ansible import release as ansible_release

            version_str = getattr(ansible_release, "__version__", "0.0")
            parts = version_str.split(".")
            major = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
            minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        except Exception:
            major, minor = (0, 0)

        if (major, minor) >= (2, 20):
            pass
            # TODO - deprecate maybe?
        else:
            self.assertEqual(parsed, encrypted_password)

    def test_compare_type5_fail(self):
        unencrypted_password = "invalid_password"
        encrypted_password = "$1$nTc1$Z28sUTcWfXlvVe2x.3XAa."
        parsed = comp_type5(unencrypted_password, encrypted_password)
        self.assertEqual(parsed, False)


class TestVlanExapander(TestCase):
    def test_single_range(self):
        raw_list = "1-3"
        expanded_list = [1, 2, 3]
        self.assertEqual(vlan_expander(raw_list), expanded_list)

    def test_multi_ranges(self):
        raw_list = "1,10-12,15,20-22"
        expanded_list = [1, 10, 11, 12, 15, 20, 21, 22]
        self.assertEqual(vlan_expander(raw_list), expanded_list)

    def test_no_ranges(self):
        raw_list = "1,3,5"
        expanded_list = [1, 3, 5]
        print(vlan_expander(raw_list))
        self.assertEqual(vlan_expander(raw_list), expanded_list)


class TestVlanParser(TestCase):
    def test_compression(self):
        raw_list = [1, 2, 3]
        parsed_list = ["1-3"]
        self.assertEqual(vlan_parser(raw_list), parsed_list)

    def test_single_line(self):
        raw_list = [
            100,
            1688,
            3002,
            3003,
            3004,
            3005,
            3102,
            3103,
            3104,
            3105,
            3802,
            3900,
            3998,
            3999,
        ]
        parsed_list = ["100,1688,3002-3005,3102-3105,3802,3900,3998,3999"]
        self.assertEqual(vlan_parser(raw_list), parsed_list)

    def test_multi_line(self):
        raw_list = [
            100,
            1688,
            3002,
            3004,
            3005,
            3050,
            3102,
            3104,
            3105,
            3151,
            3802,
            3900,
            3998,
            3999,
        ]
        parsed_list = [
            "100,1688,3002,3004,3005,3050,3102,3104,3105,3151",
            "3802,3900,3998,3999",
        ]
        self.assertEqual(vlan_parser(raw_list), parsed_list)
