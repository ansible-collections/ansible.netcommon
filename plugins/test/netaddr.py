# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The test plugin file for netaddr tests
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


import json
import re

from ansible.errors import AnsibleError
from ansible.module_utils.basic import missing_required_lib

try:
    from netaddr import EUI, IPAddress, IPNetwork

    HAS_NETADDR = True
except ImportError:
    HAS_NETADDR = False


def _need_netaddr(func):
    def wrapper(*args, **kwargs):
        if not HAS_NETADDR:
            msg = "'{test}' requires 'netaddr' {stnd}".format(
                test=func.__name__,
                stnd=missing_required_lib("netaddr").replace(
                    "module", "plugin"
                ),
            )
            raise AnsibleError(msg)
        return func(*args, **kwargs)

    return wrapper


def _to_well_known_type(obj):
    """ Convert an ansible internal type to a well-known type
    ie AnsibleUnicode => str

    :param obj: the obj to convert
    :type obj: unknown
    """
    return json.loads(json.dumps(obj))


def _error_not_list(test, obj):
    tipe = _to_well_known_type(obj)
    if not isinstance(tipe, list):
        msg = "The test '{test}' requires a list, but {obj} was a '{type}'".format(
            test=test, obj=obj, type=type(tipe).__name__
        )
        raise AnsibleError(msg)


@_need_netaddr
def hostmask(ip):
    """Test if an address is a hostmask<br/>`'0.0.0.255' is ansible.netcommon.hostmask`
    """
    try:
        return IPAddress(ip).is_hostmask()
    except Exception:
        return False


@_need_netaddr
def in_network(ip, network):
    """Test if an address or network is in a network<br/>`'10.1.1.1' is ansible.netcommon.in_network '10.0.0.0/8'`
    """
    try:
        return IPNetwork(ip) in IPNetwork(network)
    except Exception:
        return False


@_need_netaddr
def in_one_network(ip, networks):
    """Test if an IP or network is in one network<br/>`'10.1.1.1' is ansible.netcommon.in_one_network ['10.0.0.0/8', '192.168.1.0/24']`
    """

    _error_not_list("in_one_network", networks)
    bools = [in_network(ip, network) for network in networks]
    if bools.count(True) == 1:
        return True
    return False


@_need_netaddr
def in_any_network(ip, networks):
    """Test if an IP or network is in any network<br/>`'10.1.1.1' is ansible.netcommon.in_any_network ['10.0.0.0/8', '192.168.1.0/24']`
    """
    _error_not_list("in_networks", networks)
    bools = [in_network(ip, network) for network in networks]
    if True in bools:
        return True
    return False


@_need_netaddr
def ip(ip):
    """Test if something in an IP address or network<br/>`'10.1.1.1' is ansible.netcommon.ip`
    """
    try:
        IPNetwork(ip)
        return True
    except Exception:
        return False


@_need_netaddr
def ip_address(ip):
    """Test if something in an IP address<br/>`'10.1.1.1' is ansible.netcommon.ip_address`
    """
    try:
        IPAddress(ip)
        return True
    except Exception:
        return False


@_need_netaddr
def ipv4(ip):
    """Test if something in an IPv4 address or network<br/>`'10.0.0.0/8' is ansible.netcommon.ipv4`
    """
    try:
        return IPNetwork(ip).version == 4
    except Exception:
        return False


@_need_netaddr
def ipv4_address(ip):
    """Test if something in an IPv4 address<br/>`'10.1.1.1' is ansible.netcommon.ipv4_address`
    """
    try:
        return IPAddress(ip).version == 4
    except Exception:
        return False


@_need_netaddr
def ipv6(ip):
    """ Test if something is an IPv6 address or network<br/>`'2001:db8:a::123/64' is ansible.netcommon.ipv6`
    """
    try:
        return IPNetwork(ip).version == 6
    except Exception:
        return False


@_need_netaddr
def ipv6_address(ip):
    """ Test if something is an IPv6 address or network<br/>`'fe80::216:3eff:fee4:16f3' is ansible.netcommon.ipv6_address`
    """
    try:
        return IPAddress(ip).version == 6
    except Exception:
        return False


@_need_netaddr
def loopback(ip):
    """ Test if an IP address is a loopback<br/>`'127.10.10.10' is ansible.netcommon.loopback`
    """
    try:
        return IPAddress(ip).is_loopback()
    except Exception:
        return False


@_need_netaddr
def mac(mac):
    """ Test if something is a mac address<br/>`'02:16:3e:e4:16:f3' is ansible.netcommon.mac`
    """
    try:
        EUI(mac)
        return True
    except Exception:
        return False


@_need_netaddr
def mac_org(mac, regex):
    """ Test a mac OUI against a regular expression<br/>`'00:02:b3:e4:16:f3' is ansible.netcommon.mac_org('^Intel')`
    """
    try:
        oui = EUI(mac).oui
        for idx in range(oui.reg_count):
            if re.match(regex, oui.registration(idx).org):
                return True
        return False
    except Exception:
        return False


@_need_netaddr
def multicast(ip):
    """ Test for a multicast IP address<br/>`'224.0.0.1' is ansible.netcommon.multicast`
    """
    try:
        return IPAddress(ip).is_multicast()
    except Exception:
        return False


@_need_netaddr
def netmask(ip):
    """ Test for a valid netmask<br/>`'255.255.255.0' is ansible.netcommon.netmask`
    """
    try:
        return IPAddress(ip).is_netmask()
    except Exception:
        return False


@_need_netaddr
def private(ip):
    """ Test if an IP address is private<br/>`'10.1.1.1' is ansible.netcommon.private`
    """
    try:
        return IPAddress(ip).is_private()
    except Exception:
        return False


@_need_netaddr
def public(ip):
    """ Test if an IP address is public<br/>`'8.8.8.8' is ansible.netcommon.public`
    """
    try:
        ip = IPAddress(ip)
        return ip.is_unicast() and not ip.is_private()
    except Exception:
        return False


@_need_netaddr
def reserved(ip):
    """ Test for a reserved IP address<br/>`'253.0.0.1' is ansible.netcommon.reserved`
    """
    try:
        return IPAddress(ip).is_reserved()
    except Exception:
        return False


@_need_netaddr
def unicast(ip):
    """ Test for a unicast IP address<br/>`'10.0.0.1' is ansible.netcommon.unicast`
    """
    try:
        return IPAddress(ip).is_unicast()
    except Exception:
        return False


class TestModule(object):
    """ network jinja tests
    """

    test_map = {
        "hostmask": hostmask,
        "in_any_network": in_any_network,
        "in_network": in_network,
        "in_one_network": in_one_network,
        "ip_address": ip_address,
        "ip": ip,
        "ipv4": ipv4,
        "ipv4_address": ipv4_address,
        "ipv6": ipv6,
        "ipv6_address": ipv6_address,
        "loopback": loopback,
        "mac_org": mac_org,
        "mac": mac,
        "multicast": multicast,
        "netmask": netmask,
        "private": private,
        "public": public,
        "reserved": reserved,
        "unicast": unicast,
    }

    def tests(self):
        return self.test_map
