
.. Created with antsibull-docs 2.9.0

ansible.netcommon.persistent connection -- Use a persistent unix socket for connection
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This connection plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.persistent``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This is a helper plugin to allow making other connections persistent.








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
