
.. Created with antsibull-docs 2.9.0

ansible.netcommon.net_put module -- Copy a file from Ansible Controller to a network device
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.
You need further requirements to be able to use this module,
see `Requirements <ansible_collections.ansible.netcommon.net_put_module_requirements_>`_ for details.

To use it in a playbook, specify: ``ansible.netcommon.net_put``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This module provides functionality to copy file from Ansible controller to network devices.

This module has a corresponding action plugin.


.. _ansible_collections.ansible.netcommon.net_put_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- scp if using protocol=scp with paramiko






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
      <div class="ansibleOptionAnchor" id="parameter-dest"></div>
      <p style="display: inline;"><strong>dest</strong></p>
      <a class="ansibleOptionLink" href="#parameter-dest" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Specifies the destination file. The path to destination file can either be the full path or relative path as supported by network_os.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">[&#34;Filename from src and at default directory of user shell on network_os.&#34;]</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-mode"></div>
      <p style="display: inline;"><strong>mode</strong></p>
      <a class="ansibleOptionLink" href="#parameter-mode" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Set the file transfer mode. If mode is set to <em>text</em> then <em>src</em> file will go through Jinja2 template engine to replace any vars if present in the src file. If mode is set to <em>binary</em> then file will be copied as it is to destination device.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;binary&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;text&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-protocol"></div>
      <p style="display: inline;"><strong>protocol</strong></p>
      <a class="ansibleOptionLink" href="#parameter-protocol" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>
    </td>
    <td valign="top">
      <p>Protocol used to transfer file.</p>
      <p style="margin-top: 8px;"><b">Choices:</b></p>
      <ul>
        <li><p><code style="color: blue;"><b>&#34;scp&#34;</b></code> <span style="color: blue;">← (default)</span></p></li>
        <li><p><code>&#34;sftp&#34;</code></p></li>
      </ul>

    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-src"></div>
      <p style="display: inline;"><strong>src</strong></p>
      <a class="ansibleOptionLink" href="#parameter-src" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>
    </td>
    <td valign="top">
      <p>Specifies the source file. The path to the source file can either be the full path on the Ansible control host or a relative path from the playbook or role root directory.</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- Some devices need specific configurations to be enabled before scp can work These configuration should be pre-configured before using this module e.g ios - \ :literal:`ip scp server enable`\ .
- User privilege to do scp on network device should be pre-configured e.g. ios - need user privilege 15 by default for allowing scp.
- Default destination of source file.
- This module is supported on \ :literal:`ansible\_network\_os`\  network platforms. See the :ref:\`Network Platform Options \<platform\_options\>\` for details.


Examples
--------

.. code-block:: yaml


    - name: copy file from ansible controller to a network device
      ansible.netcommon.net_put:
        src: running_cfg_ios1.txt

    - name: copy file at root dir of flash in slot 3 of sw1(ios)
      ansible.netcommon.net_put:
        src: running_cfg_sw1.txt
        protocol: sftp
        dest: flash3:/running_cfg_sw1.txt







Authors
~~~~~~~

- Deepak Agrawal (@dagrawal)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
