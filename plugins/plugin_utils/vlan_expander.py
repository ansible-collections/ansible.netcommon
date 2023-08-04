#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The vlan_expander plugin code
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

from ansible.errors import AnsibleFilterError


def _raise_error(msg):
    """Raise an error message, prepend with filter name
    :param msg: The message
    :type msg: str
    :raises: AnsibleError
    """
    error = "Error when using plugin 'vlan_expander': {msg}".format(msg=msg)
    raise AnsibleFilterError(error)


def vlan_expander(data):
    if "-" not in data:
        _raise_error("Input is not valid for vlan_expander")
    expanded_list = []
    for each in data.split(","):
        if "-" in each:
            f, t = map(int, each.split("-"))
            expanded_list.extend(range(f, t + 1))
        else:
            expanded_list.append(int(each))
    return sorted(expanded_list)
