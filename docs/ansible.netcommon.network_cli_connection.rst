
.. Created with antsibull-docs 2.9.0

ansible.netcommon.network_cli connection -- Use network\_cli to run command on network appliances
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This connection plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.
You need further requirements to be able to use this connection plugin,
see `Requirements <ansible_collections.ansible.netcommon.network_cli_connection_requirements_>`_ for details.

To use it in a playbook, specify: ``ansible.netcommon.network_cli``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This connection plugin provides a connection to remote devices over the SSH and implements a CLI shell.  This connection plugin is typically used by network devices for sending and receiving CLi commands to network devices.



.. _ansible_collections.ansible.netcommon.network_cli_connection_requirements:

Requirements
------------
The below requirements are needed on the local controller node that executes this connection.

- ansible-pylibssh if using \ :emphasis:`ssh\_type=libssh`\






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
      <div class="ansibleOptionAnchor" id="parameter-become"></div>
      <p style="display: inline;"><strong>become</strong></p>
      <a class="ansibleOptionLink" href="#parameter-become" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>The become option will instruct the CLI session to attempt privilege escalation on platforms that support it.  Normally this means transitioning from user mode to <code class='docutils literal notranslate'>enable</code> mode in the CLI session. If become is set to True and the remote device does not support privilege escalation or the privilege has already been elevated, then this option is silently ignored.</p>
      <p>Can be configured from the CLI via the <code class='docutils literal notranslate'>--become</code> or <code class='docutils literal notranslate'>-b</code> options.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[privilege_escalation]
  become = false</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_BECOME</code></p>

      </li>
      <li>
        <p>Variable: ansible_become</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-become_errors"></div>
      <p style="display: inline;"><strong>become_errors</strong></p>
      <a class="ansibleOptionLink" href="#parameter-become_errors" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>This option determines how privilege escalation failures are handled when <em>become</em> is enabled.</p>
      <p>When set to <code class='docutils literal notranslate'>ignore</code>, the errors are silently ignored. When set to <code class='docutils literal notranslate'>warn</code>, a warning message is displayed. The default option <code class='docutils literal notranslate'>fail</code>, triggers a failure and halts execution.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;ignore&#34;</code></p></li>
        <li><p><code>&#34;warn&#34;</code></p></li>
        <li><p><code style="color: blue;"><b>&#34;fail&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_network_become_errors</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-become_method"></div>
      <p style="display: inline;"><strong>become_method</strong></p>
      <a class="ansibleOptionLink" href="#parameter-become_method" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>This option allows the become method to be specified in for handling privilege escalation.  Typically the become_method value is set to <code class='docutils literal notranslate'>enable</code> but could be defined as other values.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;sudo&#34;</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[privilege_escalation]
  become_method = sudo</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_BECOME_METHOD</code></p>

      </li>
      <li>
        <p>Variable: ansible_become_method</p>

      </li>
      </ul>
    </td>
  </tr>
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
      <div class="ansibleOptionAnchor" id="parameter-host_key_auto_add"></div>
      <p style="display: inline;"><strong>host_key_auto_add</strong></p>
      <a class="ansibleOptionLink" href="#parameter-host_key_auto_add" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>By default, Ansible will prompt the user before adding SSH keys to the known hosts file.  Since persistent connections such as network_cli run in background processes, the user will never be prompted.  By enabling this option, unknown host keys will automatically be added to the known hosts file.</p>
      <p>Be sure to fully understand the security implications of enabling this option on production systems as it could create a security vulnerability.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[paramiko_connection]
  host_key_auto_add = false</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_HOST_KEY_AUTO_ADD</code></p>

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

        <pre>[persistent_connection]
  host_key_checking = true</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_HOST_KEY_CHECKING</code></p>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_SSH_HOST_KEY_CHECKING</code></p>

      </li>
      <li>
        <p>Variable: ansible_host_key_checking</p>

      </li>
      <li>
        <p>Variable: ansible_ssh_host_key_checking</p>

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
      <div class="ansibleOptionAnchor" id="parameter-network_cli_retries"></div>
      <p style="display: inline;"><strong>network_cli_retries</strong></p>
      <a class="ansibleOptionLink" href="#parameter-network_cli_retries" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>

    </td>
    <td valign="top">
      <p>Number of attempts to connect to remote host. The delay time between the retires increases after every attempt by power of 2 in seconds till either the maximum attempts are exhausted or any of the <code class='docutils literal notranslate'>persistent_command_timeout</code> or <code class='docutils literal notranslate'>persistent_connect_timeout</code> timers are triggered.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">3</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[persistent_connection]
  network_cli_retries = 3</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_NETWORK_CLI_RETRIES</code></p>

      </li>
      <li>
        <p>Variable: ansible_network_cli_retries</p>

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
      <p>Configures the device platform network operating system.  This value is used to load the correct terminal and cliconf plugins to communicate with the remote device.</p>
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
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-persistent_buffer_read_timeout"></div>
      <p style="display: inline;"><strong>persistent_buffer_read_timeout</strong></p>
      <a class="ansibleOptionLink" href="#parameter-persistent_buffer_read_timeout" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">float</span>
      </p>

    </td>
    <td valign="top">
      <p>Configures, in seconds, the amount of time to wait for the data to be read from Paramiko channel after the command prompt is matched. This timeout value ensures that command prompt matched is correct and there is no more data left to be received from remote host.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">0.1</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[persistent_connection]
  buffer_read_timeout = 0.1</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_PERSISTENT_BUFFER_READ_TIMEOUT</code></p>

      </li>
      <li>
        <p>Variable: ansible_buffer_read_timeout</p>

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
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">22</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[defaults]
  remote_port = 22</pre>

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
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-single_user_mode"></div>
      <p style="display: inline;"><strong>single_user_mode</strong></p>
      <a class="ansibleOptionLink" href="#parameter-single_user_mode" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ansible.netcommon 2.0.0</i></p>

    </td>
    <td valign="top">
      <p>This option enables caching of data fetched from the target for re-use. The cache is invalidated when the target device enters configuration mode.</p>
      <p>Applicable only for platforms where this has been implemented.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Environment variable: <code>ANSIBLE_NETWORK_SINGLE_USER_MODE</code></p>

      </li>
      <li>
        <p>Variable: ansible_network_single_user_mode</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-ssh_type"></div>
      <p style="display: inline;"><strong>ssh_type</strong></p>
      <a class="ansibleOptionLink" href="#parameter-ssh_type" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>The python package that will be used by the <code class='docutils literal notranslate'>network_cli</code> connection plugin to create a SSH connection to remote host.</p>
      <p><em>libssh</em> will use the ansible-pylibssh package, which needs to be installed in order to work.</p>
      <p><em>paramiko</em> will instead use the paramiko package to manage the SSH connection.</p>
      <p><em>auto</em> will use ansible-pylibssh if that package is installed, otherwise will fallback to paramiko.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;libssh&#34;</code></p></li>
        <li><p><code>&#34;paramiko&#34;</code></p></li>
        <li><p><code style="color: blue;"><b>&#34;auto&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[persistent_connection]
  ssh_type = auto</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_NETWORK_CLI_SSH_TYPE</code></p>

      </li>
      <li>
        <p>Variable: ansible_network_cli_ssh_type</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-terminal_errors"></div>
      <p style="display: inline;"><strong>terminal_errors</strong></p>
      <a class="ansibleOptionLink" href="#parameter-terminal_errors" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ansible.netcommon 3.1.0</i></p>

    </td>
    <td valign="top">
      <p>This option determines how failures while setting terminal parameters are handled.</p>
      <p>When set to <code class='docutils literal notranslate'>ignore</code>, the errors are silently ignored. When set to <code class='docutils literal notranslate'>warn</code>, a warning message is displayed. The default option <code class='docutils literal notranslate'>fail</code>, triggers a failure and halts execution.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;ignore&#34;</code></p></li>
        <li><p><code>&#34;warn&#34;</code></p></li>
        <li><p><code style="color: blue;"><b>&#34;fail&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_network_terminal_errors</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-terminal_inital_prompt_newline"></div>
      <p style="display: inline;"><strong>terminal_inital_prompt_newline</strong></p>
      <a class="ansibleOptionLink" href="#parameter-terminal_inital_prompt_newline" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>This boolean flag, that when set to <em>True</em> will send newline in the response if any of values in <em>terminal_initial_prompt</em> is matched.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code style="color: blue;"><b>true</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_terminal_initial_prompt_newline</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-terminal_initial_answer"></div>
      <p style="display: inline;"><strong>terminal_initial_answer</strong></p>
      <a class="ansibleOptionLink" href="#parameter-terminal_initial_answer" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>

    </td>
    <td valign="top">
      <p>The answer to reply with if the <code class='docutils literal notranslate'>terminal_initial_prompt</code> is matched. The value can be a single answer or a list of answers for multiple terminal_initial_prompt. In case the login menu has multiple prompts the sequence of the prompt and excepted answer should be in same order and the value of <em>terminal_prompt_checkall</em> should be set to <em>True</em> if all the values in <code class='docutils literal notranslate'>terminal_initial_prompt</code> are expected to be matched and set to <em>False</em> if any one login prompt is to be matched.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_terminal_initial_answer</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-terminal_initial_prompt"></div>
      <p style="display: inline;"><strong>terminal_initial_prompt</strong></p>
      <a class="ansibleOptionLink" href="#parameter-terminal_initial_prompt" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>

    </td>
    <td valign="top">
      <p>A single regex pattern or a sequence of patterns to evaluate the expected prompt at the time of initial login to the remote host.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_terminal_initial_prompt</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-terminal_initial_prompt_checkall"></div>
      <p style="display: inline;"><strong>terminal_initial_prompt_checkall</strong></p>
      <a class="ansibleOptionLink" href="#parameter-terminal_initial_prompt_checkall" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>By default the value is set to <em>False</em> and any one of the prompts mentioned in <code class='docutils literal notranslate'>terminal_initial_prompt</code> option is matched it won&#x27;t check for other prompts. When set to <em>True</em> it will check for all the prompts mentioned in <code class='docutils literal notranslate'>terminal_initial_prompt</code> option in the given order and all the prompts should be received from remote host if not it will result in timeout.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_terminal_initial_prompt_checkall</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-terminal_stderr_re"></div>
      <p style="display: inline;"><strong>terminal_stderr_re</strong></p>
      <a class="ansibleOptionLink" href="#parameter-terminal_stderr_re" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=dictionary</span>
      </p>

    </td>
    <td valign="top">
      <p>This option provides the regex pattern and optional flags to match the error string from the received response chunk. This option accepts <code class='docutils literal notranslate'>pattern</code> and <code class='docutils literal notranslate'>flags</code> keys. The value of <code class='docutils literal notranslate'>pattern</code> is a python regex pattern to match the response and the value of <code class='docutils literal notranslate'>flags</code> is the value accepted by <em>flags</em> argument of <em>re.compile</em> python method to control the way regex is matched with the response, for example <em>&#x27;re.I&#x27;</em>.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_terminal_stderr_re</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-terminal_stdout_re"></div>
      <p style="display: inline;"><strong>terminal_stdout_re</strong></p>
      <a class="ansibleOptionLink" href="#parameter-terminal_stdout_re" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=dictionary</span>
      </p>

    </td>
    <td valign="top">
      <p>A single regex pattern or a sequence of patterns along with optional flags to match the command prompt from the received response chunk. This option accepts <code class='docutils literal notranslate'>pattern</code> and <code class='docutils literal notranslate'>flags</code> keys. The value of <code class='docutils literal notranslate'>pattern</code> is a python regex pattern to match the response and the value of <code class='docutils literal notranslate'>flags</code> is the value accepted by <em>flags</em> argument of <em>re.compile</em> python method to control the way regex is matched with the response, for example <em>&#x27;re.I&#x27;</em>.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_terminal_stdout_re</p>

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
