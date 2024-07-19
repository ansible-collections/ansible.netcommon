
.. Created with antsibull-docs 2.9.0

ansible.netcommon.httpapi connection -- Use httpapi to run command on network appliances
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This connection plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.httpapi``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This connection plugin provides a connection to remote devices over a HTTP(S)-based api.








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
      <div class="ansibleOptionAnchor" id="parameter-ca_path"></div>
      <p style="display: inline;"><strong>ca_path</strong></p>
      <a class="ansibleOptionLink" href="#parameter-ca_path" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">path</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ansible.netcommon 5.2.0</i></p>

    </td>
    <td valign="top">
      <p>Path to CA cert bundle to use.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_httpapi_ca_path</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-ciphers"></div>
      <p style="display: inline;"><strong>ciphers</strong></p>
      <a class="ansibleOptionLink" href="#parameter-ciphers" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ansible.netcommon 5.0.0</i></p>

    </td>
    <td valign="top">
      <p>SSL/TLS Ciphers to use for requests</p>
      <p>When a list is provided, all ciphers are joined in order with <code class='docutils literal notranslate'>:</code></p>
      <p>See the <a href='https://www.openssl.org/docs/manmaster/man1/openssl-ciphers.html#CIPHER-LIST-FORMAT'>OpenSSL Cipher List Format</a> for more details.</p>
      <p>The available ciphers is dependent on the Python and OpenSSL/LibreSSL versions.</p>
      <p>This option will have no effect on ansible-core&lt;2.14 but a warning will be emitted.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_httpapi_ciphers</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-client_cert"></div>
      <p style="display: inline;"><strong>client_cert</strong></p>
      <a class="ansibleOptionLink" href="#parameter-client_cert" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ansible.netcommon 5.2.0</i></p>

    </td>
    <td valign="top">
      <p>PEM formatted certificate chain file to be used for SSL client authentication. This file can also include the key as well, and if the key is included, <em>client_key</em> is not required</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_httpapi_client_cert</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-client_key"></div>
      <p style="display: inline;"><strong>client_key</strong></p>
      <a class="ansibleOptionLink" href="#parameter-client_key" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ansible.netcommon 5.2.0</i></p>

    </td>
    <td valign="top">
      <p>PEM formatted file that contains the private key to be used for SSL client authentication. If <em>client_cert</em> contains both the certificate and key, this option is not required.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_httpapi_client_key</p>

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
      <p>Specifies the remote device FQDN or IP address to establish the HTTP(S) connection to.</p>
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
      <div class="ansibleOptionAnchor" id="parameter-http_agent"></div>
      <p style="display: inline;"><strong>http_agent</strong></p>
      <a class="ansibleOptionLink" href="#parameter-http_agent" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ansible.netcommon 5.2.0</i></p>

    </td>
    <td valign="top">
      <p>User-Agent to use in the request.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_httpapi_http_agent</p>

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
      <p>Configures the device platform network operating system.  This value is used to load the correct httpapi plugin to communicate with the remote device</p>
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
      <p>Configures the user password used to authenticate to the remote device when needed for the device API.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_password</p>

      </li>
      <li>
        <p>Variable: ansible_httpapi_pass</p>

      </li>
      <li>
        <p>Variable: ansible_httpapi_password</p>

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
      <div class="ansibleOptionAnchor" id="parameter-platform_type"></div>
      <p style="display: inline;"><strong>platform_type</strong></p>
      <a class="ansibleOptionLink" href="#parameter-platform_type" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Set type of platform.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Environment variable: <code>ANSIBLE_PLATFORM_TYPE</code></p>

      </li>
      <li>
        <p>Variable: ansible_platform_type</p>

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
      <p>Specifies the port on the remote device that listens for connections when establishing the HTTP(S) connection.</p>
      <p>When unspecified, will pick 80 or 443 based on the value of use_ssl.</p>
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
        <p>Variable: ansible_httpapi_port</p>

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
      <p>The username used to authenticate to the remote device when the API connection is first established.  If the remote_user is not specified, the connection will use the username of the logged in user.</p>
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
      <div class="ansibleOptionAnchor" id="parameter-session_key"></div>
      <p style="display: inline;"><strong>session_key</strong></p>
      <a class="ansibleOptionLink" href="#parameter-session_key" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>

    </td>
    <td valign="top">
      <p>Configures the session key to be used to authenticate to the remote device when needed for the device API.</p>
      <p>This should contain a dictionary representing the key name and value for the token.</p>
      <p>When specified, <em>password</em> is ignored.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_httpapi_session_key</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-use_proxy"></div>
      <p style="display: inline;"><strong>use_proxy</strong></p>
      <a class="ansibleOptionLink" href="#parameter-use_proxy" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>Whether to use https_proxy for requests.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code style="color: blue;"><b>true</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_httpapi_use_proxy</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-use_ssl"></div>
      <p style="display: inline;"><strong>use_ssl</strong></p>
      <a class="ansibleOptionLink" href="#parameter-use_ssl" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>Whether to connect using SSL (HTTPS) or not (HTTP).</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_httpapi_use_ssl</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-validate_certs"></div>
      <p style="display: inline;"><strong>validate_certs</strong></p>
      <a class="ansibleOptionLink" href="#parameter-validate_certs" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>Whether to validate SSL certificates</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code style="color: blue;"><b>true</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_httpapi_validate_certs</p>

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
