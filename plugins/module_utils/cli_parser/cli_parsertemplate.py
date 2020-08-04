""" A shim class for the NetworkTemplate
this was done in case there is a need to
modify the resource module parser class
or extend it a split it from the cli parsers.
"""
from __future__ import absolute_import, division, print_function

# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name

# pylint: disable=import-error, line-too-long
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)

# pylint: disable=import-error, line-too-long


class CliParserTemplate(
    NetworkTemplate
):  # pylint: disable=too-few-public-methods
    """ The parser template base class
    """

    def __init__(self, lines=None):
        super(CliParserTemplate, self).__init__(lines=lines, tmplt=self)
