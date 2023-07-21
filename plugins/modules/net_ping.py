#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type


DOCUMENTATION = """
module: net_ping
author: Jacob McGill (@jmcgill298)
short_description: Tests reachability using ping from a network device
description:
- Tests reachability using ping from network device to a remote destination.
version_added: 1.0.0
extends_documentation_fragment:
- ansible.netcommon.network_agnostic
options:
  count:
    description:
    - Number of packets to send.
    default: 5
  dest:
    description:
    - The IP Address or hostname (resolvable by switch) of the remote node.
    required: true
  source:
    description:
    - The source IP Address.
  state:
    description:
    - Determines if the expected result is success or fail.
    choices:
    - absent
    - present
    default: present
  vrf:
    description:
    - The VRF to use for forwarding.
    default: default
notes:
- For targets running Python, use the M(ansible.builtin.shell) module along with ping command instead.
"""


EXAMPLES = """
- name: Test reachability to 10.10.10.10 using default vrf
  ansible.netcommon.net_ping:
    dest: 10.10.10.10

- name: Test reachability to 10.20.20.20 using prod vrf
  ansible.netcommon.net_ping:
    dest: 10.20.20.20
    vrf: prod

- name: Test unreachability to 10.30.30.30 using default vrf
  ansible.netcommon.net_ping:
    dest: 10.30.30.30
    state: absent

- name: Test reachability to 10.40.40.40 using prod vrf and setting count and source
  ansible.netcommon.net_ping:
    dest: 10.40.40.40
    source: loopback0
    vrf: prod
    count: 20

- Note:
    - For targets running Python, use the M(ansible.builtin.shell) module along with ping command instead.
    - Example:
        name: ping
        shell: ping -c 1 <remote-ip>
"""

RETURN = r"""
commands:
  description: Show the command sent.
  returned: always
  type: list
  sample: ["ping vrf prod 10.40.40.40 count 20 source loopback0"]
packet_loss:
  description: Percentage of packets lost.
  returned: always
  type: str
  sample: "0%"
packets_rx:
  description: Packets successfully received.
  returned: always
  type: int
  sample: 20
packets_tx:
  description: Packets successfully transmitted.
  returned: always
  type: int
  sample: 20
rtt:
  description: Show RTT stats.
  returned: always
  type: dict
  sample: {"avg": 2, "max": 8, "min": 1}
"""
