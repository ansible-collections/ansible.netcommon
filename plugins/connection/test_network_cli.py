# (c) 2022 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author:
 - Ansible Networking Team (@ansible-network)
name: test_network_cli
short_description: Use network_cli to run command on network appliances
description:
- This connection plugin provides a connection to remote devices over the SSH and
  implements a CLI shell.  This connection plugin is typically used by network devices
  for sending and receiving CLi commands to network devices.
version_added: 3.1.0
requirements:
- ansible-pylibssh if using I(ssh_type=libssh)
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
    default: 22
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
      to load the correct terminal and cliconf plugins to communicate with the remote
      device.
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
  become_errors:
    type: str
    description:
    - This option determines how privilege escalation failures are handled when
      I(become) is enabled.
    - When set to C(ignore), the errors are silently ignored.
      When set to C(warn), a warning message is displayed.
      The default option C(fail), triggers a failure and halts execution.
    vars:
    - name: ansible_network_become_errors
    default: fail
    choices: ["ignore", "warn", "fail"]
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
  host_key_auto_add:
    type: boolean
    description:
    - By default, Ansible will prompt the user before adding SSH keys to the known
      hosts file.  Since persistent connections such as network_cli run in background
      processes, the user will never be prompted.  By enabling this option, unknown
      host keys will automatically be added to the known hosts file.
    - Be sure to fully understand the security implications of enabling this option
      on production systems as it could create a security vulnerability.
    default: false
    ini:
    - section: paramiko_connection
      key: host_key_auto_add
    env:
    - name: ANSIBLE_HOST_KEY_AUTO_ADD
  persistent_buffer_read_timeout:
    type: float
    description:
    - Configures, in seconds, the amount of time to wait for the data to be read from
      Paramiko channel after the command prompt is matched. This timeout value ensures
      that command prompt matched is correct and there is no more data left to be
      received from remote host.
    default: 0.1
    ini:
    - section: persistent_connection
      key: buffer_read_timeout
    env:
    - name: ANSIBLE_PERSISTENT_BUFFER_READ_TIMEOUT
    vars:
    - name: ansible_buffer_read_timeout
  terminal_stdout_re:
    type: list
    elements: dict
    description:
    - A single regex pattern or a sequence of patterns along with optional flags to
      match the command prompt from the received response chunk. This option accepts
      C(pattern) and C(flags) keys. The value of C(pattern) is a python regex pattern
      to match the response and the value of C(flags) is the value accepted by I(flags)
      argument of I(re.compile) python method to control the way regex is matched
      with the response, for example I('re.I').
    vars:
    - name: ansible_terminal_stdout_re
  terminal_stderr_re:
    type: list
    elements: dict
    description:
    - This option provides the regex pattern and optional flags to match the error
      string from the received response chunk. This option accepts C(pattern) and
      C(flags) keys. The value of C(pattern) is a python regex pattern to match the
      response and the value of C(flags) is the value accepted by I(flags) argument
      of I(re.compile) python method to control the way regex is matched with the
      response, for example I('re.I').
    vars:
    - name: ansible_terminal_stderr_re
  terminal_initial_prompt:
    type: list
    elements: string
    description:
    - A single regex pattern or a sequence of patterns to evaluate the expected prompt
      at the time of initial login to the remote host.
    vars:
    - name: ansible_terminal_initial_prompt
  terminal_initial_answer:
    type: list
    elements: string
    description:
    - The answer to reply with if the C(terminal_initial_prompt) is matched. The value
      can be a single answer or a list of answers for multiple terminal_initial_prompt.
      In case the login menu has multiple prompts the sequence of the prompt and excepted
      answer should be in same order and the value of I(terminal_prompt_checkall)
      should be set to I(True) if all the values in C(terminal_initial_prompt) are
      expected to be matched and set to I(False) if any one login prompt is to be
      matched.
    vars:
    - name: ansible_terminal_initial_answer
  terminal_initial_prompt_checkall:
    type: boolean
    description:
    - By default the value is set to I(False) and any one of the prompts mentioned
      in C(terminal_initial_prompt) option is matched it won't check for other prompts.
      When set to I(True) it will check for all the prompts mentioned in C(terminal_initial_prompt)
      option in the given order and all the prompts should be received from remote
      host if not it will result in timeout.
    default: false
    vars:
    - name: ansible_terminal_initial_prompt_checkall
  terminal_inital_prompt_newline:
    type: boolean
    description:
    - This boolean flag, that when set to I(True) will send newline in the response
      if any of values in I(terminal_initial_prompt) is matched.
    default: true
    vars:
    - name: ansible_terminal_initial_prompt_newline
  network_cli_retries:
    description:
    - Number of attempts to connect to remote host. The delay time between the retires
      increases after every attempt by power of 2 in seconds till either the maximum
      attempts are exhausted or any of the C(persistent_command_timeout) or C(persistent_connect_timeout)
      timers are triggered.
    default: 3
    type: integer
    env:
    - name: ANSIBLE_NETWORK_CLI_RETRIES
    ini:
    - section: persistent_connection
      key: network_cli_retries
    vars:
    - name: ansible_network_cli_retries
  ssh_type:
    description:
      - The python package that will be used by the C(network_cli) connection plugin to create a SSH connection to remote host.
      - I(libssh) will use the ansible-pylibssh package, which needs to be installed in order to work.
      - I(paramiko) will instead use the paramiko package to manage the SSH connection.
      - I(auto) will use ansible-pylibssh if that package is installed, otherwise will fallback to paramiko.
    default: auto
    choices: ["libssh", "paramiko", "auto"]
    env:
        - name: ANSIBLE_NETWORK_CLI_SSH_TYPE
    ini:
        - section: persistent_connection
          key: ssh_type
    vars:
    - name: ansible_network_cli_ssh_type
  host_key_checking:
    description: 'Set this to "False" if you want to avoid host key checking by the underlying tools Ansible uses to connect to the host'
    type: boolean
    default: True
    env:
    - name: ANSIBLE_HOST_KEY_CHECKING
    - name: ANSIBLE_SSH_HOST_KEY_CHECKING
    ini:
    - section: defaults
      key: host_key_checking
    - section: persistent_connection
      key: host_key_checking
    vars:
    - name: ansible_host_key_checking
    - name: ansible_ssh_host_key_checking
  single_user_mode:
    type: boolean
    default: false
    version_added: 2.0.0
    description:
    - This option enables caching of data fetched from the target for re-use.
      The cache is invalidated when the target device enters configuration mode.
    - Applicable only for platforms where this has been implemented.
    env:
    - name: ANSIBLE_NETWORK_SINGLE_USER_MODE
    vars:
    - name: ansible_network_single_user_mode
"""

import os

from ansible_collections.ansible.netcommon.plugins.connection.network_cli import (
    Connection as RealConnection,
)
from ansible_collections.ansible.netcommon.plugins.plugin_utils.test_connection import (
    TestConnection,
    record_response,
    compare_response,
)


class Connection(TestConnection, RealConnection):
    def send(self, command, *args, **kwarg):
        # Check for testing
        if self.get_option("test_parameters").get("mode") == "playback":
            return self._send_playback(command)
        response = super(Connection, self).send(
            command,
            *args,
            **kwargs,
        )
        self._post_send(command, response)

        return response
