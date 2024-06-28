
.. Created with antsibull-docs 2.9.0

ansible.netcommon.cli_config module -- Push text based configuration to network devices over network\_cli
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.cli_config``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This module provides platform agnostic way of pushing text based configuration to network devices over network\_cli connection plugin.

This module has a corresponding action plugin.







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
      <p>This argument will cause the module to create a full backup of the current running config from the remote device before any changes are made. If the <code class='docutils literal notranslate'>backup_options</code> value is not given, the backup file is written to the <code class='docutils literal notranslate'>backup</code> folder in the playbook root directory or role root directory, if playbook is part of an ansible role. If the directory does not exist, it is created.</p>
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
      <div class="ansibleOptionAnchor" id="parameter-commit"></div>
      <p style="display: inline;"><strong>commit</strong></p>
      <a class="ansibleOptionLink" href="#parameter-commit" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>The <code class='docutils literal notranslate'>commit</code> argument instructs the module to push the configuration to the device. This is mapped to module check mode.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>false</code></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-commit_comment"></div>
      <p style="display: inline;"><strong>commit_comment</strong></p>
      <a class="ansibleOptionLink" href="#parameter-commit_comment" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The <code class='docutils literal notranslate'>commit_comment</code> argument specifies a text string to be used when committing the configuration. If the <code class='docutils literal notranslate'>commit</code> argument is set to False, this argument is silently ignored. This argument is only valid for the platforms that support commit operation with comment.</p>
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
      <p>The config to be pushed to the network device. This argument is mutually exclusive with <code class='docutils literal notranslate'>rollback</code> and either one of the option should be given as input. To ensure idempotency and correct diff the configuration lines should be similar to how they appear if present in the running configuration on device including the indentation.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-defaults"></div>
      <p style="display: inline;"><strong>defaults</strong></p>
      <a class="ansibleOptionLink" href="#parameter-defaults" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">boolean</span>
      </p>
    </td>
    <td valign="top">
      <p>The <em>defaults</em> argument will influence how the running-config is collected from the device.  When the value is set to true, the command used to collect the running-config is append with the all keyword.  When the value is set to false, the command is issued without the all keyword.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>false</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>true</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-diff_ignore_lines"></div>
      <p style="display: inline;"><strong>diff_ignore_lines</strong></p>
      <a class="ansibleOptionLink" href="#parameter-diff_ignore_lines" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>Use this argument to specify one or more lines that should be ignored during the diff. This is used for lines in the configuration that are automatically updated by the system. This argument takes a list of regular expressions or exact line matches. Note that this parameter will be ignored if the platform has onbox diff support.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-diff_match"></div>
      <p style="display: inline;"><strong>diff_match</strong></p>
      <a class="ansibleOptionLink" href="#parameter-diff_match" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Instructs the module on the way to perform the matching of the set of commands against the current device config. If <code class='docutils literal notranslate'>diff_match</code> is set to <em>line</em>, commands are matched line by line. If <code class='docutils literal notranslate'>diff_match</code> is set to <em>strict</em>, command lines are matched with respect to position. If <code class='docutils literal notranslate'>diff_match</code> is set to <em>exact</em>, command lines must be an equal match. Finally, if <code class='docutils literal notranslate'>diff_match</code> is set to <em>none</em>, the module will not attempt to compare the source configuration with the running configuration on the remote device. Note that this parameter will be ignored if the platform has onbox diff support.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;line&#34;</code></p></li>
        <li><p><code>&#34;strict&#34;</code></p></li>
        <li><p><code>&#34;exact&#34;</code></p></li>
        <li><p><code>&#34;none&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-diff_replace"></div>
      <p style="display: inline;"><strong>diff_replace</strong></p>
      <a class="ansibleOptionLink" href="#parameter-diff_replace" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Instructs the module on the way to perform the configuration on the device. If the <code class='docutils literal notranslate'>diff_replace</code> argument is set to <em>line</em> then the modified lines are pushed to the device in configuration mode. If the argument is set to <em>block</em> then the entire command block is pushed to the device in configuration mode if any line is not correct. Note that this parameter will be ignored if the platform has onbox diff support.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code>&#34;line&#34;</code></p></li>
        <li><p><code>&#34;block&#34;</code></p></li>
        <li><p><code>&#34;config&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-multiline_delimiter"></div>
      <p style="display: inline;"><strong>multiline_delimiter</strong></p>
      <a class="ansibleOptionLink" href="#parameter-multiline_delimiter" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>This argument is used when pushing a multiline configuration element to the device. It specifies the character to use as the delimiting character. This only applies to the configuration action.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-replace"></div>
      <p style="display: inline;"><strong>replace</strong></p>
      <a class="ansibleOptionLink" href="#parameter-replace" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>If the <code class='docutils literal notranslate'>replace</code> argument is set to <code class='docutils literal notranslate'>yes</code>, it will replace the entire running-config of the device with the <code class='docutils literal notranslate'>config</code> argument value. For devices that support replacing running configuration from file on device like NXOS/JUNOS, the <code class='docutils literal notranslate'>replace</code> argument takes path to the file on the device that will be used for replacing the entire running-config. The value of <code class='docutils literal notranslate'>config</code> option should be <em>None</em> for such devices. Nexus 9K devices only support replace. Use <em>net_put</em> or <em>nxos_file_copy</em> in case of NXOS module to copy the flat file to remote device and then use set the fullpath to this argument.</p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <div class="ansibleOptionAnchor" id="parameter-rollback"></div>
      <p style="display: inline;"><strong>rollback</strong></p>
      <a class="ansibleOptionLink" href="#parameter-rollback" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>
    </td>
    <td valign="top">
      <p>The <code class='docutils literal notranslate'>rollback</code> argument instructs the module to rollback the current configuration to the identifier specified in the argument.  If the specified rollback identifier does not exist on the remote device, the module will fail. To rollback to the most recent commit, set the <code class='docutils literal notranslate'>rollback</code> argument to 0. This option is mutually exclusive with <code class='docutils literal notranslate'>config</code>.</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- The commands will be returned only for platforms that do not support onbox diff. The \ :literal:`--diff`\  option with the playbook will return the difference in configuration for devices that has support for onbox diff
- To ensure idempotency and correct diff the configuration lines in the relevant module options should be similar to how they appear if present in the running configuration on device including the indentation.
- This module is supported on \ :literal:`ansible\_network\_os`\  network platforms. See the :ref:\`Network Platform Options \<platform\_options\>\` for details.


Examples
--------

.. code-block:: yaml


    - name: configure device with config
      ansible.netcommon.cli_config:
        config: "{{ lookup('template', 'basic/config.j2') }}"

    - name: multiline config
      ansible.netcommon.cli_config:
        config: |
          hostname foo
          feature nxapi

    - name: configure device with config with defaults enabled
      ansible.netcommon.cli_config:
        config: "{{ lookup('template', 'basic/config.j2') }}"
        defaults: "yes"

    - name: Use diff_match
      ansible.netcommon.cli_config:
        config: "{{ lookup('file', 'interface_config') }}"
        diff_match: none

    - name: nxos replace config
      ansible.netcommon.cli_config:
        replace: bootflash:nxoscfg

    - name: junos replace config
      ansible.netcommon.cli_config:
        replace: /var/home/ansible/junos01.cfg

    - name: commit with comment
      ansible.netcommon.cli_config:
        config: set system host-name foo
        commit_comment: this is a test

    - name: configurable backup path
      ansible.netcommon.cli_config:
        config: "{{ lookup('template', 'basic/config.j2') }}"
        backup: "yes"
        backup_options:
          filename: backup.cfg
          dir_path: /home/user





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
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;/playbooks/ansible/backup/hostname_config.2016-07-16@22:28:34&#34;</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-commands"></div>
      <p style="display: inline;"><strong>commands</strong></p>
      <a class="ansibleOptionLink" href="#return-commands" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
      </p>
    </td>
    <td valign="top">
      <p>The set of commands that will be pushed to the remote device</p>
      <p style="margin-top: 8px;"><b>Returned:</b> When <em>supports_generated_diff=True</em> and <em>supports_onbox_diff=False</em> in the platform&#x27;s cliconf plugin</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>[&#34;interface Loopback999&#34;, &#34;no shutdown&#34;]</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="return-diff"></div>
      <p style="display: inline;"><strong>diff</strong></p>
      <a class="ansibleOptionLink" href="#return-diff" title="Permalink to this return value"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The diff generated on the device when the commands were applied</p>
      <p style="margin-top: 8px;"><b>Returned:</b> When <em>supports_onbox_diff=True</em> in the platform&#x27;s cliconf plugin</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;--- system:/running-config\n+++ session:/ansible_1599745461-session-config\n@@ -4,7 +4,7 @@\n !\n transceiver qsfp default-mode 4x10G\n !\n-hostname veos\n+hostname veos3\n !\n spanning-tree mode mstp&#34;</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Trishna Guha (@trishnaguha)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
