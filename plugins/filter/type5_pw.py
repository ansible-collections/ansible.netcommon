#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The type5_pw filter plugin
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
name: type5_pw
author: Ansible Network Community (@ansible-network)
version_added: "5.1.0"
short_description: type5_pw filter plugin.
description:
    - The filter plugin extends vlans when data.
    - Using the parameters below - C(xml_data | ansible.netcommon.type5_pw(template.yml))
notes:
  - The filter plugin extends vlans when data provided in range or comma separated.
options:
  password:
    description:
    - This source xml on which type5_pw invokes.
    - For example C(xml_data | ansible.netcommon.type5_pw),
      in this case C(xml_data) represents this option.
    type: str
    required: True
  salt:
    description:
    - The template to compare it with.
    - For example C(xml_data | ansible.netcommon.type5_pw(template.yml)),
      in this case C(xml_data) represents this option.
    type: str
"""

EXAMPLES = r"""
# Using type5_pw

- name: The facts
  ansible.builtin.set_fact:
    password: "cisco@123"

- name: Filter type5_pw invocation
  ansible.builtin.debug:
    msg: "{{ password | ansible.netcommon.type5_pw(salt='avs') }}"


# Task Output
# -----------
#
# TASK [The facts]
# ok: [host] => changed=false
#   ansible_facts:
#     password: cisco@123

# TASK [Filter type5_pw invocation]
# ok: [host] =>
#   msg: $1$avs$uSTOEMh65qzvpb9yBMpzd/
"""

from ansible.errors import AnsibleFilterError
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

from ansible_collections.ansible.netcommon.plugins.plugin_utils.type5_pw import type5_pw


try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment


@pass_environment
def _type5_pw(*args, **kwargs):
    """Extend vlan data"""

    keys = ["password", "salt"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="type5_pw")
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return type5_pw(**updated_data)


class FilterModule(object):
    """type5_pw"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"type5_pw": _type5_pw}
