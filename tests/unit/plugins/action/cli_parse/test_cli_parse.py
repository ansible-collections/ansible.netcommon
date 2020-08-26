# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import tempfile
from ansible.playbook.task import Task
from ansible.template import Templar

from ansible_collections.ansible.netcommon.tests.unit.compat import unittest
from ansible_collections.ansible.netcommon.tests.unit.compat.mock import (
    MagicMock,
    patch,
)
from ansible_collections.ansible.netcommon.tests.unit.mock.loader import (
    DictDataLoader,
)
from ansible_collections.ansible.netcommon.plugins.action.cli_parse import (
    ActionModule,
)


class TestCli_Parse(unittest.TestCase):
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
        self._plugin._task.action = "cli_parse"

    def test_fn_debug(self):
        """ Confirm debug doesn't fail and return None
        """
        msg = "some message"
        result = self._plugin._debug(msg)
        self.assertEqual(result, None)

    def test_fn_ail_json(self):
        """ Confirm fail json replaces basic.py in msg
        """
        msg = "text (basic.py)"
        with self.assertRaises(Exception) as error:
            self._plugin._fail_json(msg)
        self.assertEqual("text cli_parse", str(error.exception))

    def test_fn_check_argspec_pass(self):
        """ Confirm a valid argspec passes
        """
        self._plugin._task.args = {
            "text": "text",
            "parser": {
                "name": "ansible.netcommon.pyats",
                "command": "show version",
            },
        }
        result = self._plugin._check_argspec()
        self.assertEqual(result, None)

    def test_fn_check_argspec_fail_no_test_or_command(self):
        """ Confirm failed argpsec w/o text or command
        """
        self._plugin._task.args = {
            "parser": {
                "name": "ansible.netcommon.pyats",
                "command": "show version",
            }
        }
        self._plugin.task_vars = {"ansible_network_os": "cisco.nxos.nxos"}
        with self.assertRaises(Exception) as error:
            self._plugin._check_argspec()
        self.assertEqual(
            "one of the following is required: command, text",
            str(error.exception),
        )

    def test_fn_check_argspec_fail_no_parser_name(self):
        """ Confirm failed argspec no parser name
        """
        self._plugin._task.args = {
            "text": "anything",
            "parser": {"command": "show version"},
        }
        with self.assertRaises(Exception) as error:
            self._plugin._check_argspec()
        self.assertEqual(
            "missing required arguments: name found in parser",
            str(error.exception),
        )

    def test_fn_extended_check_argspec_parser_name_not_coll(self):
        """ Confirm failed argpsec parser not collection format
        """
        self._plugin._task.args = {
            "text": "anything",
            "parser": {
                "command": "show version",
                "name": "not_collection_format",
            },
        }
        self._plugin._extended_check_argspec()
        self.assertTrue(self._plugin._result["failed"])
        self.assertIn("including collection", self._plugin._result["msg"])

    def test_fn_extended_check_argspec_missing_tpath_or_command(self):
        """ Confirm failed argpsec missing template_path
        or command when text provided
        """
        self._plugin._task.args = {
            "text": "anything",
            "parser": {"name": "a.b.c"},
        }
        self._plugin._extended_check_argspec()
        self.assertTrue(self._plugin._result["failed"])
        self.assertIn(
            "provided when parsing text", self._plugin._result["msg"]
        )

    def test_fn_load_parser_pass(self):
        """ Confirm each each of the parsers loads from the filesystem
        """
        parser_names = [
            "json",
            "native",
            "ntc_templates",
            "pyats",
            "textfsm",
            "ttp",
            "xml",
        ]
        for parser_name in parser_names:
            self._plugin._task.args = {
                "text": "anything",
                "parser": {"name": "ansible.netcommon." + parser_name},
            }
            parser = self._plugin._load_parser(task_vars=None)
            self.assertEqual(type(parser).__name__, "CliParser")
            self.assertTrue(hasattr(parser, "parse"))
            self.assertTrue(callable(parser.parse))

    def test_fn_load_parser_fail(self):
        """ Confirm missing parser fails gracefully
        """
        self._plugin._task.args = {
            "text": "anything",
            "parser": {"name": "a.b.c"},
        }
        parser = self._plugin._load_parser(task_vars=None)
        self.assertIsNone(parser)
        self.assertTrue(self._plugin._result["failed"])
        self.assertIn("No module named", self._plugin._result["msg"])

    def test_fn_set_parser_command_missing(self):
        """ Confirm parser/command is set if missing
        and command provided
        """
        self._plugin._task.args = {
            "command": "anything",
            "parser": {"name": "a.b.c"},
        }
        self._plugin._set_parser_command()
        self.assertEqual(
            self._plugin._task.args["parser"]["command"], "anything"
        )

    def test_fn_set_parser_command_present(self):
        """ Confirm parser/command is not changed if provided
        """
        self._plugin._task.args = {
            "command": "anything",
            "parser": {"command": "something", "name": "a.b.c"},
        }
        self._plugin._set_parser_command()
        self.assertEqual(
            self._plugin._task.args["parser"]["command"], "something"
        )

    def test_fn_os_from_task_vars(self):
        """ Confirm os is set based on task vars
        """
        checks = [
            ("ansible_network_os", "cisco.nxos.nxos", "nxos"),
            ("ansible_network_os", "NXOS", "nxos"),
            ("ansible_distribution", "Fedora", "fedora"),
            (None, None, ""),
        ]
        for check in checks:
            self._plugin._task_vars = {check[0]: check[1]}
            result = self._plugin._os_from_task_vars()
            self.assertEqual(result, check[2])

    def test_fn_update_template_path_not_exist(self):
        """ Check the creation of the template_path if
        it doesn't exist in the user provided data
        """
        self._plugin._task.args = {
            "parser": {"command": "a command", "name": "a.b.c"}
        }
        self._plugin._task_vars = {"ansible_network_os": "cisco.nxos.nxos"}
        with self.assertRaises(Exception) as error:
            self._plugin._update_template_path("yaml")
        self.assertIn(
            "Could not find or access 'nxos_a_command.yaml'",
            str(error.exception),
        )

    def test_fn_get_template_contents_pass(self):
        """ Check the retrieval of the template contents
        """
        temp = tempfile.NamedTemporaryFile()
        contents = "abcdef"
        with open(temp.name, "w") as fileh:
            fileh.write(contents)

        self._plugin._task.args = {"parser": {"template_path": temp.name}}
        result = self._plugin._get_template_contents()
        self.assertEqual(result, contents)

    def test_fn_get_template_contents_missing(self):
        """ Check the retrieval of the template contents
        """
        self._plugin._task.args = {"parser": {"template_path": "non-exist"}}
        with self.assertRaises(Exception) as error:
            self._plugin._get_template_contents()
        self.assertIn(
            "Failed to open template 'non-exist'", str(error.exception)
        )

    def test_fn_prune_result_pass(self):
        """ Test the removal of stdout and stdout_lines from the _result
        """
        self._plugin._result["stdout"] = "abc"
        self._plugin._result["stdout_lines"] = "abc"
        self._plugin._prune_result()
        self.assertNotIn("stdout", self._plugin._result)
        self.assertNotIn("stdout_lines", self._plugin._result)

    def test_fn_prune_result_not_exist(self):
        """ Test the removal of stdout and stdout_lines from the _result
        """
        self._plugin._prune_result()
        self.assertNotIn("stdout", self._plugin._result)
        self.assertNotIn("stdout_lines", self._plugin._result)

    def test_fn_run_command_lx(self):
        """ Check run command for non network
        """
        response = "abc"
        self._plugin._connection.socket_path = None
        self._plugin._low_level_execute_command = MagicMock()
        self._plugin._low_level_execute_command.return_value = {
            "rc": 0,
            "stdout": response,
            "stdout_lines": response,
        }
        self._plugin._task.args = {"command": "ls"}
        res = self._plugin._run_command()
        self.assertEqual(self._plugin._result["stdout"], response)
        self.assertEqual(self._plugin._result["stdout_lines"], response)

    @patch("ansible.module_utils.connection.Connection.__rpc__")
    def test_fn_run_command_network(self, mock_rpc):
        """ Check run command for network
        """
        expected = "abc"
        mock_rpc.return_value = expected
        self._plugin._connection.socket_path = (
            tempfile.NamedTemporaryFile().name
        )
        self._plugin._task.args = {"command": "command"}
        res = self._plugin._run_command()
        self.assertEqual(self._plugin._result["stdout"], expected)
        self.assertEqual(self._plugin._result["stdout_lines"], [expected])
