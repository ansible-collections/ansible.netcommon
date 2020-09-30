import json
import re
from ansible.errors import AnsibleError
from ansible.module_utils.basic import missing_required_lib


try:
    from netaddr import IPNetwork, IPAddress, EUI

    HAS_NETADDR = True
except ImportError:
    HAS_NETADDR = False


def _need_netaddr(func):
    def wrapper(*args, **kwargs):
        if not HAS_NETADDR:
            msg = "'{test}' requires 'netaddr' {stnd}".format(
                test=func.__name__,
                stnd=missing_required_lib("netaddr").replace("module", "plugin"),
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
def in_network(ip, network):
    try:
        return IPNetwork(ip) in IPNetwork(network)
    except Exception:
        return False


@_need_netaddr
def in_one_network(ip, networks):
    _error_not_list("in_one_network", networks)
    bools = [in_network(ip, network) for network in networks]
    if bools.count(True) == 1:
        return True
    return False


@_need_netaddr
def in_any_network(ip, networks):
    _error_not_list("in_networks", networks)
    bools = [in_network(ip, network) for network in networks]
    if True in bools:
        return True
    return False


@_need_netaddr
def hostmask(ip):
    try:
        return IPAddress(ip).is_hostmask()
    except Exception:
        return False


@_need_netaddr
def ip(ip):
    return ip_address(ip) or ip_network(ip)


@_need_netaddr
def ip_address(ip):
    try:
        IPAddress(ip)
        return True
    except Exception:
        return False


@_need_netaddr
def ip_network(ip):
    try:
        IPNetwork(ip)
        return True
    except Exception:
        return False


@_need_netaddr
def ipv4(ip):
    try:
        return IPAddress(ip).version == 4
    except Exception:
        return False


@_need_netaddr
def ipv6(ip):
    try:
        return IPAddress(ip).version == 6
    except Exception:
        return False


@_need_netaddr
def loopback(ip):
    try:
        return IPAddress(ip).is_loopback()
    except Exception:
        return False


@_need_netaddr
def mac(mac):
    try:
        EUI(mac)
        return True
    except Exception:
        return False

@_need_netaddr
def mac_org(mac, regex):
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
    try:
        return IPAddress(ip).is_multicast()
    except Exception:
        return False


@_need_netaddr
def netmask(ip):
    try:
        return IPAddress(ip).is_netmask()
    except Exception:
        return False


@_need_netaddr
def private(ip):
    try:
        return IPAddress(ip).is_private()
    except Exception:
        return False


@_need_netaddr
def public(ip):
    try:
        ip = IPAddress(ip)
        return ip.is_unicast() and not ip.is_private()
    except Exception:
        return False


@_need_netaddr
def reserved(ip):
    try:
        return IPAddress(ip).is_reserved()
    except Exception:
        return False


@_need_netaddr
def unicast(ip):
    try:
        return IPAddress(ip).is_unicast()
    except Exception:
        return False


class TestModule(object):
    """ network jinja tests
    """

    test_map = {
        "in_network": in_network,
        "in_one_network": in_one_network,
        "in_any_network": in_any_network,
        "hostmask": hostmask,
        "ip": ip,
        "ip_address": ip_address,
        "ip_network": ip_network,
        "ipv4": ipv4,
        "ipv6": ipv6,
        "loopback": loopback,
        "mac": mac,
        "mac_org": mac_org,
        "multicast": multicast,
        "netmask": netmask,
        "private": private,
        "public": public,
        "reserved": reserved,
        "unicast": unicast,
    }

    def tests(self):
        is_map = {"is_" + k: v for (k, v) in self.test_map.items()}
        self.test_map.update(is_map)
        return self.test_map
