
.. Created with antsibull-docs 2.9.0

ansible.netcommon.netconf connection -- Provides a persistent connection using the netconf protocol
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This connection plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.
You need further requirements to be able to use this connection plugin,
see `Requirements <ansible_collections.ansible.netcommon.netconf_connection_requirements_>`_ for details.

To use it in a playbook, specify: ``ansible.netcommon.netconf``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This connection plugin provides a connection to remote devices over the SSH NETCONF subsystem.  This connection plugin is typically used by network devices for sending and receiving RPC calls over NETCONF.
- Note this connection plugin requires ncclient to be installed on the local Ansible controller.



.. _ansible_collections.ansible.netcommon.netconf_connection_requirements:

Requirements
------------
The below requirements are needed on the local controller node that executes this connection.

- ncclient






Parameters
----------

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-host"></div>
      <p style="display: inline;"><strong>host</strong></p>
      <a class="ansibleOptionLink" href="#parameter-host" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Specifies the remote device FQDN or IP address to establish the SSH connection to.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;inventory_hostname&#34;</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: inventory_hostname</p>

      </li>
      <li>
        <p>Variable: ansible_host</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-host_key_checking"></div>
      <p style="display: inline;"><strong>host_key_checking</strong></p>
      <a class="ansibleOptionLink" href="#parameter-host_key_checking" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>Set this to "False" if you want to avoid host key checking by the underlying tools Ansible uses to connect to the host</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code style="color: blue;"><b>true</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entries</p>
        <pre>[defaults]
  host_key_checking = true</pre>

        <pre>[paramiko_connection]
  host_key_checking = true</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_HOST_KEY_CHECKING</code></p>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_SSH_HOST_KEY_CHECKING</code></p>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_NETCONF_HOST_KEY_CHECKING</code></p>

      </li>
      <li>
        <p>Variable: ansible_host_key_checking</p>

      </li>
      <li>
        <p>Variable: ansible_ssh_host_key_checking</p>

      </li>
      <li>
        <p>Variable: ansible_netconf_host_key_checking</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-import_modules"></div>
      <p style="display: inline;"><strong>import_modules</strong></p>
      <a class="ansibleOptionLink" href="#parameter-import_modules" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>Reduce CPU usage and network module execution time by enabling direct execution. Instead of the module being packaged and executed by the shell, it will be directly executed by the Ansible control node using the same python interpreter as the Ansible process. Note- Incompatible with <code class='docutils literal notranslate'>asynchronous mode</code>. Note- Python 3 and Ansible 2.9.16 or greater required. Note- With Ansible 2.9.x fully qualified modules names are required in tasks.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code style="color: blue;"><b>true</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[ansible_network]
  import_modules = true</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_NETWORK_IMPORT_MODULES</code></p>

      </li>
      <li>
        <p>Variable: ansible_network_import_modules</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-look_for_keys"></div>
      <p style="display: inline;"><strong>look_for_keys</strong></p>
      <a class="ansibleOptionLink" href="#parameter-look_for_keys" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>Enables looking for ssh keys in the usual locations for ssh keys (e.g. :file:`~/.ssh/id_*`).</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code style="color: blue;"><b>true</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[paramiko_connection]
  look_for_keys = true</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_PARAMIKO_LOOK_FOR_KEYS</code></p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-netconf_ssh_config"></div>
      <p style="display: inline;"><strong>netconf_ssh_config</strong></p>
      <a class="ansibleOptionLink" href="#parameter-netconf_ssh_config" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>This variable is used to enable bastion/jump host with netconf connection. If set to True the bastion/jump host ssh settings should be present in ~/.ssh/config file, alternatively it can be set to custom ssh configuration file path to read the bastion/jump host settings.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[netconf_connection]
  ssh_config = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_NETCONF_SSH_CONFIG</code></p>

      </li>
      <li>
        <p>Variable: ansible_netconf_ssh_config</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-network_os"></div>
      <p style="display: inline;"><strong>network_os</strong></p>
      <a class="ansibleOptionLink" href="#parameter-network_os" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Configures the device platform network operating system.  This value is used to load a device specific netconf plugin.  If this option is not configured (or set to <code class='docutils literal notranslate'>auto</code>), then Ansible will attempt to guess the correct network_os to use. If it can not guess a network_os correctly it will use <code class='docutils literal notranslate'>default</code>.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_network_os</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-password"></div>
      <p style="display: inline;"><strong>password</strong></p>
      <a class="ansibleOptionLink" href="#parameter-password" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Configures the user password used to authenticate to the remote device when first establishing the SSH connection.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_password</p>

      </li>
      <li>
        <p>Variable: ansible_ssh_pass</p>

      </li>
      <li>
        <p>Variable: ansible_ssh_password</p>

      </li>
      <li>
        <p>Variable: ansible_netconf_password</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-persistent_command_timeout"></div>
      <p style="display: inline;"><strong>persistent_command_timeout</strong></p>
      <a class="ansibleOptionLink" href="#parameter-persistent_command_timeout" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>

    </td>
    <td valign="top">
      <p>Configures, in seconds, the amount of time to wait for a command to return from the remote device.  If this timer is exceeded before the command returns, the connection plugin will raise an exception and close.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">30</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[persistent_connection]
  command_timeout = 30</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_PERSISTENT_COMMAND_TIMEOUT</code></p>

      </li>
      <li>
        <p>Variable: ansible_command_timeout</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-persistent_connect_timeout"></div>
      <p style="display: inline;"><strong>persistent_connect_timeout</strong></p>
      <a class="ansibleOptionLink" href="#parameter-persistent_connect_timeout" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>

    </td>
    <td valign="top">
      <p>Configures, in seconds, the amount of time to wait when trying to initially establish a persistent connection.  If this value expires before the connection to the remote device is completed, the connection will fail.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">30</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[persistent_connection]
  connect_timeout = 30</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_PERSISTENT_CONNECT_TIMEOUT</code></p>

      </li>
      <li>
        <p>Variable: ansible_connect_timeout</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-persistent_log_messages"></div>
      <p style="display: inline;"><strong>persistent_log_messages</strong></p>
      <a class="ansibleOptionLink" href="#parameter-persistent_log_messages" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>This flag will enable logging the command executed and response received from target device in the ansible log file. For this option to work &#x27;log_path&#x27; ansible configuration option is required to be set to a file path with write access.</p>
      <p>Be sure to fully understand the security implications of enabling this option as it could create a security vulnerability by logging sensitive information in log file.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[persistent_connection]
  log_messages = false</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_PERSISTENT_LOG_MESSAGES</code></p>

      </li>
      <li>
        <p>Variable: ansible_persistent_log_messages</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-port"></div>
      <p style="display: inline;"><strong>port</strong></p>
      <a class="ansibleOptionLink" href="#parameter-port" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>

    </td>
    <td valign="top">
      <p>Specifies the port on the remote device that listens for connections when establishing the SSH connection.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">830</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[defaults]
  remote_port = 830</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_REMOTE_PORT</code></p>

      </li>
      <li>
        <p>Variable: ansible_port</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-private_key_file"></div>
      <p style="display: inline;"><strong>private_key_file</strong></p>
      <a class="ansibleOptionLink" href="#parameter-private_key_file" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>The private SSH key or certificate file used to authenticate to the remote device when first establishing the SSH connection.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[defaults]
  private_key_file = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_PRIVATE_KEY_FILE</code></p>

      </li>
      <li>
        <p>Variable: ansible_private_key_file</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-proxy_command"></div>
      <p style="display: inline;"><strong>proxy_command</strong></p>
      <a class="ansibleOptionLink" href="#parameter-proxy_command" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Proxy information for running the connection via a jumphost.</p>
      <p>This requires ncclient &gt;= 0.6.10 to be installed on the controller.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;&#34;</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[paramiko_connection]
  proxy_command = &#34;&#34;</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_NETCONF_PROXY_COMMAND</code></p>

      </li>
      <li>
        <p>Variable: ansible_paramiko_proxy_command</p>

      </li>
      <li>
        <p>Variable: ansible_netconf_proxy_command</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-remote_user"></div>
      <p style="display: inline;"><strong>remote_user</strong></p>
      <a class="ansibleOptionLink" href="#parameter-remote_user" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>The username used to authenticate to the remote device when the SSH connection is first established.  If the remote_user is not specified, the connection will use the username of the logged in user.</p>
      <p>Can be configured from the CLI via the <code class='docutils literal notranslate'>--user</code> or <code class='docutils literal notranslate'>-u</code> options.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[defaults]
  remote_user = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_REMOTE_USER</code></p>

      </li>
      <li>
        <p>Variable: ansible_user</p>

      </li>
      </ul>
    </td>
  </tr>
  </tbody>
  </table>











Authors
~~~~~~~

- Ansible Networking Team (@ansible-network)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
