"""
native parser

This is the native parser for use with the cli_parse module and action plugin.
The parser functionality used by the network resource modules is leveraged here.

"""
from __future__ import absolute_import, division, print_function

# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

from ansible.module_utils._text import to_native

# pylint: disable=relative-beyond-top-level
from ..module_utils.cli_parser.cli_parserbase import CliParserBase
from ..module_utils.cli_parser.cli_parsertemplate import CliParserTemplate

# pylint: enable=relative-beyond-top-level

try:
    import yaml

    try:
        from yaml import CSafeLoader as SafeLoader
    except ImportError:
        from yaml import SafeLoader
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class CliParser(CliParserBase):  # pylint: disable=too-few-public-methods
    """ The natvie parser class
    Convert raw text to structured data using the resource module parser
    """

    DEFAULT_TEMPLATE_EXTENSION = "yaml"
    PROVIDE_TEMPLATE_CONTENTS = True

    def parse(self, *_args, **kwargs):
        """ Std entry point for a cli_parse parse execution

        :return: Errors or parsed text as structured data
        :rtype: dict

        :example:

        The parse function of a parser should return a dict:
        {"errors": [a list of errors]}
        or
        {"parsed": obj}
        """
        # res = self._check_reqs()
        # if res.get("errors"):
        #     return res

        template_contents = kwargs["template_contents"]
        parser = CliParserTemplate(
            lines=self._task_args.get("text").splitlines()
        )
        try:
            template_obj = yaml.load(template_contents, SafeLoader)
        except Exception as exc:  # pylint: disable=broad-except
            print("here")
            return {"errors": [to_native(exc)]}

        try:
            parser.PARSERS = template_obj
            return {"parsed": parser.parse()}
        except Exception as exc:  # pylint: disable=broad-except
            msg = "Native parser returned an error while parsing. Error: {err}"
            return {"errors": [msg.format(err=to_native(exc))]}
