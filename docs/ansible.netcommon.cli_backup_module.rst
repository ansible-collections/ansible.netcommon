
.. Created with antsibull-docs 2.9.0

ansible.netcommon.cli_backup module -- Back up device configuration from network devices over network\_cli
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.cli_backup``.

New in ansible.netcommon 4.2.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This module provides platform agnostic way of backing up text based configuration from network devices over network\_cli connection plugin.

This module has a corresponding action plugin.







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
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-dir_path"></div>
      <p style="display: inline;"><strong>dir_path</strong></p>
      <a class="ansibleOptionLink" href="#parameter-dir_path" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">path</span>
      </p>
    </td>
    <td valign="top">
      <p>This option provides the path ending with directory name in which the backup configuration file will be stored. If the directory does not exist it will be first created and the filename is either the value of <code class='docutils literal notranslate'>filename</code> or default filename as described in <code class='docutils literal notranslate'>filename</code> options description. If the path value is not given in that case a <em>backup</em> directory will be created in the current working directory and backup configuration will be copied in <code class='docutils literal notranslate'>filename</code> within <em>backup</em> directory.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-filename"></div>
      <p style="display: inline;"><strong>filename</strong></p>
      <a class="ansibleOptionLink" href="#parameter-filename" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>The filename to be used to store the backup configuration. If the filename is not given it will be generated based on the hostname, current time and date in format defined by &lt;hostname&gt;_config.&lt;current-date&gt;@&lt;current-time&gt;</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- This module is supported on \ :literal:`ansible\_network\_os`\  network platforms. See the :ref:\`Network Platform Options \<platform\_options\>\` for details.


Examples
--------

.. code-block:: yaml


    - name: configurable backup path
      ansible.netcommon.cli_backup:
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
      <p style="margin-top: 8px;"><b>Returned:</b> always</p>
      <p style="margin-top: 8px; color: blue; word-wrap: break-word; word-break: break-all;"><b style="color: black;">Sample:</b> <code>&#34;/playbooks/ansible/backup/hostname_config.2016-07-16@22:28:34&#34;</code></p>
    </td>
  </tr>
  </tbody>
  </table>




Authors
~~~~~~~

- Kate Case (@Qalthos)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
