# (c) 2022 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author:
 - Ansible Networking Team (@ansible-network)
name: test_httpapi
short_description: Use httpapi to run command on network appliances
description:
- This connection plugin provides a connection to remote devices over a HTTP(S)-based
  api.
version_added: 3.1.0
extends_documentation_fragment:
- ansible.netcommon.connection_persistent
- ansible.netcommon.test_connection
options:
  host:
    description:
    - Specifies the remote device FQDN or IP address to establish the HTTP(S) connection
      to.
    default: inventory_hostname
    vars:
    - name: ansible_host
  port:
    type: int
    description:
    - Specifies the port on the remote device that listens for connections when establishing
      the HTTP(S) connection.
    - When unspecified, will pick 80 or 443 based on the value of use_ssl.
    ini:
    - section: defaults
      key: remote_port
    env:
    - name: ANSIBLE_REMOTE_PORT
    vars:
    - name: ansible_httpapi_port
  network_os:
    description:
    - Configures the device platform network operating system.  This value is used
      to load the correct httpapi plugin to communicate with the remote device
    vars:
    - name: ansible_network_os
  remote_user:
    description:
    - The username used to authenticate to the remote device when the API connection
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
      needed for the device API.
    vars:
    - name: ansible_password
    - name: ansible_httpapi_pass
    - name: ansible_httpapi_password
  session_key:
    type: dict
    description:
    - Configures the session key to be used to authenticate to the remote device when
      needed for the device API.
    - This should contain a dictionary representing the key name and value for the
      token.
    - When specified, I(password) is ignored.
    vars:
    - name: ansible_httpapi_session_key
  use_ssl:
    type: boolean
    description:
    - Whether to connect using SSL (HTTPS) or not (HTTP).
    default: false
    vars:
    - name: ansible_httpapi_use_ssl
  validate_certs:
    type: boolean
    description:
    - Whether to validate SSL certificates
    default: true
    vars:
    - name: ansible_httpapi_validate_certs
  use_proxy:
    type: boolean
    description:
    - Whether to use https_proxy for requests.
    default: true
    vars:
    - name: ansible_httpapi_use_proxy
  become:
    type: boolean
    description:
    - The become option will instruct the CLI session to attempt privilege escalation
      on platforms that support it.  Normally this means transitioning from user mode
      to C(enable) mode in the CLI session. If become is set to True and the remote
      device does not support privilege escalation or the privilege has already been
      elevated, then this option is silently ignored.
    - Can be configured from the CLI via the C(--become) or C(-b) options.
    default: false
    ini:
    - section: privilege_escalation
      key: become
    env:
    - name: ANSIBLE_BECOME
    vars:
    - name: ansible_become
  become_method:
    description:
    - This option allows the become method to be specified in for handling privilege
      escalation.  Typically the become_method value is set to C(enable) but could
      be defined as other values.
    default: sudo
    ini:
    - section: privilege_escalation
      key: become_method
    env:
    - name: ANSIBLE_BECOME_METHOD
    vars:
    - name: ansible_become_method
  platform_type:
    description:
    - Set type of platform.
    env:
    - name: ANSIBLE_PLATFORM_TYPE
    vars:
    - name: ansible_platform_type
"""

import os

from ansible_collections.ansible.netcommon.plugins.connection.httpapi import (
    Connection as RealConnection,
)
from ansible_collections.ansible.netcommon.plugins.plugin_utils.test_connection import (
    TestConnection,
    record_response,
    compare_response,
)


class Connection(TestConnection, RealConnection):
    def send(self, path, data, *args, **kwarg):
        # This should be good enough to make a key
        command = "\n".join([path, data])
        # Check for testing
        if self.get_option("test_parameters").get("mode") == "playback":
            return self._send_playback(command)
        response = super(Connection, self).send(
            path,
            data,
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
