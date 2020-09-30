# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
The index_of filter plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.plugins.lookup import LookupBase

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.index_of import (
    index_of,
)


class FilterModule(object):
    """ index_of  """

    def filters(self):
        """ a mapping of filter names to functions
        """
        return {"index_of": index_of}
