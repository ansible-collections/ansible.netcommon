# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy
from jinja2 import Template, TemplateSyntaxError
from ansible.playbook.task import Task
from ansible.template import Templar
from ansible_collections.ansible.netcommon.tests.unit.compat import unittest
from ansible_collections.ansible.netcommon.tests.unit.compat.mock import (
    MagicMock,
)
from ansible_collections.ansible.netcommon.tests.unit.mock.loader import (
    DictDataLoader,
)
from ansible_collections.ansible.netcommon.plugins.action.update_fact import (
    ActionModule,
)

VALID_DATA = {
    "a": {
        "b": {"4.4": [{"1": {5: {"foo": 123}}}], 5.5: "float5.5"},
        "127.0.0.1": "localhost",
    }
}

VALID_TESTS = [
    {
        "path": 'a.b["4.4"][0]["1"].5[\'foo\']',
        "split": ["a", "b", "4.4", 0, "1", 5, "foo"],
        "template_result": "123",
    },
    {
        "path": 'a.b["4.4"][0]["1"].5[\'foo\']',
        "split": ["a", "b", "4.4", 0, "1", 5, "foo"],
        "template_result": "123",
    },
    {
        "path": "a.b[5.5]",
        "split": ["a", "b", 5.5],
        "template_result": "float5.5",
    },
    {
        "path": "a['127.0.0.1']",
        "split": ["a", "127.0.0.1"],
        "template_result": "localhost",
    },
    {
        "path": "a.b['4.4'].0['1'].5['foo']",
        "split": ["a", "b", "4.4", 0, "1", 5, "foo"],
        "template_result": "123",
    },
]


INVALID_JINJA = [
    {
        "path": "a.'1'",
        "note": "quoted values are required to be in brackets",
        "error": "expected name or number",
    },
    {
        "path": "a.[1]",
        "note": "brackets can't follow dots",
        "error": "expected name or number",
    },
    {
        "path": 'a.b["4.4"][0]["1"]."5"[\'foo\']',
        "note": "quoted values are required to be in brackets",
        "error": "expected name or number",
    },
]


class TestUpdate_Fact(unittest.TestCase):
    def setUp(self):
        task = MagicMock(Task)
        play_context = MagicMock()
        play_context.check_mode = False
        connection = MagicMock()
        fake_loader = DictDataLoader({})
        templar = Templar(loader=fake_loader)
        self._plugin = ActionModule(
            task=task,
            connection=connection,
            play_context=play_context,
            loader=fake_loader,
            templar=templar,
            shared_loader_obj=None,
        )
        self._plugin._task.action = "update_fact"

    def test_argspec_no_updates(self):
        """Check passing invalid argspec"""
        self._plugin._task.args = {"a": 10}
        with self.assertRaises(Exception) as error:
            self._plugin.run(task_vars=None)
        self.assertIn(
            "Unsupported parameters for 'update_fact' module",
            str(error.exception),
        )

    def test_argspec_none(self):
        """Check passing a dict"""
        self._plugin._task.args = {}
        with self.assertRaises(Exception) as error:
            self._plugin.run(task_vars=None)
        self.assertIn(
            "missing required arguments: updates", str(error.exception)
        )

    def test_valid_jinja(self):
        for test in VALID_TESTS:
            tmplt = Template("{{" + test["path"] + "}}")
            result = tmplt.render(VALID_DATA)
            self.assertEqual(result, test["template_result"])

    def test_invalid_jinja(self):
        for test in INVALID_JINJA:
            with self.assertRaises(TemplateSyntaxError) as error:
                Template("{{" + test["path"] + "}}")
            self.assertIn(test["error"], str(error.exception))

    def test_fields(self):
        """Check the parsing of a path into it's parts"""
        for stest in VALID_TESTS:
            result = self._plugin._field_split(stest["path"])
            self.assertEqual(result, stest["split"])

    def test_missing_var(self):
        """Check for a missing fact"""
        self._plugin._task.args = {"updates": [{"path": "a.b.c", "value": 5}]}
        with self.assertRaises(Exception) as error:
            self._plugin.run(task_vars={"vars": {}})
        self.assertIn(
            "'a' was not found in the current facts.", str(error.exception)
        )

    def test_run_simple(self):
        """Confirm a valid argspec passes"""
        task_vars = {"vars": {"a": {"b": [1, 2, 3]}}}
        expected = copy.deepcopy(task_vars["vars"])
        expected["a"]["b"] = 5
        expected.update({"changed": True})
        self._plugin._task.args = {"updates": [{"path": "a.b", "value": 5}]}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)

    def test_run_multiple(self):
        """Confirm multiple paths passes"""
        task_vars = {
            "vars": {"a": {"b1": [1, 2, 3], "b2": {"c": "123", "d": False}}}
        }
        expected = {"a": {"b1": [1, 2, 3, 4], "b2": {"c": 456, "d": True}}}
        expected.update({"changed": True})
        self._plugin._task.args = {
            "updates": [
                {"path": "a.b1.3", "value": 4},
                {"path": "a.b2.c", "value": 456},
                {"path": "a.b2.d", "value": True},
            ]
        }
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)

    def test_run_replace_in_list(self):
        """Replace in list"""
        task_vars = {"vars": {"a": {"b": [1, 2, 3]}}}
        expected = copy.deepcopy(task_vars["vars"])
        expected["a"]["b"][1] = 5
        expected.update({"changed": True})
        self._plugin._task.args = {"updates": [{"path": "a.b.1", "value": 5}]}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)

    def test_run_append_to_list(self):
        """Append to list"""
        task_vars = {"vars": {"a": {"b": [1, 2, 3]}}}
        expected = copy.deepcopy(task_vars["vars"])
        expected["a"]["b"].append(4)
        expected.update({"changed": True})
        self._plugin._task.args = {"updates": [{"path": "a.b.3", "value": 4}]}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)

    def test_run_bracket_single_quote(self):
        """Bracket notation sigle quote"""
        task_vars = {"vars": {"a": {"b": [1, 2, 3]}}}
        expected = copy.deepcopy(task_vars["vars"])
        expected["a"]["b"].append(4)
        expected.update({"changed": True})
        self._plugin._task.args = {
            "updates": [{"path": "a['b'][3]", "value": 4}]
        }
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)

    def test_run_bracket_double_quote(self):
        """Bracket notation double quote"""
        task_vars = {"vars": {"a": {"b": [1, 2, 3]}}}
        expected = copy.deepcopy(task_vars["vars"])
        expected["a"]["b"].append(4)
        expected.update({"changed": True})
        self._plugin._task.args = {
            "updates": [{"path": 'a["b"][3]', "value": 4}]
        }
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)

    def test_run_int_dict_keys(self):
        """Integer dict keys"""
        task_vars = {"vars": {"a": {0: [1, 2, 3]}}}
        expected = copy.deepcopy(task_vars["vars"])
        expected["a"][0][0] = 0
        expected.update({"changed": True})
        self._plugin._task.args = {"updates": [{"path": "a.0.0", "value": 0}]}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)

    def test_run_int_as_string(self):
        """Integer dict keys as string"""
        task_vars = {"vars": {"a": {"0": [1, 2, 3]}}}
        expected = copy.deepcopy(task_vars["vars"])
        expected["a"]["0"][0] = 0
        expected.update({"changed": True})
        self._plugin._task.args = {
            "updates": [{"path": 'a["0"].0', "value": 0}]
        }
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)

    def test_run_invalid_path_quote_after_dot(self):
        """Invalid path format"""
        self._plugin._task.args = {"updates": [{"path": "a.'b'", "value": 0}]}
        with self.assertRaises(Exception) as error:
            self._plugin.run(task_vars={"vars": {}})
        self.assertIn("malformed", str(error.exception))

    def test_run_invalid_path_bracket_after_dot(self):
        """Invalid path format"""
        self._plugin._task.args = {
            "updates": [{"path": "a.['b']", "value": 0}]
        }
        with self.assertRaises(Exception) as error:
            self._plugin.run(task_vars={"vars": {}})
        self.assertIn("malformed", str(error.exception))

    def test_run_invalid_key_start_with_dot(self):
        """Invalid key format"""
        self._plugin._task.args = {"updates": [{"path": ".abc", "value": 0}]}
        with self.assertRaises(Exception) as error:
            self._plugin.run(task_vars={"vars": {}})
        self.assertIn("malformed", str(error.exception))

    def test_run_no_update_list(self):
        """Confirm no change when same"""
        task_vars = {"vars": {"a": {"b": [1, 2, 3]}}}
        expected = copy.deepcopy(task_vars["vars"])
        expected["a"]["b"] = [1, 2, 3]
        expected.update({"changed": False})
        self._plugin._task.args = {"updates": [{"path": "a.b.0", "value": 1}]}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)

    def test_run_no_update_dict(self):
        """Confirm no change when same"""
        task_vars = {"vars": {"a": {"b": [1, 2, 3]}}}
        expected = copy.deepcopy(task_vars["vars"])
        expected["a"]["b"] = [1, 2, 3]
        expected.update({"changed": False})
        self._plugin._task.args = {
            "updates": [{"path": "a.b", "value": [1, 2, 3]}]
        }
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)

    def test_run_missing_key(self):
        """Confirm error when key not found"""
        task_vars = {"vars": {"a": {"b": 1}}}
        self._plugin._task.args = {"updates": [{"path": "a.c.d", "value": 1}]}
        with self.assertRaises(Exception) as error:
            self._plugin.run(task_vars=task_vars)
        self.assertIn("the key 'c' was not found", str(error.exception))

    def test_run_list_not_int(self):
        """Confirm error when key not found"""
        task_vars = {"vars": {"a": {"b": [1]}}}
        self._plugin._task.args = {
            "updates": [{"path": "a.b['0']", "value": 2}]
        }
        with self.assertRaises(Exception) as error:
            self._plugin.run(task_vars=task_vars)
        self.assertIn(
            "index provided was not an integer", str(error.exception)
        )

    def test_run_list_not_long(self):
        """List not long enough"""
        task_vars = {"vars": {"a": {"b": [0]}}}
        self._plugin._task.args = {"updates": [{"path": "a.b.2", "value": 2}]}
        with self.assertRaises(Exception) as error:
            self._plugin.run(task_vars=task_vars)
        self.assertIn(
            "not long enough for item #2 to be set", str(error.exception)
        )

    def test_not_mutable_sequence_or_mapping(self):
        """Confirm graceful fail when immutable object
        This should never happen in the real world
        """
        obj = {"a": frozenset([1, 2, 3])}
        path = ["a", 0]
        val = 9
        with self.assertRaises(Exception) as error:
            self._plugin.set_value(obj, path, val)
        self.assertIn("can only modify mutable objects", str(error.exception))

    def test_run_not_dotted_success_one(self):
        """Test with a not dotted key"""
        task_vars = {"vars": {"a": 0}}
        expected = copy.deepcopy(task_vars["vars"])
        expected["a"] = 1
        expected.update({"changed": True})
        self._plugin._task.args = {"updates": [{"path": "a", "value": 1}]}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)

    def test_run_not_dotted_success_three(self):
        """Test with a not dotted key longer"""
        task_vars = {"vars": {"abc": 0}}
        expected = copy.deepcopy(task_vars["vars"])
        expected["abc"] = 1
        expected.update({"changed": True})
        self._plugin._task.args = {"updates": [{"path": "abc", "value": 1}]}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)

    def test_run_not_dotted_fail_missing(self):
        """Test with a not dotted key, missing"""
        task_vars = {"vars": {"abc": 0}}
        self._plugin._task.args = {"updates": [{"path": "123", "value": 1}]}
        with self.assertRaises(Exception) as error:
            self._plugin.run(task_vars=task_vars)
        self.assertIn(
            "'123' was not found in the current facts", str(error.exception)
        )

    def test_run_not_dotted_success_same(self):
        """Test with a not dotted key, no change"""
        task_vars = {"vars": {"a": 0}}
        expected = copy.deepcopy(task_vars["vars"])
        expected.update({"changed": False})
        self._plugin._task.args = {"updates": [{"path": "a", "value": 0}]}
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)

    def test_run_looks_like_a_bool(self):
        """Test with a key that looks like a bool"""
        task_vars = {"vars": {"a": {"True": 0}}}
        expected = copy.deepcopy(task_vars["vars"])
        expected["a"]["True"] = 1
        expected.update({"changed": True})
        self._plugin._task.args = {
            "updates": [{"path": "a['True']", "value": 1}]
        }
        result = self._plugin.run(task_vars=task_vars)
        self.assertEqual(result, expected)
