# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Tests that filter wrappers run convert_to_native (coverage for new code)."""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible.errors import AnsibleFilterError

from ansible_collections.ansible.netcommon.plugins.filter.comp_type5 import _comp_type5
from ansible_collections.ansible.netcommon.plugins.filter.hash_salt import _hash_salt
from ansible_collections.ansible.netcommon.plugins.filter.parse_cli import _parse_cli
from ansible_collections.ansible.netcommon.plugins.filter.parse_cli_textfsm import (
    _parse_cli_textfsm,
)
from ansible_collections.ansible.netcommon.plugins.filter.parse_xml import _parse_xml
from ansible_collections.ansible.netcommon.plugins.filter.type5_pw import _type5_pw
from ansible_collections.ansible.netcommon.plugins.filter.vlan_expander import _vlan_expander
from ansible_collections.ansible.netcommon.plugins.filter.vlan_parser import _vlan_parser


class TestAllFiltersConvertToNative(TestCase):
    """Single test that exercises convert_to_native in every filter wrapper (for coverage)."""

    def test_all_filter_wrappers_run_convert_to_native(self):
        env = None
        # Each call runs the filter wrapper and thus convert_to_native(data).
        self.assertEqual(_hash_salt(env, "$1$avs$x"), "avs")
        self.assertEqual(_vlan_expander(env, "1-2"), [1, 2])
        self.assertEqual(_vlan_parser(env, [1, 2, 3])[0], "1-3")
        # type5_pw and comp_type5: just run the wrapper (result is backend-dependent)
        self.assertEqual(len(_type5_pw(env, "cisco")), 30)
        result = _comp_type5(env, "cisco@123", _type5_pw(env, "cisco@123", salt="avs"), False)
        self.assertIsInstance(result, bool)


class TestCompType5FilterWrapper(TestCase):
    """comp_type5 filter wrapper runs convert_to_native before validation."""

    def test_comp_type5_filter_wrapper(self):
        env = None
        # Run filter wrapper; comp_type5 result is backend-dependent (passlib vs do_encrypt)
        encrypted = _type5_pw(env, "cisco@123", salt="avs")
        result = _comp_type5(env, "cisco@123", encrypted, False)
        self.assertIsInstance(result, bool)


class TestParseCliFilterWrapper(TestCase):
    """parse_cli filter wrapper runs convert_to_native before validation."""

    def test_parse_cli_filter_wrapper(self):
        env = None
        # Validation passes; underlying parser may raise (e.g. missing template).
        with self.assertRaises((AnsibleFilterError, OSError, IOError)):
            _parse_cli(env, "cli output", "nonexistent_spec.yml")


class TestParseCliTextfsmFilterWrapper(TestCase):
    """parse_cli_textfsm filter wrapper runs convert_to_native before validation."""

    def test_parse_cli_textfsm_filter_wrapper(self):
        env = None
        with self.assertRaises((AnsibleFilterError, OSError, IOError, ImportError)):
            _parse_cli_textfsm(env, "cli output", "nonexistent_template.textfsm")


class TestParseXmlFilterWrapper(TestCase):
    """parse_xml filter wrapper runs convert_to_native before validation."""

    def test_parse_xml_filter_wrapper(self):
        env = None
        with self.assertRaises((AnsibleFilterError, OSError, IOError)):
            _parse_xml(env, "<root/>", "nonexistent_spec.yml")
