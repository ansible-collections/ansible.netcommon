# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The action plugin file for cli_parse
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from importlib import import_module

from ansible.errors import AnsibleActionFail
from ansible.module_utils._text import to_native, to_text
from ansible.module_utils.connection import (
    Connection,
    ConnectionError as AnsibleConnectionError,
)
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display

from ansible_collections.ansible.utils.plugins.modules.cli_parse import (
    DOCUMENTATION,
)
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    check_argspec,
)

# python 2.7 compat for FileNotFoundError
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


ARGSPEC_CONDITIONALS = {
    "argument_spec": {
        "parser": {"mutually_exclusive": [["command", "template_path"]]}
    },
    "required_one_of": [["command", "text"]],
    "mutually_exclusive": [["command", "text"]],
}

display = Display()


class ActionModule(ActionBase):
    """action module"""

    PARSER_CLS_NAME = "CliParser"

    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)
        self._playhost = None
        self._parser_name = None
        self._result = {}
        self._task_vars = None

    def _debug(self, msg):
        """Output text using ansible's display

        :param msg: The message
        :type msg: str
        """
        msg = "<{phost}> [cli_parse] {msg}".format(
            phost=self._playhost, msg=msg
        )
        self._display.vvvv(msg)

    def _fail_json(self, msg):
        """Replace the AnsibleModule fai_json here

        :param msg: The message for the failure
        :type msg: str
        """
        msg = msg.replace("(basic.py)", self._task.action)
        raise AnsibleActionFail(msg)

    def _extended_check_argspec(self):
        """Check additional requirements for the argspec
        that cannot be covered using stnd techniques
        """
        errors = []
        requested_parser = self._task.args.get("parser").get("name")
        if len(requested_parser.split(".")) != 3:
            msg = "Parser name should be provided as a full name including collection"
            errors.append(msg)

        if self._task.args.get("text") and requested_parser not in [
            "ansible.utils.json",
            "ansible.utils.xml",
        ]:
            if not (
                self._task.args.get("parser").get("command")
                or self._task.args.get("parser").get("template_path")
            ):
                msg = "Either parser/command or parser/template_path needs to be provided when parsing text."
                errors.append(msg)
        if errors:
            self._result["failed"] = True
            self._result["msg"] = " ".join(errors)

    def _load_parser(self, task_vars):
        """Load a parser from the fs

        :param task_vars: The vars provided when the task was run
        :type task_vars: dict
        :return: An instance of class CliParser
        :rtype: CliParser
        """
        requested_parser = self._task.args.get("parser").get("name")
        cref = dict(
            zip(["corg", "cname", "plugin"], requested_parser.split("."))
        )
        if cref["cname"] == "netcommon" and cref["plugin"] in [
            "json",
            "textfsm",
            "ttp",
            "xml",
        ]:
            cref["cname"] = "utils"
            msg = (
                "Use 'ansible.utils.{plugin}' for parser name instead of '{requested_parser}'."
                " This feature will be removed from 'ansible.netcommon' collection in a release"
                " after 2022-11-01".format(
                    plugin=cref["plugin"], requested_parser=requested_parser
                )
            )
            self._display.warning(msg)
            parserlib = "ansible_collections.{corg}.{cname}.plugins.sub_plugins.cli_parser.{plugin}_parser".format(
                **cref
            )
        elif cref["cname"] == "netcommon" and cref["plugin"] in [
            "native",
            "ntc_templates",
            "pyats",
        ]:
            parserlib = "ansible_collections.{corg}.{cname}.plugins.sub_plugins.cli_parser.{plugin}_parser".format(
                **cref
            )
        else:
            msg = (
                "The custom cli_parse sub-plugin location is changed from 'plugins/cli_parsers/' to 'plugins/sub_plugins/cli_parse/'."
                " Move the sub-plugins to the new location and update it to use the imports from 'ansible.utils>=2.0.0' collection."
                " The old sub-plugin location will no longer be supported after the end of the deprecation cycle for 'ansible.netcommon.cli_parse' module"
            )

            self._display.warning(msg)
            parserlib = "ansible_collections.{corg}.{cname}.plugins.cli_parsers.{plugin}_parser".format(
                **cref
            )
        try:
            parsercls = getattr(import_module(parserlib), self.PARSER_CLS_NAME)
            parser = parsercls(
                task_args=self._task.args,
                task_vars=task_vars,
                debug=self._debug,
            )
            return parser
        except Exception as exc:
            self._result["failed"] = True
            self._result["msg"] = "Error loading parser: {err}".format(
                err=to_native(exc)
            )
            return None

    def _set_parser_command(self):
        """Set the /parser/command in the task args based on /command if needed"""
        if self._task.args.get("command"):
            if not self._task.args.get("parser").get("command"):
                self._task.args.get("parser")["command"] = self._task.args.get(
                    "command"
                )

    def _set_text(self):
        """Set the /text in the task_args based on the command run"""
        if self._result.get("stdout"):
            self._task.args["text"] = self._result["stdout"]

    def _os_from_task_vars(self):
        """Extract an os str from the task's vars

        :return: A short OS name
        :rtype: str
        """
        os_vars = ["ansible_distribution", "ansible_network_os"]
        oper_sys = ""
        for hvar in os_vars:
            if self._task_vars.get(hvar):
                if hvar == "ansible_network_os":
                    oper_sys = self._task_vars.get(hvar, "").split(".")[-1]
                    self._debug(
                        "OS set to {os}, derived from ansible_network_os".format(
                            os=oper_sys.lower()
                        )
                    )
                else:
                    oper_sys = self._task_vars.get(hvar)
                    self._debug(
                        "OS set to {os}, using {key}".format(
                            os=oper_sys.lower(), key=hvar
                        )
                    )
        return oper_sys.lower()

    def _update_template_path(self, template_extension):
        """Update the template_path in the task args
        If not provided, generate template name using os and command

        :param template_extension: The parser specific template extension
        :type template extension: str
        """
        if not self._task.args.get("parser").get("template_path"):
            if self._task.args.get("parser").get("os"):
                oper_sys = self._task.args.get("parser").get("os")
            else:
                oper_sys = self._os_from_task_vars()
            cmd_as_fname = (
                self._task.args.get("parser").get("command").replace(" ", "_")
            )
            fname = "{os}_{cmd}.{ext}".format(
                os=oper_sys, cmd=cmd_as_fname, ext=template_extension
            )
            source = self._find_needle("templates", fname)
            self._debug(
                "template_path in task args updated to {source}".format(
                    source=source
                )
            )
            self._task.args["parser"]["template_path"] = source

    def _get_template_contents(self):
        """Retrieve the contents of the parser template

        :return: The parser's contents
        :rtype: str
        """
        template_contents = None
        template_path = self._task.args.get("parser").get("template_path")
        if template_path:
            try:
                with open(template_path, "rb") as file_handler:
                    try:
                        template_contents = to_text(
                            file_handler.read(), errors="surrogate_or_strict"
                        )
                    except UnicodeError:
                        raise AnsibleActionFail(
                            "Template source files must be utf-8 encoded"
                        )
            except FileNotFoundError as exc:
                raise AnsibleActionFail(
                    "Failed to open template '{tpath}'. Error: {err}".format(
                        tpath=template_path, err=to_native(exc)
                    )
                )
        return template_contents

    def _prune_result(self):
        """In the case of an error, remove stdout and stdout_lines
        this allows for easier visibility of the error message.
        In the case of an actual command error, it will be thrown
        in the module
        """
        self._result.pop("stdout", None)
        self._result.pop("stdout_lines", None)

    def _run_command(self):
        """Run a command on the host
        If socket_path exists, assume it's a network device
        else, run a low level command
        """
        command = self._task.args.get("command")
        if command:
            socket_path = self._connection.socket_path
            if socket_path:
                connection = Connection(socket_path)
                try:
                    response = connection.get(command=command)
                    self._result["stdout"] = response
                    self._result["stdout_lines"] = response.splitlines()
                except AnsibleConnectionError as exc:
                    self._result["failed"] = True
                    self._result["msg"] = [to_text(exc)]
            else:
                result = self._low_level_execute_command(cmd=command)
                if result["rc"]:
                    self._result["failed"] = True
                    self._result["msg"] = result["stderr"]
                self._result["stdout"] = result["stdout"]
                self._result["stdout_lines"] = result["stdout_lines"]

    def run(self, tmp=None, task_vars=None):
        """The std execution entry pt for an action plugin

        :param tmp: no longer used
        :type tmp: none
        :param task_vars: The vars provided when the task is run
        :type task_vars: dict
        :return: The results from the parser
        :rtype: dict
        """
        msg = (
            "Use 'ansible.utils.cli_parse' instead of 'ansible.netcommon.cli_parse'."
            " See the plugin documentation for more details."
            " This feature will be removed from ansible.netcommon in a release after 2023-01-01"
        )
        display.deprecated(
            msg, date="2023-01-01", collection_name="ansible.netcommon"
        )

        valid, argspec_result, updated_params = check_argspec(
            DOCUMENTATION,
            "cli_parse module",
            schema_conditionals=ARGSPEC_CONDITIONALS,
            **self._task.args
        )
        if not valid:
            return argspec_result

        self._extended_check_argspec()
        if self._result.get("failed"):
            return self._result

        self._task_vars = task_vars
        self._playhost = task_vars.get("inventory_hostname")
        self._parser_name = self._task.args.get("parser").get("name")

        self._run_command()
        if self._result.get("failed"):
            return self._result

        self._set_parser_command()
        self._set_text()

        parser = self._load_parser(task_vars)
        if self._result.get("failed"):
            self._prune_result()
            return self._result

        # Not all parsers use a template, in the case a parser provides
        # an extension, provide it the template path
        if getattr(parser, "DEFAULT_TEMPLATE_EXTENSION", False):
            self._update_template_path(parser.DEFAULT_TEMPLATE_EXTENSION)

        # Not all parsers require the template contents
        # when true, provide the template contents
        if getattr(parser, "PROVIDE_TEMPLATE_CONTENTS", False) is True:
            template_contents = self._get_template_contents()
        else:
            template_contents = None

        try:
            result = parser.parse(template_contents=template_contents)
            # ensure the response returned to the controller
            # contains only native types, nothing unique to the parser
            result = json.loads(json.dumps(result))
        except Exception as exc:
            raise AnsibleActionFail(
                "Unhandled exception from parser '{parser}'. Error: {err}".format(
                    parser=self._parser_name, err=to_native(exc)
                )
            )

        if result.get("errors"):
            self._prune_result()
            self._result.update(
                {"failed": True, "msg": " ".join(result["errors"])}
            )
        else:
            self._result["parsed"] = result["parsed"]
            set_fact = self._task.args.get("set_fact")
            if set_fact:
                self._result["ansible_facts"] = {set_fact: result["parsed"]}
        return self._result
