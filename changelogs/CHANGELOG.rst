==========================================
Ansible Netcommon Collection Release Notes
==========================================

.. contents:: Topics


v1.0.0
======

New Plugins
-----------

Become
~~~~~~

- enable - Switch to elevated permissions on a network device

Connection
~~~~~~~~~~

- httpapi - Use httpapi to run command on network appliances
- napalm - Provides persistent connection using NAPALM
- netconf - Provides a persistent connection using the netconf protocol
- network_cli - Use network_cli to run command on network appliances
- persistent - Use a persistent unix socket for connection

Httpapi
~~~~~~~

- restconf - HttpApi Plugin for devices supporting Restconf API

Netconf
~~~~~~~

- default - Use default netconf plugin to run standard netconf commands as per RFC

New Modules
-----------

- cli_command - Run a cli command on cli-based network devices
- cli_config - Push text based configuration to network devices over network_cli
- net_banner - (deprecated, removed after 2022-06-01) Manage multiline banners on network devices
- net_get - Copy a file from a network device to Ansible Controller
- net_interface - (deprecated, removed after 2022-06-01) Manage Interface on network devices
- net_l2_interface - (deprecated, removed after 2022-06-01) Manage Layer-2 interface on network devices
- net_l3_interface - (deprecated, removed after 2022-06-01) Manage L3 interfaces on network devices
- net_linkagg - (deprecated, removed after 2022-06-01) Manage link aggregation groups on network devices
- net_lldp - (deprecated, removed after 2022-06-01) Manage LLDP service configuration on network devices
- net_lldp_interface - (deprecated, removed after 2022-06-01) Manage LLDP interfaces configuration on network devices
- net_logging - (deprecated, removed after 2022-06-01) Manage logging on network devices
- net_ping - Tests reachability using ping from a network device
- net_put - Copy a file from Ansible Controller to a network device
- net_static_route - (deprecated, removed after 2022-06-01) Manage static IP routes on network appliances (routers, switches et. al.)
- net_system - (deprecated, removed after 2022-06-01) Manage the system attributes on network devices
- net_user - (deprecated, removed after 2022-06-01) Manage the aggregate of local users on network device
- net_vlan - (deprecated, removed after 2022-06-01) Manage VLANs on network devices
- net_vrf - (deprecated, removed after 2022-06-01) Manage VRFs on network devices
- netconf_config - netconf device configuration
- netconf_get - Fetch configuration/state data from NETCONF enabled network devices.
- netconf_rpc - Execute operations on NETCONF enabled network devices.
- restconf_config - Handles create, update, read and delete of configuration data on RESTCONF enabled devices.
- restconf_get - Fetch configuration/state data from RESTCONF enabled devices.
- telnet - Executes a low-down and dirty telnet command
