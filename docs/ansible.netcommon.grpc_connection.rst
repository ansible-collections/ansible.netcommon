
.. Created with antsibull-docs 2.9.0

ansible.netcommon.grpc connection -- Provides a persistent connection using the gRPC protocol
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This connection plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.
You need further requirements to be able to use this connection plugin,
see `Requirements <ansible_collections.ansible.netcommon.grpc_connection_requirements_>`_ for details.

To use it in a playbook, specify: ``ansible.netcommon.grpc``.

New in ansible.netcommon 3.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This connection plugin provides a connection to remote devices over gRPC and is typically used with devices for sending and receiving RPC calls over gRPC framework.
- Note this connection plugin requires the grpcio python library to be installed on the local Ansible controller.



.. _ansible_collections.ansible.netcommon.grpc_connection_requirements:

Requirements
------------
The below requirements are needed on the local controller node that executes this connection.

- grpcio
- protobuf






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
      <div class="ansibleOptionAnchor" id="parameter-certificate_chain_file"></div>
      <p style="display: inline;"><strong>certificate_chain_file</strong></p>
      <a class="ansibleOptionLink" href="#parameter-certificate_chain_file" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>The PEM encoded certificate chain file used to create a SSL-enabled channel. If the value is None, no certificate chain is used.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[grpc_connection]
  certificate_chain_file = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_CERTIFICATE_CHAIN_FILE</code></p>

      </li>
      <li>
        <p>Variable: ansible_certificate_chain_file</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-grpc_type"></div>
      <p style="display: inline;"><strong>grpc_type</strong></p>
      <a class="ansibleOptionLink" href="#parameter-grpc_type" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>This option indicates the grpc type and it can be used in place of network_os. (example cisco.iosxr.iosxr)</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">false</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[grpc_connection]
  type = false</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_GRPC_CONNECTION_TYPE</code></p>

      </li>
      <li>
        <p>Variable: ansible_grpc_connection_type</p>

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
      <p>Specifies the remote device FQDN or IP address to establish the gRPC connection to.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;inventory_hostname&#34;</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_host</p>

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
      <div class="ansibleOptionAnchor" id="parameter-network_os"></div>
      <p style="display: inline;"><strong>network_os</strong></p>
      <a class="ansibleOptionLink" href="#parameter-network_os" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Configures the device platform network operating system. This value is used to load a device specific grpc plugin to communicate with the remote device.</p>
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
      <p>Configures the user password used to authenticate to the remote device when first establishing the gRPC connection.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_password</p>

      </li>
      <li>
        <p>Variable: ansible_ssh_pass</p>

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
      <p>Specifies the port on the remote device that listens for connections when establishing the gRPC connection. If None only the <code class='docutils literal notranslate'>host</code> part will be used.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[defaults]
  remote_port = VALUE</pre>

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
      <p>The PEM encoded private key file used to authenticate to the remote device when first establishing the grpc connection.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[grpc_connection]
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
      <p>The username used to authenticate to the remote device when the gRPC connection is first established.  If the remote_user is not specified, the connection will use the username of the logged in user.</p>
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
      <div class="ansibleOptionAnchor" id="parameter-root_certificates_file"></div>
      <p style="display: inline;"><strong>root_certificates_file</strong></p>
      <a class="ansibleOptionLink" href="#parameter-root_certificates_file" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>The PEM encoded root certificate file used to create a SSL-enabled channel, if the value is None it reads the root certificates from a default location chosen by gRPC at runtime.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[grpc_connection]
  root_certificates_file = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_ROOT_CERTIFICATES_FILE</code></p>

      </li>
      <li>
        <p>Variable: ansible_root_certificates_file</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-ssl_target_name_override"></div>
      <p style="display: inline;"><strong>ssl_target_name_override</strong></p>
      <a class="ansibleOptionLink" href="#parameter-ssl_target_name_override" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>The option overrides SSL target name used for SSL host name checking. The name used for SSL host name checking will be the target parameter (assuming that the secure channel is an SSL channel). If this parameter is specified and the underlying is not an SSL channel, it will just be ignored.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[grpc_connection]
  ssl_target_name_override = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_GPRC_SSL_TARGET_NAME_OVERRIDE</code></p>

      </li>
      <li>
        <p>Variable: ansible_grpc_ssl_target_name_override</p>

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
