#
# Copyright 2020 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: update_fact
short_description: Update currently set facts
version_added: "1.3"
description:
    - This module allows updating existing variables.
    - Variables are updated on a host-by-host basis.
    - Variable are not modified in place, instead they are returned by the module
options:
  updates:
    description:
      - A list of dictionaries, each a desired update to make
    type: list
    elements: dict
    required: True
    suboptions:
      path:
        description:
        - The path in a currently set variable to update
        - The path can be in dot or bracket notation
        - It should be a valid jinja reference
        type: str
        required: True
      value:
        description:
        - The value to be set at the path
        - Can be a simple or complex data structure
        type: raw
        required: True


notes:

author:
- Bradley Thornton (@cidrblock)
"""

<<<<<<< HEAD
EXAMPLES = r"""

# Update an exisitng fact, dot or bracket notation
=======
RETURN = """
object:
    description: Each modified object is returned
diff:
  description: If --diff option in enabled while running, the changes are
               returned as part of before and after key.
  returned: when diff is enabled
  type: dict
"""
EXAMPLES = r"""

# Update an exisitng fact, dot or bracket notation, run with --diff
>>>>>>> 2f130c3d3342f29e8d38d99797688918f7ca819f
- name: Set a fact
  set_fact:
    a:
      b:
        c:
        - 1
        - 2

- name: Update the fact
  ansible.netcommon.update_fact:
    updates:
    - path: a.b.c.0
      value: 10
    - path: "a['b']['c'][1]"
      value: 20
  register: updated

- debug:
    var: updated.a

# updated:
#   a:
#     b:
#       c:
#       - 10
#       - 20
#   changed: true


# Lists can be appended, new keys added to dictionaries

- name: Set a fact
  set_fact:
    a:
      b:
        b1:
        - 1
        - 2

- name: Update, add to list, add new key
  ansible.netcommon.update_fact:
    updates:
    - path: a.b.b1.2
      value: 3
    - path: a.b.b2
      value:
      - 10
      - 20
      - 30
  register: updated

- debug:
    var: updated.a

# updated:
#   a:
#     b:
#       b1:
#       - 1
#       - 2
#       - 3
#       b2:
#       - 10
#       - 20
#       - 30
#   changed: true

# Update every item in a list of dictionaries
# build the update list ahead of time using a loop
# and then apply the changes to the fact

- name: Set fact
  set_fact:
    addresses:
    - raw: 10.1.1.0/255.255.255.0
      name: servers
    - raw: 192.168.1.0/255.255.255.0
      name: printers
    - raw: 8.8.8.8
      name: dns

- name: Build a list of updates
  set_fact:
    update_list: "{{ update_list + update }}"
  loop: "{{ addresses }}"
  loop_control:
    index_var: idx
  vars:
    update_list: []
    update:
    - path: addresses[{{ idx }}].network
      value: "{{ item['raw'] | ansible.netcommon.ipaddr('network') }}"
    - path: addresses[{{ idx }}].prefix
      value: "{{ item['raw'] | ansible.netcommon.ipaddr('prefix') }}"

- debug:
    var: update_list

# TASK [debug] *******************
# ok: [localhost] =>
#   update_list:
#   - path: addresses[0].network
#     value: 10.1.1.0
#   - path: addresses[0].prefix
#     value: '24'
#   - path: addresses[1].network
#     value: 192.168.1.0
#   - path: addresses[1].prefix
#     value: '24'
#   - path: addresses[2].network
#     value: 8.8.8.8
#   - path: addresses[2].prefix
#     value: '32'

- name: Make the updates
  ansible.netcommon.update_fact:
    updates: "{{ update_list }}"
  register: updated

- debug:
    var: updated

# TASK [debug] ***********************
# ok: [localhost] =>
#   updated:
#     addresses:
#     - name: servers
#       network: 10.1.1.0
#       prefix: '24'
#       raw: 10.1.1.0/255.255.255.0
#     - name: printers
#       network: 192.168.1.0
#       prefix: '24'
#       raw: 192.168.1.0/255.255.255.0
#     - name: dns
#       network: 8.8.8.8
#       prefix: '32'
#       raw: 8.8.8.8
#     changed: true
#     failed: false

# Retrieve, update, and apply interface description change

- name: Get the current interface config
  cisco.nxos.nxos_interfaces:
    state: gathered
  register: current

- name: Rekey the interface list using the interface name
  set_fact:
    current: "{{ current['gathered']|rekey_on_member('name') }}"

- name: Update the description of Ethernet1/1
  ansible.netcommon.update_fact:
    updates:
    - path: current.Ethernet1/1.description
      value: "Configured by ansible"
  register: updated

- name: Update the configuration
  cisco.nxos.nxos_interfaces:
    config: "{{ updated.current.values()|list }}"
    state: overridden
  register: result

- name: Show the commands issued
  debug:
    msg: "{{ result['commands'] }}"

# TASK [Show the commands issued] *********
# ok: [sw01] =>
#   msg:
#   - interface Ethernet1/1
#   - description Configured by ansible


# Retrieve, update, and apply an ipv4 ACL change

- name: Retrieve the current acls
  arista.eos.eos_acls:
    state: gathered
  register: current

- name: Retrieve the index of the ipv4 acls
  set_fact:
    afi_index: "{{ idx }}"
  loop: "{{ current.gathered }}"
  loop_control:
    index_var: idx
  when: item.afi == 'ipv4'

- name: Retrieve the index of the test1 acl
  set_fact:
    acl_index: "{{ idx }}"
  loop: "{{ current.gathered[afi_index].acls }}"
  loop_control:
    index_var: idx
  when: item.name == 'test1'

- name: Retrieve the index of sequence 10
  set_fact:
    ace_index: "{{ idx }}"
  loop: "{{ current.gathered[afi_index].acls[acl_index].aces }}"
  loop_control:
    index_var: idx
  when: item.sequence == 10

- name: Update the fact
  ansible.netcommon.update_fact:
    updates:
    - path: current.gathered[{{ afi_index }}].acls[{{ acl_index }}].aces[{{ ace_index }}].source
      value:
        subnet_address: "192.168.1.0/24"
  register: updated

- name: Apply the changes
  arista.eos.eos_acls:
    config: "{{ updated.current.gathered }}"
    state: overridden
  register: changes

- name: Show the commands issued
  debug:
    var: changes.commands

# TASK [Show the commands issued] ***************
# ok: [eos101] =>
#   changes.commands:
#   - ip access-list test1
#   - no 10
#   - ip access-list test1
#   - 10 permit ip 192.168.20.0/24 host 10.1.1.2


# Disable ip redirects on any layer3 interface

- name: Get the current interface config
  cisco.nxos.nxos_facts:
    gather_network_resources:
    - interfaces
    - l3_interfaces

- name: Rekey the l3 interface lists using the interface name
  set_fact:
    l3_interfaces: "{{ ansible_network_resources['l3_interfaces']|rekey_on_member('name') }}"

- name: Build the update list for any layer3 interface
  set_fact:
    update_list: "{{ update_list + update }}"
  loop: "{{ ansible_network_resources['interfaces'] }}"
  vars:
    update:
    - path: "l3_interfaces[{{ item['name'] }}]['redirects']"
      value: False
    update_list: []
  when: item['mode']|default() == 'layer3'

# TASK [debug] **************************************
# ok: [nxos101] =>
#   update_list:
#   - path: l3_interfaces[Ethernet1/10]['redirects']
#     value: false
#   - path: l3_interfaces[Ethernet1/11]['redirects']
#     value: false

- name: Apply the fact updates
  ansible.netcommon.update_fact:
    updates: "{{ update_list }}"
  register: updated

- name: Update the configuration
  cisco.nxos.nxos_l3_interfaces:
    config: "{{ updated.l3_interfaces.values()|list }}"
    state: overridden
  register: result
  when: updated['changed']

- name: Show the commands issued
  debug:
    msg: "{{ result['commands'] }}"
  when: updated['changed']

# TASK [Show the commands issued] *******
# ok: [sw01] =>
#   msg:
#   - interface Ethernet1/10
#   - no ip redirects
#   - interface Ethernet1/11
#   - no ip redirects

"""
