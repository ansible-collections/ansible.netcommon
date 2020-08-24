# (c) 2020 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest
from ansible_collections.ansible.netcommon.tests.unit.compat import unittest
from ansible_collections.ansible.netcommon.plugins.cli_parsers.xml_parser import (
    CliParser,
)

xmltodict = pytest.importorskip("xmltodict")


class TestXmlParser(unittest.TestCase):
    def test_invalid_xml(self):
        task_args = {"text": "Definitely not XML", "parser": {"os": "none"}}
        parser = CliParser(task_args=task_args, task_vars=[], debug=False)

        result = parser.parse()
        self.assertEqual(result["errors"], 1)
