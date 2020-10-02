# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
The index_of lookup plugin
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
    lookup: index_of
    author: Bradley Thornton (@cidrblock)
    version_added: "1.4"
    short_description: Find the indicies of items in a list matching some criteria
    description:
        - This lookup returns a list of indicies of items matching some criteria in a list.
        - C(index_of) is also available as a C(filter_plugin) for convenience
    options:
      _terms:
        description: The values below provided in the order C(test), C(value), C(key).
        required: True
      data:
        description: A list of items to enumerate and test against
        type: list
        required: True
      test:
        description: >
            The name of the test to run against the list, a valid jinja2 test or ansible test plugin.
            Jinja2 includes the following tests U(http://jinja.palletsprojects.com/templates/#builtin-tests).
            An overview of tests included in ansible U(https://docs.ansible.com/ansible/latest/user_guide/playbooks_tests.html)
        type: str
        required: True
      value:
        description: >
            The value used to test each list item against
            Not required for simple tests (eg: C(true), C(false), C(even), C(odd))
            May be a C(string), C(boolean), C(number), C(regular expesion) C(dict) etc, depending on the C(test) used
        type: raw
      key:
        description: >
            When the data provided is a list of dictionaries, run the test againt this dictionary key
            When using a C(key), the C(data) must only contain dictionaries
            See C(fail_on_missing) below to determine the behaviour when the C(key) is missing from a dictionary in the C(data)
        type: str
      fail_on_missing:
        description: When provided a list of dictionaries, fail if the key is missing from one or more of the dictionaries
        type: bool
      wantlist:
        description: >
            When only a single entry in the C(data) is matched, that entries index is returned as an integer
            If set to C(True), the return value will always be a list, even if only a single entry is matched
            This can also be accomplised using C(query) or C(q) instead of C(lookup)
            U(https://docs.ansible.com/ansible/latest/plugins/lookup.html)
        type: bool

    notes:
"""

EXAMPLES = r"""

#### Simple examples using a list of values

- set_fact:
    data:
    - 1
    - 2
    - 3

- name: Find the index of 2, lookup or filter
  set_fact:
    as_lookup: "{{ lookup('ansible.netcommon.index_of', data, 'eq', 2) }}"
    as_filter: "{{ data|ansible.netcommon.index_of('eq', 2) }}"

# TASK [Find the index of 2, lookup or filter] *******************************
# ok: [sw01] => changed=false
#   ansible_facts:
#     as_filter: '1'
#     as_lookup: '1'

- name: Any test can be negated using not or !
  set_fact:
    as_lookup: "{{ lookup('ansible.netcommon.index_of', data, 'not in', [1,2]) }}"
    as_filter: "{{ data|ansible.netcommon.index_of('!in', [1,2]) }}"

# TASK [Any test can be negated using not or !] ******************************
# ok: [localhost] => changed=false
#   ansible_facts:
#     as_filter: '2'
#     as_lookup: '2'

- name: Find the index of 2, lookup or filter, ensure list is returned
  set_fact:
    as_query: "{{ query('ansible.netcommon.index_of', data, 'eq', 2) }}"
    as_lookup: "{{ lookup('ansible.netcommon.index_of', data, 'eq', 2, wantlist=True) }}"
    as_filter: "{{ data|ansible.netcommon.index_of('eq', 2, wantlist=True) }}"

# TASK [Find the index of 2, lookup or filter, ensure list is returned] ******
# ok: [sw01] => changed=false
#   ansible_facts:
#     as_filter:
#     - 1
#     as_lookup:
#     - 1
#     as_query:
#     - 1

- name: Find the index of 3 using the long format
  set_fact:
    as_query: "{{ query('ansible.netcommon.index_of', data=data, test='eq', value=value) }}"
    as_lookup: "{{ lookup('ansible.netcommon.index_of', data=data, test='eq',value =value, wantlist=True) }}"
    as_filter: "{{ data|ansible.netcommon.index_of(test='eq', value=value, wantlist=True) }}"
  vars:
    value: 3

# TASK [Find the index of 3 using the long format] ***************************
# ok: [sw01] => changed=false
#   ansible_facts:
#     as_filter:
#     - 2
#     as_lookup:
#     - 2
#     as_query:
#     - 2

- name: Find numbers greater than 1, using loop
  debug:
    msg: "{{ data[item] }} is {{ test }} than {{ value }}"
  loop: "{{ data|ansible.netcommon.index_of(test, value) }}"
  vars:
    test: '>'
    value: 1

# TASK [Find numbers great than 1, using loop] *******************************
# ok: [sw01] => (item=1) =>
#   msg: 2 is > than 1
# ok: [sw01] => (item=2) =>
#   msg: 3 is > than 1

- name: Find numbers greater than 1, using with
  debug:
    msg: "{{ data[item] }} is {{ params.test }} than {{ params.value }}"
  with_ansible.netcommon.index_of: "{{ params }}"
  vars:
    params:
      data: "{{ data }}"
      test: '>'
      value: 1

# TASK [Find numbers greater than 1, using with] *****************************
# ok: [sw01] => (item=1) =>
#   msg: 2 is > than 1
# ok: [sw01] => (item=2) =>
#   msg: 3 is > than 1



#### Working with lists of dictionaries

- set_fact:
    data:
    - name: sw01.example.lan
      type: switch
    - name: rtr01.example.lan
      type: router
    - name: fw01.example.corp
      type: firewall
    - name: fw02.example.corp
      type: firewall

- name: Find the index of all firewalls using the type key
  set_fact:
    as_query: "{{ query('ansible.netcommon.index_of', data, 'eq', 'firewall', 'type') }}"
    as_lookup: "{{ lookup('ansible.netcommon.index_of', data, 'eq', 'firewall', 'type') }}"
    as_filter: "{{ data|ansible.netcommon.index_of('eq', 'firewall', 'type') }}"

# TASK [Find the index of all firewalls using the type key] ******************
# ok: [sw01] => changed=false
#   ansible_facts:
#     as_filter:
#     - 2
#     - 3
#     as_lookup:
#     - 2
#     - 3
#     as_query:
#     - 2
#     - 3

- name: Find the index of all firewalls, use in a loop, as a filter
  debug:
    msg: "The type of {{ device_type }} at index {{ item }} has name {{ data[item].name }}."
  loop: "{{ data|ansible.netcommon.index_of('eq', device_type, 'type') }}"
  vars:
    device_type: firewall

# TASK [Find the index of all firewalls, use in a loop] **********************
# ok: [sw01] => (item=2) =>
#   msg: The type of firewall at index 2 has name fw01.
# ok: [sw01] => (item=3) =>
#   msg: The type of firewall at index 3 has name fw02.

- name: Find the index of all devices with a .corp name, as a lookup
  debug:
    msg: "The device named {{ data[item].name }} is a {{ data[item].type }}"
  loop: "{{ lookup('ansible.netcommon.index_of', data, 'regex', regex, 'name') }}"
  vars:
    regex: '\.corp$' # ends with .corp

# TASK [Find the index of all devices with a .corp name, as a lookup] **********
# ok: [sw01] => (item=2) =>
#   msg: The device named fw01.example.corp is a firewall
# ok: [sw01] => (item=3) =>
#   msg: The device named fw02.example.corp is a firewall



#### Working with data from resource modules

- name: Retrieve the current L3 interface configuration
  cisco.nxos.nxos_l3_interfaces:
    state: gathered
  register: current_l3

# TASK [Retrieve the current L3 interface configuration] *********************
# ok: [sw01] => changed=false
#   gathered:
#   - name: Ethernet1/1
#   - name: Ethernet1/2
#   <...>
#   - name: Ethernet1/128
#   - ipv4:
#     - address: 192.168.101.14/24
#     name: mgmt0

- name: Find the index of the interface and address with a 192.168.101.xx ip address
  set_fact:
    found: "{{ found + entry }}"
  with_indexed_items: "{{ current_l3.gathered }}"
  vars:
    found: []
    ip: '192.168.101.'
    address: "{{ item.1.ipv4|d([])|ansible.netcommon.index_of('search', ip, 'address', wantlist=True) }}"
    entry:
    - interface_idx: "{{ item.0 }}"
    address_idxs: "{{ address }}"
  when: address

# TASK [debug] ***************************************************************
# ok: [sw01] =>
#   found:
#   - address_idxs:
#     - 0
#     interface_idx: '128'

- name: Show all interfaces and their address
  debug:
    msg: "{{ interface.name }} has ip {{ address }}"
  loop: "{{ found|subelements('address_idxs') }}"
  vars:
    interface: "{{ current_l3.gathered[item.0.interface_idx|int] }}"
    address: "{{ interface.ipv4[item.1].address }}"

# TASK [debug] ***************************************************************
# ok: [sw01] => (item=[{'interface_idx': '128', 'address_idx': [0]}, 0]) =>
#   msg: mgmt0 has ip 192.168.101.14/24



#### Working with complex structures

- set_fact:
    data:
      interfaces:
        interface:
        - config:
            description: configured by Ansible - 1
            enabled: True
            loopback-mode: False
            mtu: 1024
            name: loopback0000
            type: eth
          name: loopback0000
          subinterfaces:
            subinterface:
            - config:
                description: subinterface configured by Ansible - 1
                enabled: True
                index: 5
              index: 5
            - config:
                description: subinterface configured by Ansible - 2
                enabled: False
                index: 2
              index: 2
        - config:
            description: configured by Ansible - 2
            enabled: False
            loopback-mode: False
            mtu: 2048
            name: loopback1111
            type: virt
          name: loopback1111
          subinterfaces:
            subinterface:
            - config:
                description: subinterface configured by Ansible - 3
                enabled: True
                index: 10
              index: 10
            - config:
                description: subinterface configured by Ansible - 4
                enabled: False
                index: 3
              index: 3


- name: Find the description of loopback111, subinterface index 10
  debug:
    msg: |-
      {{ data.interfaces.interface[int_idx|int]
           .subinterfaces.subinterface[subint_idx|int]
             .config.description }}
  vars:
    # the values to search for
    int_name: loopback1111
    sub_index: 10
    # retrieve the index in each nested list
    int_idx: |
      {{ data.interfaces.interface|
           ansible.netcommon.index_of('eq', int_name, 'name') }}
    subint_idx: |
      {{ data.interfaces.interface[int_idx|int]
           .subinterfaces.subinterface|
             ansible.netcommon.index_of('eq', sub_index, 'index') }}

# TASK [Find the description of loopback111, subinterface index 10] ************
# ok: [sw01] =>
#   msg: subinterface configured by Ansible - 3



"""

RETURN = """
  _raw:
    description:
      - One or more zero-based indicies of the matching list items
      - See C(wantlist) if a list is always required
"""

from ansible.plugins.lookup import LookupBase
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.index_of import (
    index_of,
)


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):
        if isinstance(terms, dict):
            terms.update(kwargs)
            res = index_of(**terms)
        else:
            res = index_of(*terms, **kwargs)
        if not isinstance(res, list):
            return [res]
        return res
