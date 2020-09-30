# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
The index_of filter plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.index_of import (
    index_of,
)


def _index_of(*args, **kwargs):
    """ Find items in a list. L(See examples, https://github.com/ansible-collections/ansible.netcommon/blob/main/docs/ansible.netcommon.httpapi_connection.rst)
    """
    return index_of(*args, **kwargs)


class FilterModule(object):
    """ index_of  """

    def filters(self):
        """ a mapping of filter names to functions
        """
        return {"index_of": _index_of}
