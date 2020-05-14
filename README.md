ansible_collections.ansible.netcommon
=====================================

Ansible Network Collection for Common Code


<!--start collection content-->
# Become plugins
Name | Description
--- | ---
[ansible.netcommon.enable](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.enable.rst)|Switch to elevated permissions on a network device
# Connection plugins
Name | Description
--- | ---
[ansible.netcommon.httpapi](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.httpapi.rst)|Use httpapi to run command on network appliances
[ansible.netcommon.napalm](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.napalm.rst)|Provides persistent connection using NAPALM
[ansible.netcommon.netconf](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.netconf.rst)|Provides a persistent connection using the netconf protocol
[ansible.netcommon.network_cli](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.network_cli.rst)|Use network_cli to run command on network appliances
[ansible.netcommon.persistent](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.persistent.rst)|Use a persistent unix socket for connection
# Filter plugins
Name | Description
--- | ---
cidr_merge|
comp_type5|
hash_salt|
hwaddr|Check if string is a HW/MAC address and filter it 
ip4_hex|Convert an IPv4 address to Hexadecimal notation 
ipaddr|Check if string is an IP address or network and filter it 
ipmath|
ipsubnet|Manipulate IPv4/IPv6 subnets 
ipv4|
ipv6|
ipwrap|
macaddr|
network_in_network|Checks whether the 'test' address or addresses are in 'value', including broadcast and network
network_in_usable|Checks whether 'test' is a useable address or addresses in 'value'
next_nth_usable|
nthhost|Get the nth host within a given network 
parse_cli|
parse_cli_textfsm|
parse_xml|
previous_nth_usable|
reduce_on_network|Reduces a list of addresses to only the addresses that match a given network.
slaac|Get the SLAAC address within given network 
type5_pw|
vlan_parser|Input: Unsorted list of vlan integers Output: Sorted string list of integers according to IOS-like vlan list rules 1. Vlans are listed in ascending order 2. Runs of 3 or more consecutive vlans are listed with a dash 3. The first line of the list can be first_line_len characters long 4. Subsequent list lines can be other_line_len characters
# Modules
Name | Description
--- | ---
[ansible.netcommon.cli_command](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.cli_command.rst)|Run a cli command on cli-based network devices
[ansible.netcommon.cli_config](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.cli_config.rst)|Push text based configuration to network devices over network_cli
[ansible.netcommon.net_banner](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_banner.rst)|Manage multiline banners on network devices
[ansible.netcommon.net_get](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_get.rst)|Copy a file from a network device to Ansible Controller
[ansible.netcommon.net_interface](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_interface.rst)|Manage Interface on network devices
[ansible.netcommon.net_l2_interface](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_l2_interface.rst)|Manage Layer-2 interface on network devices
[ansible.netcommon.net_l3_interface](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_l3_interface.rst)|Manage L3 interfaces on network devices
[ansible.netcommon.net_linkagg](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_linkagg.rst)|Manage link aggregation groups on network devices
[ansible.netcommon.net_lldp](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_lldp.rst)|Manage LLDP service configuration on network devices
[ansible.netcommon.net_lldp_interface](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_lldp_interface.rst)|Manage LLDP interfaces configuration on network devices
[ansible.netcommon.net_logging](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_logging.rst)|Manage logging on network devices
[ansible.netcommon.net_ping](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_ping.rst)|Tests reachability using ping from a network device
[ansible.netcommon.net_put](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_put.rst)|Copy a file from Ansible Controller to a network device
[ansible.netcommon.net_static_route](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_static_route.rst)|Manage static IP routes on network appliances (routers, switches et. al.)
[ansible.netcommon.net_system](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_system.rst)|Manage the system attributes on network devices
[ansible.netcommon.net_user](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_user.rst)|Manage the aggregate of local users on network device
[ansible.netcommon.net_vlan](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_vlan.rst)|Manage VLANs on network devices
[ansible.netcommon.net_vrf](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.net_vrf.rst)|Manage VRFs on network devices
[ansible.netcommon.netconf_config](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.netconf_config.rst)|netconf device configuration
[ansible.netcommon.netconf_get](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.netconf_get.rst)|Fetch configuration/state data from NETCONF enabled network devices.
[ansible.netcommon.netconf_rpc](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.netconf_rpc.rst)|Execute operations on NETCONF enabled network devices.
[ansible.netcommon.restconf_config](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.restconf_config.rst)|Handles create, update, read and delete of configuration data on RESTCONF enabled devices.
[ansible.netcommon.restconf_get](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.restconf_get.rst)|Fetch configuration/state data from RESTCONF enabled devices.
[ansible.netcommon.telnet](https://github.com/cidrblock/arista.eos/blob/master/docs/ansible.netcommon.telnet.rst)|Executes a low-down and dirty telnet command
<!--end collection content-->