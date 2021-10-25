
.. _plugins_in_ansible.netcommon:


Ansible.Netcommon
=================

Collection version None

.. toctree::
    :maxdepth: 1

Plugin Index
------------

These are the plugins in the ansible.netcommon collection

Become
~~~~~~

* :ref:`netcommon <ansible_collections.ansible.netcommon.enable>` -- Switch to elevated permissions on a network device

Connection
~~~~~~~~~~

* :ref:`netcommon <ansible_collections.ansible.netcommon.network_cli>` -- Use network_cli to run command on network appliances
* :ref:`netcommon <ansible_collections.ansible.netcommon.libssh>` -- (Tech preview) Run tasks using libssh for ssh connection
* :ref:`netcommon <ansible_collections.ansible.netcommon.napalm>` -- Provides persistent connection using NAPALM
* :ref:`netcommon <ansible_collections.ansible.netcommon.persistent>` -- Use a persistent unix socket for connection
* :ref:`netcommon <ansible_collections.ansible.netcommon.httpapi>` -- Use httpapi to run command on network appliances
* :ref:`netcommon <ansible_collections.ansible.netcommon.netconf>` -- Provides a persistent connection using the netconf protocol

Ipaddr Filter
~~~~~~~~~~~~~

* :ref:`netcommon <ansible_collections.ansible.netcommon.cidr_merge>` -- ansible.netcommon cidr_merge filter plugin
* :ref:`netcommon <ansible_collections.ansible.netcommon.ipaddr>` -- Check if string is an IP address or network and filter it
* :ref:`netcommon <ansible_collections.ansible.netcommon.ipmath>` -- ansible.netcommon ipmath filter plugin
* :ref:`netcommon <ansible_collections.ansible.netcommon.ipwrap>` -- ansible.netcommon ipwrap filter plugin
* :ref:`netcommon <ansible_collections.ansible.netcommon.ip4_hex>` -- Convert an IPv4 address to Hexadecimal notation
* :ref:`netcommon <ansible_collections.ansible.netcommon.ipv4>` -- ansible.netcommon ipv4 filter plugin
* :ref:`netcommon <ansible_collections.ansible.netcommon.ipv6>` -- ansible.netcommon ipv6 filter plugin
* :ref:`netcommon <ansible_collections.ansible.netcommon.ipsubnet>` -- Manipulate IPv4/IPv6 subnets
* :ref:`netcommon <ansible_collections.ansible.netcommon.next_nth_usable>` -- ansible.netcommon next_nth_usable filter plugin
* :ref:`netcommon <ansible_collections.ansible.netcommon.network_in_network>` -- Checks whether the 'test' address or addresses are in 'value', including broadcast and network
* :ref:`netcommon <ansible_collections.ansible.netcommon.network_in_usable>` -- Checks whether 'test' is a useable address or addresses in 'value'
* :ref:`netcommon <ansible_collections.ansible.netcommon.reduce_on_network>` -- Reduces a list of addresses to only the addresses that match a given network.
* :ref:`netcommon <ansible_collections.ansible.netcommon.nthhost>` -- Get the nth host within a given network
* :ref:`netcommon <ansible_collections.ansible.netcommon.previous_nth_usable>` -- ansible.netcommon previous_nth_usable filter plugin
* :ref:`netcommon <ansible_collections.ansible.netcommon.slaac>` -- Get the SLAAC address within given network
* :ref:`netcommon <ansible_collections.ansible.netcommon.hwaddr>` -- Check if string is a HW/MAC address and filter it
* :ref:`netcommon <ansible_collections.ansible.netcommon.macaddr>` -- ansible.netcommon macaddr filter plugin

Network Filter
~~~~~~~~~~~~~~

* :ref:`netcommon <ansible_collections.ansible.netcommon.parse_cli>` -- ansible.netcommon parse_cli filter plugin
* :ref:`netcommon <ansible_collections.ansible.netcommon.parse_cli_textfsm>` -- ansible.netcommon parse_cli_textfsm filter plugin
* :ref:`netcommon <ansible_collections.ansible.netcommon.parse_xml>` -- ansible.netcommon parse_xml filter plugin
* :ref:`netcommon <ansible_collections.ansible.netcommon.type5_pw>` -- ansible.netcommon type5_pw filter plugin
* :ref:`netcommon <ansible_collections.ansible.netcommon.hash_salt>` -- ansible.netcommon hash_salt filter plugin
* :ref:`netcommon <ansible_collections.ansible.netcommon.comp_type5>` -- ansible.netcommon comp_type5 filter plugin
* :ref:`netcommon <ansible_collections.ansible.netcommon.vlan_parser>` -- Input: Unsorted list of vlan integers
* :ref:`netcommon <ansible_collections.ansible.netcommon.vlan_expander>` -- ansible.netcommon vlan_expander filter plugin

Httpapi
~~~~~~~

* :ref:`netcommon <ansible_collections.ansible.netcommon.restconf>` -- HttpApi Plugin for devices supporting Restconf API

Netconf
~~~~~~~

* :ref:`netcommon <ansible_collections.ansible.netcommon.default>` -- Use default netconf plugin to run standard netconf commands as per RFC

Modules
~~~~~~~

* :ref:`netcommon <ansible_collections.ansible.netcommon.restconf_config>` -- Handles create, update, read and delete of configuration data on RESTCONF enabled devices.
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_lldp>` -- (deprecated, removed after 2022-07-01) Manage LLDP service configuration on network devices
* :ref:`netcommon <ansible_collections.ansible.netcommon.cli_config>` -- Push text based configuration to network devices over network_cli
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_put>` -- Copy a file from Ansible Controller to a network device
* :ref:`netcommon <ansible_collections.ansible.netcommon.cli_command>` -- Run a cli command on cli-based network devices
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_ping>` -- Tests reachability using ping from a network device
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_l2_interface>` -- (deprecated, removed after 2022-07-01) Manage Layer-2 interface on network devices
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_system>` -- (deprecated, removed after 2022-07-01) Manage the system attributes on network devices
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_static_route>` -- (deprecated, removed after 2022-07-01) Manage static IP routes on network appliances (routers, switches et. al.)
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_l3_interface>` -- (deprecated, removed after 2022-07-01) Manage L3 interfaces on network devices
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_lldp_interface>` -- (deprecated, removed after 2022-07-01) Manage LLDP interfaces configuration on network devices
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_interface>` -- (deprecated, removed after 2022-07-01) Manage Interface on network devices
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_get>` -- Copy a file from a network device to Ansible Controller
* :ref:`netcommon <ansible_collections.ansible.netcommon.netconf_get>` -- Fetch configuration/state data from NETCONF enabled network devices.
* :ref:`netcommon <ansible_collections.ansible.netcommon.netconf_config>` -- netconf device configuration
* :ref:`netcommon <ansible_collections.ansible.netcommon.netconf_rpc>` -- Execute operations on NETCONF enabled network devices.
* :ref:`netcommon <ansible_collections.ansible.netcommon.telnet>` -- Executes a low-down and dirty telnet command
* :ref:`netcommon <ansible_collections.ansible.netcommon.network_resource>` -- Manage resource modules
* :ref:`netcommon <ansible_collections.ansible.netcommon.cli_parse>` -- Parse cli output or text using a variety of parsers
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_user>` -- (deprecated, removed after 2022-07-01) Manage the aggregate of local users on network device
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_banner>` -- (deprecated, removed after 2022-07-01) Manage multiline banners on network devices
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_logging>` -- (deprecated, removed after 2022-07-01) Manage logging on network devices
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_vrf>` -- (deprecated, removed after 2022-07-01) Manage VRFs on network devices
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_linkagg>` -- (deprecated, removed after 2022-07-01) Manage link aggregation groups on network devices
* :ref:`netcommon <ansible_collections.ansible.netcommon.restconf_get>` -- Fetch configuration/state data from RESTCONF enabled devices.
* :ref:`netcommon <ansible_collections.ansible.netcommon.net_vlan>` -- (deprecated, removed after 2022-07-01) Manage VLANs on network devices


.. seealso::

    List of :ref:`collections <list_of_collections>` with docs hosted here.

.. toctree::
    :maxdepth: 1
    :hidden:
