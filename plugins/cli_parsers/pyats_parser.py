"""
pyats parser

This is the payats parser for use with the cli_parse module and action plugin.
https://developer.cisco.com/docs/pyats/#!parsing-device-output

"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.six import PY3
from ansible.module_utils._text import to_native


from ..module_utils.cli_parser.cli_parserbase import CliParserBase


try:
    from genie.conf.base import Device
    from genie.libs.parser.utils import get_parser

    HAS_GENIE = True
except ImportError:
    HAS_GENIE = False

try:
    from pyats.datastructures import AttrDict

    HAS_PYATS = True
except ImportError:
    HAS_PYATS = False


class CliParser(CliParserBase):
    """ The pyats parser class
    Convert raw text to structured data using pyats/genie
    """

    DEFAULT_TEMPLATE_EXTENSION = None
    PROVIDE_TEMPLATE_CONTENTS = False

    @staticmethod
    def _check_reqs():
        """ Check the prerequistes are installed for pyats/genie

        :return dict: A dict with a list of errors
        """
        errors = []
        if not PY3:
            errors.append("Genie requires Python 3")
        if not HAS_GENIE:
            msg = (
                "The pyats parser requires Genie be installed "
                "on the control node. (e.g. 'pip install genie')"
            )
            errors.append(msg)
        if not HAS_PYATS:
            msg = (
                "The pyats parser requires pyATS be installed "
                "on the control node. (e.g. 'pip install pyats')"
            )
            errors.append(msg)
        return errors

    def _check_vars(self):
        """ Ensure specific args are set

        :return: A dict with a list of errors
        :rtype: dict
        """
        errors = []
        if not self._task_args.get("parser").get("command"):
            errors.append(
                "The pyats parser requires parser/command be provided."
            )
        return errors

    def _transform_ansible_network_os(self):
        """ Transform the anssible_network_os to a pyats OS
        The last part of the fully qualified name is used
        org.name.platform => platform

        In the case of ios, the os is assumed to be iosxs
        """
        ane = self._task_vars.get("ansible_network_os", "").split(".")[-1]
        if ane == "ios":
            self._debug("ansible_network_os was ios, using iosxe.")
            ane = "iosxe"
        self._debug(
            "OS set to '{ane}' using 'ansible_network_os'.".format(ane=ane)
        )
        return ane

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
        errors.extend(self._check_vars())
        if errors:
            return {"errors": errors}

        command = self._task_args.get("parser").get("command")
        network_os = (
            self._task_args.get("parser").get("os")
            or self._transform_ansible_network_os()
        )
        cli_output = self._task_args.get("text")

        device = Device("new_device", os=network_os)
        device.custom.setdefault("abstraction", {})["order"] = ["os"]
        device.cli = AttrDict({"execute": None})

        try:
            get_parser(command, device)
        except Exception as exc:
            msg = "Unable to find parser for command '{cmd}' for os '{os}'. Error: {err}."
            return {
                "errors": [
                    (
                        msg.format(
                            cmd=command, os=network_os, err=to_native(exc)
                        )
                    )
                ]
            }

        try:
            parsed = device.parse(command, output=cli_output)
        except Exception as exc:
            msg = (
                "Parser for '{cmd}' for {os} was found, "
                "but failed to parse the provided output. Error {err}."
            )
            return {
                "errors": [
                    (
                        msg.format(
                            cmd=command, os=network_os, err=to_native(exc)
                        )
                    )
                ]
            }
        return {"parsed": parsed}
