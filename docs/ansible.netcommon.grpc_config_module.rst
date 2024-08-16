
.. Created with antsibull-docs 2.9.0

ansible.netcommon.grpc_config module -- Fetch configuration/state data from gRPC enabled target hosts.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.
You need further requirements to be able to use this module,
see `Requirements <ansible_collections.ansible.netcommon.grpc_config_module_requirements_>`_ for details.

To use it in a playbook, specify: ``ansible.netcommon.grpc_config``.

New in ansible.netcommon 3.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- gRPC is a high performance, open-source universal RPC framework.
- This module allows the user to append configs to an existing configuration in a gRPC enabled devices.

This module has a corresponding action plugin.


.. _ansible_collections.ansible.netcommon.grpc_config_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- grpcio
- protobuf






Parameters
----------

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th colspan="2"><p>Parameter</p></th>
    <th><p>Comments</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-backup"></div>
      <p style="display: inline;"><strong>backup</strong></p>
      <a class="ansibleOptionLink" href="#parameter-backup" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>This argument will cause the module to create a full backup of the current <code class='docutils literal notranslate'>running-config</code> from the remote device before any changes are made. If the <code class='docutils literal notranslate'>backup_options</code> value is not given, the backup file is written to the <code class='docutils literal notranslate'>backup</code> folder in the playbook root directory or role root directory, if playbook is part of an ansible role. If the directory does not exist, it is created.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-backup_options"></div>
      <p style="display: inline;"><strong>backup_options</strong></p>
      <a class="ansibleOptionLink" href="#parameter-backup_options" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>This is a dict object containing configurable options related to backup file path. The value of this option is read only when <code class='docutils literal notranslate'>backup</code> is set to <em>yes</em>, if <code class='docutils literal notranslate'>backup</code> is set to <em>no</em> this option will be silently ignored.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-backup_options/dir_path"></div>
      <p style="display: inline;"><strong>dir_path</strong></p>
      <a class="ansibleOptionLink" href="#parameter-backup_options/dir_path" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">path</span>
      </p>
    </td>
    <td valign="top">
      <p>This option provides the path ending with directory name in which the backup configuration file will be stored. If the directory does not exist it will be first created and the filename is either the value of <code class='docutils literal notranslate'>filename</code> or default filename as described in <code class='docutils literal notranslate'>filename</code> options description. If the path value is not given in that case a <em>backup</em> directory will be created in the current working directory and backup configuration will be copied in <code class='docutils literal notranslate'>filename</code> within <em>backup</em> directory.</p>
    </td>
  </tr>
  <tr>
    <td></td>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-backup_options/filename"></div>
      <p style="display: inline;"><strong>filename</strong></p>
      <a class="ansibleOptionLink" href="#parameter-backup_options/filename" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The filename to be used to store the backup configuration. If the filename is not given it will be generated based on the hostname, current time and date in format defined by &lt;hostname&gt;_config.&lt;current-date&gt;@&lt;current-time&gt;</p>
    </td>
  </tr>

  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-config"></div>
      <p style="display: inline;"><strong>config</strong></p>
      <a class="ansibleOptionLink" href="#parameter-config" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>This option specifies the string which acts as a filter to restrict the portions of the data to be retrieved from the target host device. If this option is not specified the entire configuration or state data is returned in response provided it is supported by target host.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-state"></div>
      <p style="display: inline;"><strong>state</strong></p>
      <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>action to be performed</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- This module requires the gRPC system service be enabled on the target host being managed.
- This module supports the use of connection=connection=ansible.netcommon.grpc
- This module requires the value of 'ansible\_network\_os' or 'grpc\_type' configuration option (refer ansible.netcommon.grpc connection plugin documentation) be defined as an inventory variable.
- Tested against iosxrv 9k version 6.1.2.


Examples
--------

.. code-block:: yaml


    - name: Merge static route config
      ansible.netcommon.grpc_config:
        config:
          Cisco-IOS-XR-ip-static-cfg:router-static:
            default-vrf:
              address-family:
                vrfipv4:
                  vrf-unicast:
                    vrf-prefixes:
                      vrf-prefix:
                        - prefix: "1.2.3.6"
                          prefix-length: 32
                          vrf-route:
                            vrf-next-hop-table:
                              vrf-next-hop-next-hop-address:
                                - next-hop-address: "10.0.2.2"
        state: merged

    - name: Merge bgp config
      ansible.netcommon.grpc_config:
        config: "{{ lookup('file', 'bgp.json')  }}"
        state: merged

    - name: Find diff
      diff: true
      ansible.netcommon.grpc_config:
        config: "{{ lookup('file', 'bgp_start.yml')  }}"
        state: merged

    - name: Backup running config
      ansible.netcommon.grpc_config:
        backup: true





Return Values
-------------
The following are the fields unique to this module:

.. raw:: html

  <table style="width: 100%;">
  <thead>
    <tr>
    <th><p>Key</p></th>
    <th><p>Description</p></th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-backup_path"></div>
      <p style="display: inline;"><strong>backup_path</strong></p>
      <a class="ansibleOptionLink" href="#return-backup_path" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The full path to the backup file</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when backup is yes</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;/playbooks/ansible/backup/config.2022-07-16@22:28:34&#34;</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-diff"></div>
      <p style="display: inline;"><strong>diff</strong></p>
      <a class="ansibleOptionLink" href="#return-diff" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">dictionary</span>
      </p>
    </td>
    <td valign="top">
      <p>If --diff option in enabled while running, the before and after configuration change are returned as part of before and after key.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> when diff is enabled</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-stdout"></div>
      <p style="display: inline;"><strong>stdout</strong></p>
      <a class="ansibleOptionLink" href="#return-stdout" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The raw string containing response object received from the gRPC server.</p>
      <p style="margin-top: 8px;"><b>Returned:</b> error mesage, when failure happens. empty , when the operation is successful</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;...&#34;</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-stdout_lines"></div>
      <p style="display: inline;"><strong>stdout_lines</strong></p>
      <a class="ansibleOptionLink" href="#return-stdout_lines" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The value of stdout split into a list</p>
      <p style="margin-top: 8px;"><b>Returned:</b> always apart from low-level errors (such as action plugin)</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;...&#34;, &#34;...&#34;]</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Gomathi Selvi S (@GomathiselviS)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
