
.. Created with antsibull-docs 2.9.0

ansible.netcommon.libssh connection -- Run tasks using libssh for ssh connection
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This connection plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.libssh``.

New in ansible.netcommon 1.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Use the ansible-pylibssh python bindings to connect to targets
- The python bindings use libssh C library (https://www.libssh.org/) to connect to targets
- This plugin borrows a lot of settings from the ssh plugin as they both cover the same protocol.








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
      <div class="ansibleOptionAnchor" id="parameter-config_file"></div>
      <p style="display: inline;"><strong>config_file</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config_file" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">path</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ansible.netcommon 5.1.0</i></p>

    </td>
    <td valign="top">
      <p>Alternate SSH config file location</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[libssh_connection]
  config_file = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_LIBSSH_CONFIG_FILE</code></p>

      </li>
      <li>
        <p>Variable: ansible_libssh_config_file</p>

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
      <p>TODO: write it</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[libssh_connection]
  host_key_auto_add = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_LIBSSH_HOST_KEY_AUTO_ADD</code></p>

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

        <pre>[libssh_connection]
  host_key_checking = true</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_HOST_KEY_CHECKING</code></p>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_SSH_HOST_KEY_CHECKING</code></p>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_LIBSSH_HOST_KEY_CHECKING</code></p>

      </li>
      <li>
        <p>Variable: ansible_host_key_checking</p>

      </li>
      <li>
        <p>Variable: ansible_ssh_host_key_checking</p>

      </li>
      <li>
        <p>Variable: ansible_libssh_host_key_checking</p>

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
      <p>TODO: write it</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code style="color: blue;"><b>true</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[libssh_connection]
  look_for_keys = true</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_LIBSSH_LOOK_FOR_KEYS</code></p>

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
      <p>Secret used to either login the ssh server or as a passphrase for ssh keys that require it</p>
      <p>Can be set from the CLI via the <code class='docutils literal notranslate'>--ask-pass</code> option.</p>
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
        <p>Variable: ansible_libssh_pass</p>

      </li>
      <li>
        <p>Variable: ansible_libssh_password</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-password_prompt"></div>
      <p style="display: inline;"><strong>password_prompt</strong></p>
      <a class="ansibleOptionLink" href="#parameter-password_prompt" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ansible.netcommon 3.1.0</i></p>

    </td>
    <td valign="top">
      <p>Text to match when using keyboard-interactive authentication to determine if the prompt is for the password.</p>
      <p>Requires ansible-pylibssh version &gt;= 1.0.0</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_libssh_password_prompt</p>

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
      <p>Also this plugin will scan &#x27;ssh_args&#x27;, &#x27;ssh_extra_args&#x27; and &#x27;ssh_common_args&#x27; from the &#x27;ssh&#x27; plugin settings for proxy information if set.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;&#34;</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[libssh_connection]
  proxy_command = &#34;&#34;</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_LIBSSH_PROXY_COMMAND</code></p>

      </li>
      <li>
        <p>Variable: ansible_paramiko_proxy_command</p>

      </li>
      <li>
        <p>Variable: ansible_libssh_proxy_command</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-pty"></div>
      <p style="display: inline;"><strong>pty</strong></p>
      <a class="ansibleOptionLink" href="#parameter-pty" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>TODO: write it</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code style="color: blue;"><b>true</b></code> <span style="color: blue;">← (default)</span></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[libssh_connection]
  pty = true</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_LIBSSH_PTY</code></p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-remote_addr"></div>
      <p style="display: inline;"><strong>remote_addr</strong></p>
      <a class="ansibleOptionLink" href="#parameter-remote_addr" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Address of the remote target</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;inventory_hostname&#34;</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: inventory_hostname</p>

      </li>
      <li>
        <p>Variable: ansible_host</p>

      </li>
      <li>
        <p>Variable: ansible_ssh_host</p>

      </li>
      <li>
        <p>Variable: ansible_libssh_host</p>

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
      <p>User to login/authenticate as</p>
      <p>Can be set from the CLI via the <code class='docutils literal notranslate'>--user</code> or <code class='docutils literal notranslate'>-u</code> options.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entries</p>
        <pre>[defaults]
  remote_user = VALUE</pre>

        <pre>[libssh_connection]
  remote_user = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_REMOTE_USER</code></p>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_LIBSSH_REMOTE_USER</code></p>

      </li>
      <li>
        <p>Variable: ansible_user</p>

      </li>
      <li>
        <p>Variable: ansible_ssh_user</p>

      </li>
      <li>
        <p>Variable: ansible_libssh_user</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-ssh_args"></div>
      <p style="display: inline;"><strong>ssh_args</strong></p>
      <a class="ansibleOptionLink" href="#parameter-ssh_args" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ansible.netcommon 3.2.0</i></p>

    </td>
    <td valign="top">
      <p>Arguments to pass to all ssh CLI tools.</p>
      <p>ProxyCommand is the only supported argument.</p>
      <p>This option is deprecated in favor of <em>proxy_command</em> and will be removed in a release after 2026-01-01.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[ssh_connection]
  ssh_args = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_SSH_ARGS</code></p>

      </li>
      <li>
        <p>Variable: ansible_ssh_args</p>

      </li>
      <li>
        <p>CLI argument: --ssh-args</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-ssh_common_args"></div>
      <p style="display: inline;"><strong>ssh_common_args</strong></p>
      <a class="ansibleOptionLink" href="#parameter-ssh_common_args" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ansible.netcommon 3.2.0</i></p>

    </td>
    <td valign="top">
      <p>Common extra arguments for all ssh CLI tools.</p>
      <p>ProxyCommand is the only supported argument.</p>
      <p>This option is deprecated in favor of <em>proxy_command</em> and will be removed in a release after 2026-01-01.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[ssh_connection]
  ssh_common_args = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_SSH_COMMON_ARGS</code></p>

      </li>
      <li>
        <p>Variable: ansible_ssh_common_args</p>

      </li>
      <li>
        <p>CLI argument: --ssh-common-args</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-ssh_extra_args"></div>
      <p style="display: inline;"><strong>ssh_extra_args</strong></p>
      <a class="ansibleOptionLink" href="#parameter-ssh_extra_args" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
      <p><i style="font-size: small; color: darkgreen;">added in ansible.netcommon 3.2.0</i></p>

    </td>
    <td valign="top">
      <p>Extra arguments exclusive to the &#x27;ssh&#x27; CLI tool.</p>
      <p>ProxyCommand is the only supported argument.</p>
      <p>This option is deprecated in favor of <em>proxy_command</em> and will be removed in a release after 2026-01-01.</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[ssh_connection]
  ssh_extra_args = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_SSH_EXTRA_ARGS</code></p>

      </li>
      <li>
        <p>Variable: ansible_ssh_extra_args</p>

      </li>
      <li>
        <p>CLI argument: --ssh-extra-args</p>

      </li>
      </ul>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-use_persistent_connections"></div>
      <p style="display: inline;"><strong>use_persistent_connections</strong></p>
      <a class="ansibleOptionLink" href="#parameter-use_persistent_connections" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>

    </td>
    <td valign="top">
      <p>Toggles the use of persistence for connections</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[defaults]
  use_persistent_connections = false</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_USE_PERSISTENT_CONNECTIONS</code></p>

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
