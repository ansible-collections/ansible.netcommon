==========================================
Ansible Netcommon Collection Release Notes
==========================================

.. contents:: Topics


v2.4.0
======

Minor Changes
-------------

- Add network_resource plugin to manage and provide single entry point for all resource modules for higher oder roles.

Deprecated Features
-------------------

- network_cli - The paramiko_ssh setting ``look_for_keys`` was set automatically based on the values of the ``password`` and ``private_key_file`` options passed to network_cli. This option can now be set explicitly, and the automatic setting of ``look_for_keys`` will be removed after 2024-01-01  (https://github.com/ansible-collections/ansible.netcommon/pull/271).

Bugfixes
--------

- network_cli - Add ability to set options inherited from paramiko/libssh in ansible >= 2.11 (https://github.com/ansible-collections/ansible.netcommon/pull/271).

New Modules
-----------

- network_resource - Manage resource modules

v2.3.0
======

Minor Changes
-------------

- Add vlan_expander filter
- Persistent connection options (persistent_command_timeout, persistent_log_messages, etc.) have been unified across all persistent connections. New persistent connections may also now get these options by extending the connection_persistent documentation fragment.

v2.2.0
======

Minor Changes
-------------

- Add variable to control ProxyCommand with libssh connection.
- NetworkTemplate and ResouceModule base classes have been moved under module_utils.network.common.rm_base. Stubs have been kept for backwards compatibility. These will be removed after 2023-01-01. Please update imports for existing modules that subclass them. The `cli_rm_builder <https://github.com/ansible-network/cli_rm_builder>`_ has been updated to use the new imports.

Bugfixes
--------

- libssh - Fix fromatting of authenticity error message when not prompting for input (https://github.com/ansible-collections/ansible.netcommon/issues/283)
- netconf - Fix connection with ncclient versions < 0.6.10
- network_cli - Fix for execution failing when ansible_ssh_password is used to specify password (https://github.com/ansible-collections/ansible.netcommon/issues/288)

v2.1.0
======

Minor Changes
-------------

- Add support for ProxyCommand with netconf connection.

Bugfixes
--------

- Variables in play_context will now be updated for netconf connections on each task run.
- fix SCP/SFTP when using network_cli with libssh

v2.0.2
======

Bugfixes
--------

- Fix cli_parse issue with parsers in utils collection (https://github.com/ansible-collections/ansible.netcommon/pull/270)
- Support single_user_mode with Ansible 2.9.

v2.0.1
======

Minor Changes
-------------

- Several module_utils files were intended to be licensed BSD, but missing a license preamble in the files. The preamble has been added, and all authors for the files have given their assent to the intended license https://github.com/ansible-collections/ansible.netcommon/pull/122

Bugfixes
--------

- Allow setting `host_key_checking` through a play/task var for `network_cli`.
- Ensure passed-in terminal_initial_prompt and terminal_initial_answer values are cast to bytes before using
- Update valid documentation for net_ping module.
- ncclient - catch and handle exception to prevent stack trace when running in FIPS mode
- net_put - Remove temp file created when file already exist on destination when mode is 'text'.

v2.0.0
======

Major Changes
-------------

- Remove deprecated connection arguments from netconf_config

Minor Changes
-------------

- Add SCP support when using ssh_type libssh
- Add `single_user_mode` option for command output caching.
- Move cli_config idempotent warning message with the task response under `warnings` key if `changed` is `True`
- Reduce CPU usage and network module run time when using `ansible_network_import_modules`
- Support any() and all() filters in Jinja2.

Breaking Changes / Porting Guide
--------------------------------

- Removed vendored ipaddress package from collection. If you use ansible_collections.ansible.netcommon.plugins.module_utils.compat.ipaddress in your collection, you will need to change this to import ipaddress instead. If your content using ipaddress supports Python 2.7, you will additionally need to make sure that the user has the ipaddress package installed. Please refer to https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_best_practices.html#importing-and-using-shared-code to see how to safely import external packages that may be missing from the user's system A backport of ipaddress for Python 2.7 is available at https://pypi.org/project/ipaddress/

Deprecated Features
-------------------

- Deprecate cli_parse module and textfsm, ttp, xml, json parser plugins as they are moved to ansible.utils collection (https://github.com/ansible-collections/ansible.netcommon/pull/182 https://github.com/ansible-collections/ansible.utils/pull/28)

Bugfixes
--------

- Expose connection class object to rm_template (https://github.com/ansible-collections/ansible.netcommon/pull/180)
- network_cli - When using ssh_type libssh, handle closed connection gracefully instead of throwing an exception

New Plugins
-----------

Cache
~~~~~

- memory - RAM backed, non persistent cache.

v1.5.0
======

Minor Changes
-------------

- Add 'purged' to ACTION_STATES.

Bugfixes
--------

- Add netconf_config integration tests for nxos (https://github.com/ansible-collections/ansible.netcommon/pull/185)
- Fix GetReply object has no attribute strip() (https://github.com/ansible-collections/cisco.iosxr/issues/97)
- Fix config diff logic if parent configuration is present more than once in the candidate config and update docs (https://github.com/ansible-collections/ansible.netcommon/pull/189)
- Fix missing changed from net_get (https://github.com/ansible-collections/ansible.netcommon/issues/198)
- Fix netconf_config module integration test issuea (https://github.com/ansible-collections/ansible.netcommon/pull/177)
- Fix restconf_config incorrectly spoofs HTTP 409 codes (https://github.com/ansible-collections/ansible.netcommon/issues/191)
- Split checks for prompt and errors in network_cli so that detected errors are not lost if the prompt is in a later chunk.

v1.4.1
======

Release Summary
---------------

Change how black config is specified to avoid issues with Automation Hub release process

v1.4.0
======

Minor Changes
-------------

- 'prefix' added to NetworkTemplate class, inorder to handle the negate operation for vyos config commands.
- Add support for json format input format for netconf modules using ``xmltodict``
- Update docs for netconf_get and netconf_config examples using display=native

Bugfixes
--------

- Added support for private key based authentication with libssh transport (https://github.com/ansible-collections/ansible.netcommon/issues/168)
- Fixed ipaddr filter plugins in ansible.netcommon collections is not working with latest Ansible (https://github.com/ansible-collections/ansible.netcommon/issues/157)
- Fixed netconf_rpc task fails due to encoding issue in the response (https://github.com/ansible-collections/ansible.netcommon/issues/151)
- Fixed ssh_type none issue while using net_put and net_get module (https://github.com/ansible-collections/ansible.netcommon/issues/153)
- Fixed unit tests under python3.5
- ipaddr filter - query "address/prefix" (also: "gateway", "gw", "host/prefix", "hostnet", and "router") now handles addresses with /32 prefix or /255.255.255.255 netmask
- network_cli - Update underlying ssh connection's play_context in update_play_context, so that the username or password can be updated

v1.3.0
======

Minor Changes
-------------

- Confirmed commit fails with TypeError in IOS XR netconf plugin (https://github.com/ansible-collections/cisco.iosxr/issues/74)
- The netconf_config module now allows root tag with namespace prefix.
- cli_config: Add new return value diff which is returned when the cliconf plugin supports onbox diff
- cli_config: Clarify when commands is returned when the module is run

Bugfixes
--------

- cli_parse - Ensure only native types are returned to the control node from the parser.
- netconf - Changed log level for message of using default netconf plugin to match the level used when a platform-specific netconf plugin is found

v1.2.1
======

Bugfixes
--------

- Fixed "Object of type Capabilities is not JSON serializable" when using default netconf plugin.

v1.2.0
======

Minor Changes
-------------

- Added description to collection galaxy.yml file.
- NetworkConfig objects now have an optional `comment_tokens` parameter which takes a list of strings which will override the DEFAULT_COMMENT_TOKENS list.
- New cli_parse module for parsing structured text using a variety of parsers. The initial implemetation of cli_parse can be used with json, native, ntc_templates, pyats, textfsm, ttp, and xml.
- The httpapi connection plugin now works with `wait_for_connection`. This will periodically request the root page of the server described by the plugin's options until the request succeeds. This can only test that the server is reachable, the correctness or usability of the API is not guaranteed.

Bugfixes
--------

- cli_config fixes issue when rollback_id = 0 evalutes to False
- sort_list will sort a list of dicts using the sorted method with key as an argument.

New Modules
-----------

- cli_parse - Parse cli output or text using a variety of parsers

v1.1.2
======

Release Summary
---------------

Rereleased 1.1.1 with updated changelog.

v1.1.1
======

Release Summary
---------------

Rereleased 1.1.0 with regenerated documentation.

v1.1.0
======

Major Changes
-------------

- Add libssh connection plugin and refactor network_cli (https://github.com/ansible-collections/ansible.netcommon/pull/30)

Minor Changes
-------------

- Add content option validation for netconf_config module (https://github.com/ansible-collections/ansible.netcommon/pull/66)
- Documentation of module arguments updated to match expected types where missing.
- Resource Modules: changed flag is set to true in check_mode for all ACTION_STATES (https://github.com/ansible-collections/ansible.netcommon/pull/82)

Removed Features (previously deprecated)
----------------------------------------

- module_utils.network.common.utils.ComplexDict has been removed

Bugfixes
--------

- Replace deprecated `getiterator` call with `iter`
- ipaddr - "host" query supports /31 subnets properly
- ipaddr filter - Fixed issue where the first IPv6 address in a subnet was not being considered a valid address.
- ipaddr filter now returns empty list instead of False on empty list input
- net_put - Restore missing function removed when action plugin stopped inheriting NetworkActionBase
- nthhost filter now returns str instead of IPAddress object
- slaac filter now returns str instead of IPAddress object

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
