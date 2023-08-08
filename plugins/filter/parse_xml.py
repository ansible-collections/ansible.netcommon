#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The parse_xml filter plugin
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
name: parse_xml
author: Ansible Network Community (@ansible-network)
version_added: "5.1.0"
short_description: parse_xml filter plugin.
description:
    - The filter plugin extends vlans when data.
    - Using the parameters below - C(xml_data | ansible.netcommon.parse_xml(template.yml))
notes:
  - The filter plugin extends vlans when data provided in range or comma separated.
options:
  data:
    description:
    - This source xml on which parse_xml invokes.
    - For example C(xml_data | ansible.netcommon.parse_xml),
      in this case C(xml_data) represents this option.
    type: raw
    required: True
  template:
    description:
    - The template to compare it with.
    - For example C(xml_data | ansible.netcommon.parse_xml(template.yml)),
      in this case C(xml_data) represents this option.
    type: raw
"""

EXAMPLES = r"""
# Using parse_xml

# example_output.xml

# <data>
# 	<ntp>
# 		<nodes>
# 			<node>
# 				<node>0/0/CPU0</node>
# 				<associations>
# 					<is-ntp-enabled>true</is-ntp-enabled>
# 					<sys-leap>ntp-leap-no-warning</sys-leap>
# 					<peer-summary-info>
# 						<peer-info-common>
# 							<host-mode>ntp-mode-client</host-mode>
# 							<is-configured>true</is-configured>
# 							<address>10.1.1.1</address>
# 							<reachability>0</reachability>
# 						</peer-info-common>
# 						<time-since>-1</time-since>
# 					</peer-summary-info>
# 					<peer-summary-info>
# 						<peer-info-common>
# 							<host-mode>ntp-mode-client</host-mode>
# 							<is-configured>true</is-configured>
# 							<address>172.16.252.29</address>
# 							<reachability>255</reachability>
# 						</peer-info-common>
# 						<time-since>991</time-since>
# 					</peer-summary-info>
# 				</associations>
# 			</node>
# 		</nodes>
# 	</ntp>
# </data>

# parse_xml.yml

# ---
# vars:
#   ntp_peers:
#     address: "{{ item.address }}"
# keys:
#   result:
#     value: "{{ ntp_peers }}"
#     top: "{http://cisco.com/ns/yang/Cisco-IOS-XR-ip-ntp-oper}ntp/"
#     items:
#       address: "{http://cisco.com/ns/yang/Cisco-IOS-XR-ip-ntp-oper}node"

- name: Facts setup
  ansible.builtin.set_fact:
    xml: "{{ lookup('file', 'example_output.xml') }}"

- name: Parse xml invocation
  ansible.builtin.debug:
    msg: "{{ xml | ansible.netcommon.parse_xml('parse_xml.yml') }}"


# Task Output
# -----------
#
# TODO
"""

from ansible.errors import AnsibleFilterError
from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
    AnsibleArgSpecValidator,
)

from ansible_collections.ansible.netcommon.plugins.plugin_utils.parse_xml import parse_xml


try:
    from jinja2.filters import pass_environment
except ImportError:
    from jinja2.filters import environmentfilter as pass_environment


@pass_environment
def _parse_xml(*args, **kwargs):
    """Extend vlan data"""

    keys = ["data", "template"]
    data = dict(zip(keys, args[1:]))
    data.update(kwargs)
    aav = AnsibleArgSpecValidator(data=data, schema=DOCUMENTATION, name="parse_xml")
    valid, errors, updated_data = aav.validate()
    if not valid:
        raise AnsibleFilterError(errors)
    return parse_xml(**updated_data)


class FilterModule(object):
    """parse_xml"""

    def filters(self):
        """a mapping of filter names to functions"""
        return {"parse_xml": _parse_xml}
