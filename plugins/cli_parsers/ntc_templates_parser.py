"""
ntc_templates parser

This is the ntc_teamples parser for use with the cli_parse module and action plugin.
https://github.com/networktocode/ntc-templates

"""
from __future__ import absolute_import, division, print_function

# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

from ansible.module_utils._text import to_native

# pylint: disable=relative-beyond-top-level
from ..module_utils.cli_parser.cli_parserbase import CliParserBase

# pylint: enable=relative-beyond-top-level
try:
    import textfsm  # pylint: disable=unused-import

    HAS_TEXTFSM = True
except ImportError:
    HAS_TEXTFSM = False

try:
    from ntc_templates.parse import parse_output

    HAS_NTC = True
except ImportError:
    HAS_NTC = False


class CliParser(CliParserBase):  # pylint: disable=too-few-public-methods
    """ The ntc_templates parser class
    Convert raw text to structured data using textfsm and predefined templates in
    the ntc-templates python package
    """

    DEFAULT_TEMPLATE_EXTENSION = None
    PROVIDE_TEMPLATE_CONTENTS = False

    def _check_reqs(self):
        """ Check the prerequisites for the ntc template parser

        :return: A dict with errors or a network_os and command
        :rtype: dict
        """
        errors = []

        if not HAS_TEXTFSM:
            msg = (
                "The ntc_templates parser requires TextFSM be "
                "installed on the control node. (e.g. 'pip install textfsm')"
            )
            errors.append(msg)
        if not HAS_NTC:
            msg = (
                "The ntc_templates parser requires ntc_templates be "
                "installed on the control node. (e.g. 'pip install ntc_templates')"
            )
            errors.append(msg)
        network_os = self._task_args.get("parser").get("network_os")
        if network_os:
            self._debug("OS set to {os} using task args".format(os=network_os))
        if not network_os:
            ano = dict(
                zip(
                    ["vendor", "platform", "os"],
                    self._task_vars.get("ansible_network_os", "").split("."),
                )
            )
            network_os = "{vendor}_{os}".format(**ano)
            self._debug(
                "OS set to {os} using ansible_network_os".format(os=network_os)
            )
        if not network_os:
            errors.append(
                "Either 'parser/os' needs to be specified or 'ansible_network_os' set."
            )
        command = self._task_args.get("parser").get("command")
        if not command:
            errors.append("'command' needs to be specified.")

        if errors:
            return {"errors": errors}
        return {"network_os": network_os, "command": command}

    def parse(self, *_args, **_kwargs):
        """ Std entry point for a cli_parse parse execution

        :return: Errors or parsed text as structured data
        :rtype: dict

        :example:

        The parse function of a parser should return a dict:
        {"errors": [a list of errors]}
        or
        {"parsed": obj}
        """
        cli_output = self._task_args.get("text")
        res = self._check_reqs()
        if res.get("errors"):
            return {"errors": res.get("errors")}
        platform = res["network_os"]
        command = res["command"]
        try:
            parsed = parse_output(
                platform=platform, command=command, data=cli_output
            )
            return {"parsed": parsed}
        except Exception as exc:  # pylint: disable=broad-except
            return {"errors": [to_native(exc)]}
