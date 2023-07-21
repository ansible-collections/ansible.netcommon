# -*- coding: utf-8 -*-
#
# (c) 2017 Red Hat, Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import re

import pytest

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import config


RUNNING = """interface Ethernet1
   speed auto
   no switchport
   no lldp receive
!
interface Ethernet2
   speed auto
   no switchport
   no lldp transmit
!
interface Management1
   ip address dhcp
!"""

WANT_SRC_1 = """
router ospfv3
   fips restrictions
   address-family ipv4
      fips restrictions
      redistribute connected
      exit
   address-family ipv6
      router-id 10.1.1.1
      exit
   exit
router ospfv3 vrf vrf01
   fips restrictions
   address-family ipv4
      passive-interface default
      exit
   address-family ipv6
      fips restrictions
      exit
   exit
router ospfv3 vrf vrf02
   fips restrictions
   address-family ipv6
      fips restrictions
      exit
   exit
"""

HAVE_SRC_1 = ""

WANT_SRC_2 = """
interface loopback0
 ip ospf 1 area 0.0.0.0
!
interface GigabitEthernet0/1
 ip ospf 1 area 0.0.0.0
interface GigabitEthernet0/2
 ip ospf 1 area 0.0.0.0
!
router isis fabric
 is-type level-2
 net 49.0000.0000.0003.00
!
interface loopback0
 ip router isis fabric
!
interface GigabitEthernet0/1
 ip router isis fabric
interface GigabitEthernet0/2
 ip router isis fabric
"""

HAVE_SRC_2 = """
interface GigabitEthernet0/1
interface GigabitEthernet0/2
"""

ORIGINAL_DEFAULT_IGNORE_LINES_RE = config.DEFAULT_IGNORE_LINES_RE.copy()


def test_config_items():
    net_config = config.NetworkConfig(indent=3, contents=RUNNING)
    assert len(net_config.items) == 10

    net_config = config.NetworkConfig(indent=3, contents=RUNNING, ignore_lines=[r"\s*no .*"])
    assert len(net_config.items) == 6

    net_config = config.NetworkConfig(
        indent=3, contents=RUNNING, ignore_lines=[re.compile(r"\s*no .*")]
    )
    assert len(net_config.items) == 6
    # above updates the global DEFAULT_IGNORE_LINES_RE list, revert back the global
    # to it's original value
    config.DEFAULT_IGNORE_LINES_RE = ORIGINAL_DEFAULT_IGNORE_LINES_RE


def test_config_get_block():
    net_config = config.NetworkConfig(indent=3, contents=RUNNING)

    with pytest.raises(AssertionError, match="path argument must be a list object"):
        net_config.get_block("interface Ethernet2")

    with pytest.raises(ValueError, match="path does not exist in config"):
        net_config.get_block(["interface Ethernet3"])

    block = net_config.get_block(["interface Ethernet2"])
    assert len(block) == 4


def test_line_hierarchy():
    net_config = config.NetworkConfig(indent=3, contents=RUNNING)

    lines = net_config.items
    assert lines[0].has_children
    assert not lines[0].has_parents
    assert not lines[1].has_children
    assert lines[1].has_parents


def test_updates_repeat_lines():
    candidate_obj = config.NetworkConfig(indent=3)
    candidate_obj.load(WANT_SRC_1)

    running_obj = config.NetworkConfig(indent=3, contents=HAVE_SRC_1)

    configdiffobjs = candidate_obj.difference(running_obj)
    diff_list = config.dumps(configdiffobjs, "commands").split("\n")
    want_src_list = WANT_SRC_1.strip().split("\n")
    for generated_diff_line, candidate_diff_line in zip(diff_list, want_src_list):
        assert generated_diff_line == candidate_diff_line.strip()


def test_updates_repeat_parents():
    expected_diff = [
        "interface loopback0",
        "ip ospf 1 area 0.0.0.0",
        "interface GigabitEthernet0/1",
        "ip ospf 1 area 0.0.0.0",
        "interface GigabitEthernet0/2",
        "ip ospf 1 area 0.0.0.0",
        "router isis fabric",
        "is-type level-2",
        "net 49.0000.0000.0003.00",
        "interface loopback0",
        "ip router isis fabric",
        "interface GigabitEthernet0/1",
        "ip router isis fabric",
        "interface GigabitEthernet0/2",
        "ip router isis fabric",
    ]
    candidate_obj = config.NetworkConfig(indent=1)
    candidate_obj.load(WANT_SRC_2)

    running_obj = config.NetworkConfig(indent=1, contents=HAVE_SRC_2)

    configdiffobjs = candidate_obj.difference(running_obj)
    diff_list = config.dumps(configdiffobjs, "commands").split("\n")

    for generated_diff_line, candidate_diff_line in zip(diff_list, expected_diff):
        print(generated_diff_line, candidate_diff_line)
        assert generated_diff_line == candidate_diff_line.strip()
