
.. Created with antsibull-docs 2.9.0

ansible.netcommon.net_get module -- Copy a file from a network device to Ansible Controller
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This module is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.
You need further requirements to be able to use this module,
see `Requirements <ansible_collections.ansible.netcommon.net_get_module_requirements_>`_ for details.

To use it in a playbook, specify: ``ansible.netcommon.net_get``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This module provides functionality to copy file from network device to ansible controller.

This module has a corresponding action plugin.


.. _ansible_collections.ansible.netcommon.net_get_module_requirements:

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
      <p>Specifies the destination file. The path to the destination file can either be the full path on the Ansible control host or a relative path from the playbook or role root directory.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">[&#34;Same filename as specified in I(src). The path will be playbook root or role root directory if playbook is part of a role.&#34;]</code></p>
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
      <p>Specifies the source file. The path to the source file can either be the full path on the network device or a relative path as per path supported by destination network device.</p>
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


    - name: copy file from the network device to Ansible controller
      ansible.netcommon.net_get:
        src: running_cfg_ios1.txt

    - name: copy file from ios to common location at /tmp
      ansible.netcommon.net_get:
        src: running_cfg_sw1.txt
        dest: /tmp/ios1.txt







Authors
~~~~~~~

- Deepak Agrawal (@dagrawal)



Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
