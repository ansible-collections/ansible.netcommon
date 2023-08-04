#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The vlan_expander filter plugin
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
name: vlan_expander
author: Ansible Network Community (@ansible-network)
version_added: "5.1.0"
short_description: vlan_expander filter plugin.
description:
    - The filter plugin extends vlans when data.
    - Using the parameters below - C(vlans_data | ansible.netcommon.vlan_expander)
notes:
  - The filter plugin extends vlans when data provided in range or comma separated.
options:
  data:
    description:
    - This option represents a string containing the range of vlans.
    - For example C(vlans_data | ansible.netcommon.vlan_expander),
      in this case C(vlans_data) represents this option.
    type: raw
    required: True
"""

EXAMPLES = r"""
# Using vlan_expander

- name: Setting host facts for vlan_expander filter plugin
  ansible.builtin.set_fact:
    vlan_ranges: "1,10-12,15,20-22"

- name: Invoke vlan_expander filter plugin
  ansible.builtin.set_fact:
    extended_vlans: "{{ vlan_ranges | ansible.netcommon.vlan_expander }}"


# Task Output
# -----------
#
# TASK [Setting host facts for vlan_expander filter plugin]
# ok: [host] => changed=false
#   ansible_facts:
#     vlan_ranges: 1,10-12,15,20-22

# TASK [Invoke vlan_expander filter plugin]
# ok: [host] => changed=false
#   ansible_facts:
#     extended_vlans:
#     - 1
#     - 10
#     - 11
#     - 12
#     - 15
#     - 20
#     - 21
#     - 22
"""

from ansible.errors import AnsibleFilterError
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

from ansible_collections.ansible.netcommon.plugins.plugin_utils.vlan_expander import vlan_expander


try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment


@pass_environment
def _vlan_expander(*args, **kwargs):
    """Extend vlan data"""

    keys = ["data"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="vlan_expander")
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return vlan_expander(**updated_data)


class FilterModule(object):
    """vlan_expander"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"vlan_expander": _vlan_expander}