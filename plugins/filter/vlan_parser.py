#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The vlan_parser filter plugin
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
name: vlan_parser
author: Ansible Network Community (@ansible-network)
version_added: "5.1.0"
short_description: vlan_parser filter plugin.
description:
    - The filter plugin extends vlans when data.
    - Using the parameters below - C(vlans_data | ansible.netcommon.vlan_parser)
notes:
  - The filter plugin extends vlans when data provided in range or comma separated.
options:
  data:
    description:
    - This option represents a string containing the range of vlans.
    - For example C(vlans_data | ansible.netcommon.vlan_parser),
      in this case C(vlans_data) represents this option.
    type: list
    required: True
  first_line_len:
    description:
    - The first line of the list can be first_line_len characters long.
    - For example C(vlans_data | ansible.netcommon.vlan_parser),
      in this case C(vlans_data) represents this option.
    type: int
    default: 48
  other_line_len:
    description:
    - The subsequent list lines can be other_line_len characters.
    - For example C(vlans_data | ansible.netcommon.vlan_parser),
      in this case C(vlans_data) represents this option.
    type: int
    default: 44
"""

EXAMPLES = r"""
# Using vlan_parser

- name: Setting host facts for vlan_parser filter plugin
  ansible.builtin.set_fact:
    vlan_ranges:
      [
        100,
        1688,
        3002,
        3003,
        3004,
        3005,
        3102,
        3103,
        3104,
        3105,
        3802,
        3900,
        3998,
        3999,
      ]

- name: Invoke vlan_parser filter plugin
  ansible.builtin.set_fact:
    extended_vlans: "{{ vlan_ranges | ansible.netcommon.vlan_parser(first_line_len = 20, other_line_len=20)  }}"


# Task Output
# -----------
#
# TASK [Setting host facts for vlan_parser filter plugin]
# ok: [host] => changed=false
#   ansible_facts:
#     vlan_ranges:
#     - 100
#     - 1688
#     - 3002
#     - 3003
#     - 3004
#     - 3005
#     - 3102
#     - 3103
#     - 3104
#     - 3105
#     - 3802
#     - 3900
#     - 3998
#     - 3999
#     vlan_rangesx: 1,10-12,15,20-22

# TASK [Invoke vlan_parser filter plugin]
# ok: [host] => changed=false
#   ansible_facts:
#     clean_acls:
#     - 100,1688,3002-3005
#     - 3102-3105,3802,3900
#     - 3998,3999
"""

from ansible.errors import AnsibleFilterError
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

from ansible_collections.ansible.netcommon.plugins.plugin_utils.vlan_parser import vlan_parser


try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment


@pass_environment
def _vlan_parser(*args, **kwargs):
    """Extend vlan data"""

    keys = ["data", "first_line_len", "other_line_len"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="vlan_parser")
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return vlan_parser(**updated_data)


class FilterModule(object):
    """vlan_parser"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"vlan_parser": _vlan_parser}
