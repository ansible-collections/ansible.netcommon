"""
xml parser

This is the xml parser for use with the cli_parse module and action plugin
https://github.com/martinblech/xmltodict
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
    import xmltodict

    HAS_XMLTODICT = True
except ImportError:
    HAS_XMLTODICT = False


class CliParser(CliParserBase):  # pylint: disable=too-few-public-methods
    """ The textfsm parser class
    Convert an xml string to structured data using xmltodict
    """

    DEFAULT_TEMPLATE_EXTENSION = None
    PROVIDE_TEMPLATE_CONTENTS = False

    @staticmethod
    def _check_reqs():
        """ Check the prequisites for the xml parser
        """
        errors = []
        if not HAS_XMLTODICT:
            msg = (
                "The XML parser requires xmltodict be installed "
                "on the control node. (e.g. 'pip install xmltodict')"
            )
            errors.append(msg)
        return errors

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
        errors = self._check_reqs()
        if errors:
            return {"errors": errors}

        cli_output = self._task_args.get("text")

        network_os = self._task_args.get("parser").get(
            "os"
        ) or self._task_vars.get("ansible_network_os")
        # the nxos | xml includes a odd garbage line at the end, so remove it
        if "nxos" in network_os:
            splitted = cli_output.splitlines()
            if splitted[-1] == "]]>]]>":
                cli_output = "\n".join(splitted[:-1])

        try:
            parsed = xmltodict.parse(cli_output)
            return {"parsed": parsed}
        except Exception as exc:  # pylint: disable=broad-except
            msg = "XML parser returned an error while parsing. Error: {err}"
            return {"errors": [msg.format(err=to_native(exc))]}
