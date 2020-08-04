"""
The action plugin file for cli_parse
"""
from __future__ import absolute_import, division, print_function

# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

from importlib import import_module
from ansible.module_utils._text import to_native, to_text
from ansible.plugins.action.normal import ActionModule as _ActionModule
from ansible.errors import AnsibleActionFail


class ActionModule(_ActionModule):
    """ action module
    """

    PARSER_CLS_NAME = "CliParser"

    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)
        self._playhost = None
        self._parser_name = None
        self._result = None
        self._task_vars = None

    def _debug(self, msg):
        """ Output text using ansible's display

        :param msg: The message
        :type msg: str
        """
        msg = "<{phost}> [cli_parse] {msg}".format(
            phost=self._playhost, msg=msg
        )
        self._display.vvvv(msg)

    def _load_parser(self, task_vars):
        """ Load a parser from the fs

        :param task_vars: The vars provided when the task was run
        :type task_vars: dict
        :return: An instance of class CliParser
        :rtype: CliParser
        """
        requested_parser = self._task.args.get("parser").get("name")
        cref = dict(
            zip(["corg", "cname", "plugin"], requested_parser.split("."))
        )
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
        except Exception as exc:  # pylint: disable=broad-except
            self._result["failed"] = True
            self._result["msg"] = "Error loading parser: {err}".format(
                err=to_native(exc)
            )
            return None

    def _set_parser_command(self):
        """ Set the /parser/command in the task args based on /command if needed
        """
        if self._task.args.get("command"):
            if not self._task.args.get("parser").get("command"):
                self._task.args.get("parser")["command"] = self._task.args.get(
                    "command"
                )

    def _set_text(self):
        """ Set the /text in the task_args based on the command run
        """
        if self._result.get("stdout"):
            self._task.args["text"] = self._result["stdout"]

    def _os_from_task_vars(self):
        """ Extract an os str from the task's vars

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
                            os=oper_sys
                        )
                    )
                else:
                    oper_sys = self._task_vars.get(hvar)
                    self._debug(
                        "OS set to {os}, using ansible_distribution".format(
                            os=oper_sys
                        )
                    )
        return oper_sys.lower()

    def _update_template_path(self, template_extension):
        """ Update the template_path in the task args
        If not provided, generate template name using os and command

        :param template_extention: The parser specific template extension
        :type template extension: str
        """
        if not self._task.args.get("parser").get("template_path"):
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
        """ Retrieve the contents of the parser template

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
        """ In the case of an error, remove stdout and stdout_lines
        this allows for easier visibility of the error message.
        In the case of an actual command error, it will be thrown
        in the module
        """
        self._result.pop("stdout", None)
        self._result.pop("stdout_lines", None)

    def run(self, tmp=None, task_vars=None):
        """ The std execution entry pt for an action plugin

        :param tmp: no longer used
        :type tmp: none
        :param task_vars: The vars provided when the task is run
        :type task_vars: dict
        :return: The results from the parser
        :rtype: dict
        """
        self._result = super(ActionModule, self).run(task_vars=task_vars)
        self._task_vars = task_vars
        self._playhost = task_vars.get("inventory_hostname")
        self._parser_name = self._task.args.get("parser").get("name")

        if self._result.get("failed"):
            return self._result

        self._set_parser_command()
        self._set_text()

        parser = self._load_parser(task_vars)
        if self._result.get("failed"):
            self._prune_result()
            return self._result

        # Not all parsers use a template
        try:
            if parser.DEFAULT_TEMPLATE_EXTENSION:
                self._update_template_path(parser.DEFAULT_TEMPLATE_EXTENSION)
        except AttributeError:
            pass

        # Not all parsers require the template contents
        template_contents = None
        try:
            if parser.PROVIDE_TEMPLATE_CONTENTS:
                template_contents = self._get_template_contents()
        except AttributeError:
            pass

        try:
            result = parser.parse(template_contents=template_contents)
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
