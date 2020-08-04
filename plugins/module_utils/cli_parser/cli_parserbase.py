"""
The base class for cli_parsers
"""
from __future__ import absolute_import, division, print_function

# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name


class CliParserBase:  # pylint: disable=too-few-public-methods
    """ The base class for cli parsers
    Provides a  _debug function to normalize parser debug output
    """

    def __init__(self, task_args, task_vars, debug):
        self._debug = debug
        self._task_args = task_args
        self._task_vars = task_vars
