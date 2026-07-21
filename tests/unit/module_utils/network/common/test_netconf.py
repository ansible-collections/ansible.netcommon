# -*- coding: utf-8 -*-
#
# (c) 2017 Red Hat, Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import pytest

from ansible.module_utils.common.text.converters import to_bytes
from lxml.etree import XMLParser, XMLSyntaxError, fromstring


TEN_MB = 10 * 1024 * 1024


def _build_huge_xml(size):
    f"""
    Build an XML string with a single text node of the given size: {size}
    """

    return f"<data>{'A'*size}</data>"


def test_fromstring_succeeds_with_huge_tree_parser():
    """Verify that the same payload parses fine when huge_tree=True."""
    huge_xml = _build_huge_xml(TEN_MB + 1)
    parser = XMLParser(huge_tree=True)
    result = fromstring(to_bytes(huge_xml), parser=parser)
    assert result.tag == "data"
    assert len(result.text) > TEN_MB


def test_fromstring_fails_on_huge_text_node():
    """Reproduce: lxml.etree.fromstring() rejects text nodes > 10MB
    without huge_tree=True.

    This mirrors what happens inside NetconfConnection.__rpc__() when
    the NETCONF device returns a response with a very large text node.
    """
    huge_xml = _build_huge_xml(TEN_MB + 1)

    with pytest.raises(
        XMLSyntaxError, match="Resource limit exceeded: Text node too long, try XML_PARSE_HUGE"
    ):
        fromstring(to_bytes(huge_xml))
