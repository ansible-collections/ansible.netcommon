# (c) 2022 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author:
 - Ansible Networking Team (@ansible-network)
name: test_netconf
short_description: Provides a persistent connection using the netconf protocol
description:
- This connection plugin provides a connection to remote devices over the SSH NETCONF
  subsystem.  This connection plugin is typically used by network devices for sending
  and receiving RPC calls over NETCONF.
- Note this connection plugin requires ncclient to be installed on the local Ansible
  controller.
version_added: 3.1.0
requirements:
- ncclient
extends_documentation_fragment:
- ansible.netcommon.connection_persistent
- ansible.netcommon.test_connection
options:
  host:
    description:
    - Specifies the remote device FQDN or IP address to establish the SSH connection
      to.
    default: inventory_hostname
    vars:
    - name: ansible_host
  port:
    type: int
    description:
    - Specifies the port on the remote device that listens for connections when establishing
      the SSH connection.
    default: 830
    ini:
    - section: defaults
      key: remote_port
    env:
    - name: ANSIBLE_REMOTE_PORT
    vars:
    - name: ansible_port
  network_os:
    description:
    - Configures the device platform network operating system.  This value is used
      to load a device specific netconf plugin.  If this option is not configured
      (or set to C(auto)), then Ansible will attempt to guess the correct network_os
      to use. If it can not guess a network_os correctly it will use C(default).
    vars:
    - name: ansible_network_os
  remote_user:
    description:
    - The username used to authenticate to the remote device when the SSH connection
      is first established.  If the remote_user is not specified, the connection will
      use the username of the logged in user.
    - Can be configured from the CLI via the C(--user) or C(-u) options.
    ini:
    - section: defaults
      key: remote_user
    env:
    - name: ANSIBLE_REMOTE_USER
    vars:
    - name: ansible_user
  password:
    description:
    - Configures the user password used to authenticate to the remote device when
      first establishing the SSH connection.
    vars:
    - name: ansible_password
    - name: ansible_ssh_pass
    - name: ansible_ssh_password
    - name: ansible_netconf_password
  private_key_file:
    description:
    - The private SSH key or certificate file used to authenticate to the remote device
      when first establishing the SSH connection.
    ini:
    - section: defaults
      key: private_key_file
    env:
    - name: ANSIBLE_PRIVATE_KEY_FILE
    vars:
    - name: ansible_private_key_file
  look_for_keys:
    default: true
    description:
    - Enables looking for ssh keys in the usual locations for ssh keys (e.g. :file:`~/.ssh/id_*`).
    env:
    - name: ANSIBLE_PARAMIKO_LOOK_FOR_KEYS
    ini:
    - section: paramiko_connection
      key: look_for_keys
    type: boolean
  host_key_checking:
    description: Set this to "False" if you want to avoid host key checking by the
      underlying tools Ansible uses to connect to the host
    type: boolean
    default: true
    env:
    - name: ANSIBLE_HOST_KEY_CHECKING
    - name: ANSIBLE_SSH_HOST_KEY_CHECKING
    - name: ANSIBLE_NETCONF_HOST_KEY_CHECKING
    ini:
    - section: defaults
      key: host_key_checking
    - section: paramiko_connection
      key: host_key_checking
    vars:
    - name: ansible_host_key_checking
    - name: ansible_ssh_host_key_checking
    - name: ansible_netconf_host_key_checking
  proxy_command:
    default: ''
    description:
      - Proxy information for running the connection via a jumphost.
      - This requires ncclient >= 0.6.10 to be installed on the controller.
    env:
      - name: ANSIBLE_NETCONF_PROXY_COMMAND
    ini:
      - {key: proxy_command, section: paramiko_connection}
    vars:
      - name: ansible_paramiko_proxy_command
      - name: ansible_netconf_proxy_command
  netconf_ssh_config:
    description:
    - This variable is used to enable bastion/jump host with netconf connection. If
      set to True the bastion/jump host ssh settings should be present in ~/.ssh/config
      file, alternatively it can be set to custom ssh configuration file path to read
      the bastion/jump host settings.
    ini:
    - section: netconf_connection
      key: ssh_config
    env:
    - name: ANSIBLE_NETCONF_SSH_CONFIG
    vars:
    - name: ansible_netconf_ssh_config
"""

import os

from ansible_collections.ansible.netcommon.plugins.connection.netconf import (
    Connection as RealConnection,
)
from ansible_collections.ansible.netcommon.plugins.plugin_utils.test_connection import (
    TestConnection,
    record_response,
    compare_response,
)


class Connection(TestConnection, RealConnection):
    def exec_command(self, command, *args, **kwargs):
        # Check for testing
        if self.get_option("test_parameters").get("mode") == "playback":
            return self._send_playback(command)
        response = super(Connection, self).exec_command(
            command,
            *args,
            **kwargs,
        )

        test_parameters = self.get_option("test_parameters")
        if not test_parameters:
            return response

        self._send_sequence += 1

        fixture_file = os.path.join(
            test_parameters["fixture_directory"],
            "%s.json" % self._send_sequence,
        )

        if test_parameters["mode"] == "record":
            record_response(command, response, fixture_file, test_parameters)
        elif test_parameters["mode"] == "compare":
            compare_response(command, response, fixture_file, test_parameters)

        return response
