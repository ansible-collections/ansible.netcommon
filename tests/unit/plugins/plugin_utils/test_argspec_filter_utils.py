# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from copy import deepcopy
from unittest import TestCase

from ansible_collections.ansible.netcommon.plugins.plugin_utils.argspec_filter_utils import (
    convert_to_native,
)


class TestConvertToNative(TestCase):
    def test_none(self):
        self.assertIs(convert_to_native(None), None)

    def test_bool(self):
        self.assertIs(convert_to_native(True), True)
        self.assertIs(convert_to_native(False), False)

    def test_int_float_str(self):
        self.assertEqual(convert_to_native(42), 42)
        self.assertEqual(convert_to_native(3.14), 3.14)
        self.assertEqual(convert_to_native("hello"), "hello")

    def test_list_to_list(self):
        inp = [1, 2, 3]
        out = convert_to_native(inp)
        self.assertEqual(out, [1, 2, 3])
        self.assertIsInstance(out, list)

    def test_tuple_to_list(self):
        inp = (1, 2, 3)
        out = convert_to_native(inp)
        self.assertEqual(out, [1, 2, 3])
        self.assertIsInstance(out, list)

    def test_dict_to_dict(self):
        inp = {"a": 1, "b": 2}
        out = convert_to_native(inp)
        self.assertEqual(out, {"a": 1, "b": 2})
        self.assertIsInstance(out, dict)

    def test_nested(self):
        inp = {"data": [1, 2, 3], "first_line_len": 20, "other_line_len": 44}
        out = convert_to_native(inp)
        self.assertEqual(out, {"data": [1, 2, 3], "first_line_len": 20, "other_line_len": 44})
        self.assertIsInstance(out["data"], list)

    def test_list_subclass_converted_to_native_list(self):
        """List subclasses (e.g. lazy wrappers) become plain lists so deepcopy works."""

        class UncopyableList(list):
            def __deepcopy__(self, memo):
                raise NotImplementedError("Cannot deepcopy lazy container")

        uncopyable = UncopyableList([1, 2, 3])
        out = convert_to_native({"data": uncopyable})
        self.assertEqual(out, {"data": [1, 2, 3]})
        self.assertIsInstance(out["data"], list)
        # Verify the original would have failed deepcopy
        with self.assertRaises(NotImplementedError):
            deepcopy(uncopyable)
