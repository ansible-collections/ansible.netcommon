# (c) 2016 Red Hat Inc.
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

DOCUMENTATION = """
author:
 - Ansible Networking Team (@ansible-network)
name: netconf
short_description: Provides a persistent connection using the netconf protocol
description:
- This connection plugin provides a connection to remote devices over the SSH NETCONF
  subsystem.  This connection plugin is typically used by network devices for sending
  and receiving RPC calls over NETCONF.
- Note this connection plugin requires ncclient to be installed on the local Ansible
  controller.
version_added: 1.0.0
requirements:
- ncclient
extends_documentation_fragment:
- ansible.netcommon.connection_persistent
options:
  host:
    description:
    - Specifies the remote device FQDN or IP address to establish the SSH connection
      to.
    default: inventory_hostname
    type: string
    vars:
    - name: inventory_hostname
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
    type: string
    vars:
    - name: ansible_network_os
  remote_user:
    description:
    - The username used to authenticate to the remote device when the SSH connection
      is first established.  If the remote_user is not specified, the connection will
      use the username of the logged in user.
    - Can be configured from the CLI via the C(--user) or C(-u) options.
    type: string
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
    type: string
    vars:
    - name: ansible_password
    - name: ansible_ssh_pass
    - name: ansible_ssh_password
    - name: ansible_netconf_password
  private_key_file:
    description:
    - The private SSH key or certificate file used to authenticate to the remote device
      when first establishing the SSH connection.
    type: string
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
    type: string
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
    type: string
    ini:
    - section: netconf_connection
      key: ssh_config
    env:
    - name: ANSIBLE_NETCONF_SSH_CONFIG
    vars:
    - name: ansible_netconf_ssh_config
"""

import json
import logging
import os

from ansible.errors import AnsibleConnectionFailure, AnsibleError
from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.parsing.convert_bool import BOOLEANS_FALSE, BOOLEANS_TRUE
from ansible.module_utils.six import PY3
from ansible.module_utils.six.moves import cPickle
from ansible.playbook.play_context import PlayContext
from ansible.plugins.connection import ensure_connect
from ansible.plugins.loader import netconf_loader

from ansible_collections.ansible.netcommon.plugins.plugin_utils.connection_base import (
    NetworkConnectionBase,
)
from ansible_collections.ansible.netcommon.plugins.plugin_utils.version import Version


try:
    from ncclient import __version__ as NCCLIENT_VERSION
    from ncclient import manager
    from ncclient.operations import RPCError
    from ncclient.transport.errors import AuthenticationError, SSHUnknownHostError
    from ncclient.xml_ import to_ele, to_xml
    from paramiko import ProxyCommand

    HAS_NCCLIENT = True
    NCCLIENT_IMP_ERR = None
# paramiko and gssapi are incompatible and raise AttributeError not ImportError
# When running in FIPS mode, cryptography raises InternalError
# https://bugzilla.redhat.com/show_bug.cgi?id=1778939
except Exception as err:
    HAS_NCCLIENT = False
    NCCLIENT_IMP_ERR = err

logging.getLogger("ncclient").setLevel(logging.INFO)


class Connection(NetworkConnectionBase):
    """NetConf connections"""

    transport = "ansible.netcommon.netconf"
    has_pipelining = False

    def __init__(self, play_context, new_stdin, *args, **kwargs):
        super(Connection, self).__init__(play_context, new_stdin, *args, **kwargs)

        # If network_os is not specified then set the network os to auto
        # This will be used to trigger the use of guess_network_os when connecting.
        self._network_os = self._network_os or "auto"

        self.netconf = netconf_loader.get(self._network_os, self)
        if self.netconf:
            self._sub_plugin = {
                "type": "netconf",
                "name": self.netconf._load_name,
                "obj": self.netconf,
            }
            self.queue_message(
                "vvvv",
                "loaded netconf plugin %s from path %s for network_os %s"
                % (
                    self.netconf._load_name,
                    self.netconf._original_path,
                    self._network_os,
                ),
            )
        else:
            self.netconf = netconf_loader.get("default", self)
            self._sub_plugin = {
                "type": "netconf",
                "name": "default",
                "obj": self.netconf,
            }
            self.queue_message(
                "vvvv",
                "unable to load netconf plugin for network_os %s, falling back to default plugin"
                % self._network_os,
            )

        self.queue_message("log", "network_os is set to %s" % self._network_os)
        self._manager = None
        self.key_filename = None
        self._ssh_config = None

    def exec_command(self, cmd, in_data=None, sudoable=True):
        """Sends the request to the node and returns the reply
        The method accepts two forms of request.  The first form is as a byte
        string that represents xml string be send over netconf session.
        The second form is a json-rpc (2.0) byte string.
        """
        if self._manager:
            # to_ele operates on native strings
            request = to_ele(to_native(cmd, errors="surrogate_or_strict"))

            if request is None:
                return "unable to parse request"

            try:
                reply = self._manager.rpc(request)
            except RPCError as exc:
                error = self.internal_error(
                    data=to_text(to_xml(exc.xml), errors="surrogate_or_strict")
                )
                return json.dumps(error)

            return reply.data_xml
        else:
            return super(Connection, self).exec_command(cmd, in_data, sudoable)

    def update_play_context(self, pc_data):
        """Updates the play context information for the connection"""
        pc_data = to_bytes(pc_data)
        if PY3:
            pc_data = cPickle.loads(pc_data, encoding="bytes")
        else:
            pc_data = cPickle.loads(pc_data)
        play_context = PlayContext()
        play_context.deserialize(pc_data)
        self._play_context = play_context

    @property
    @ensure_connect
    def manager(self):
        return self._manager

    def _get_proxy_command(self, port=22):
        proxy_command = None

        # TO-DO: Add logic to scan ssh_* args to read ProxyCommand

        proxy_command = self.get_option("proxy_command")

        sock = None
        if proxy_command:
            if Version(NCCLIENT_VERSION) < "0.6.10":
                raise AnsibleError(
                    "Configuring jumphost settings through ProxyCommand is unsupported in ncclient version %s. "
                    "Please upgrade to ncclient 0.6.10 or newer." % NCCLIENT_VERSION
                )

            replacers = {
                "%h": self._play_context.remote_addr,
                "%p": port,
                "%r": self._play_context.remote_user,
            }

            for find, replace in replacers.items():
                proxy_command = proxy_command.replace(find, str(replace))
            sock = ProxyCommand(proxy_command)

        return sock

    def _connect(self):
        if not HAS_NCCLIENT:
            raise AnsibleError(
                "%s: %s"
                % (
                    missing_required_lib("ncclient"),
                    to_native(NCCLIENT_IMP_ERR),
                )
            )

        self.queue_message("log", "ssh connection done, starting ncclient")

        allow_agent = True
        if self._play_context.password is not None:
            allow_agent = False
        setattr(self._play_context, "allow_agent", allow_agent)

        self.key_filename = self._play_context.private_key_file or self.get_option(
            "private_key_file"
        )
        if self.key_filename:
            self.key_filename = str(os.path.expanduser(self.key_filename))

        self._ssh_config = self.get_option("netconf_ssh_config")
        if self._ssh_config in BOOLEANS_TRUE:
            self._ssh_config = True
        elif self._ssh_config in BOOLEANS_FALSE:
            self._ssh_config = None

        # Try to guess the network_os if the network_os is set to auto
        if self._network_os == "auto":
            for cls in netconf_loader.all(class_only=True):
                network_os = cls.guess_network_os(self)
                if network_os:
                    self.queue_message("vvv", "discovered network_os %s" % network_os)
                    self._network_os = network_os

        # If we have tried to detect the network_os but were unable to i.e. network_os is still 'auto'
        # then use default as the network_os

        if self._network_os == "auto":
            # Network os not discovered. Set it to default
            self.queue_message(
                "vvv",
                "Unable to discover network_os. Falling back to default.",
            )
            self._network_os = "default"
        try:
            ncclient_device_handler = self.netconf.get_option("ncclient_device_handler")
        except KeyError:
            ncclient_device_handler = "default"
        self.queue_message(
            "vvv",
            "identified ncclient device handler: %s." % ncclient_device_handler,
        )
        device_params = {"name": ncclient_device_handler}

        try:
            port = self._play_context.port or 830
            self.queue_message(
                "vvv",
                "ESTABLISH NETCONF SSH CONNECTION FOR USER: %s on PORT %s TO %s WITH SSH_CONFIG = %s"
                % (
                    self._play_context.remote_user,
                    port,
                    self._play_context.remote_addr,
                    self._ssh_config,
                ),
            )

            params = dict(
                host=self._play_context.remote_addr,
                port=port,
                username=self._play_context.remote_user,
                password=self._play_context.password,
                key_filename=self.key_filename,
                hostkey_verify=self.get_option("host_key_checking"),
                look_for_keys=self.get_option("look_for_keys"),
                device_params=device_params,
                allow_agent=self._play_context.allow_agent,
                timeout=self.get_option("persistent_connect_timeout"),
                ssh_config=self._ssh_config,
            )
            # sock is only supported by ncclient >= 0.6.10, and will error if
            # included on older versions. We check the version in
            # _get_proxy_command, so if this returns a value, the version is
            # fine and we have something to send. Otherwise, don't even send
            # the option to support older versions of ncclient
            sock = self._get_proxy_command(port)
            if sock:
                params["sock"] = sock

            self._manager = manager.connect(**params)

            self._manager._timeout = self.get_option("persistent_command_timeout")
        except SSHUnknownHostError as exc:
            raise AnsibleConnectionFailure(to_native(exc))
        except AuthenticationError as exc:
            if str(exc).startswith("FileNotFoundError"):
                raise AnsibleError(
                    "Encountered FileNotFoundError in ncclient connect. Does {0} exist?".format(
                        self.key_filename
                    )
                )
            raise
        except ImportError:
            raise AnsibleError(
                "connection=netconf is not supported on {0}".format(self._network_os)
            )

        if not self._manager.connected:
            return 1, b"", b"not connected"

        self.queue_message("log", "ncclient manager object created successfully")

        self._connected = True

        super(Connection, self)._connect()

        return (
            0,
            to_bytes(self._manager.session_id, errors="surrogate_or_strict"),
            b"",
        )

    def close(self):
        if self._manager and self._manager.connected:
            self._manager.close_session()
        super(Connection, self).close()
