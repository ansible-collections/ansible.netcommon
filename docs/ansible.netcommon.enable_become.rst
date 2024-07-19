
.. Created with antsibull-docs 2.9.0

ansible.netcommon.enable become -- Switch to elevated permissions on a network device
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This become plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.enable``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This become plugins allows elevated permissions on a remote network device.








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
      <div class="ansibleOptionAnchor" id="parameter-become_pass"></div>
      <p style="display: inline;"><strong>become_pass</strong></p>
      <a class="ansibleOptionLink" href="#parameter-become_pass" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>password</p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>INI entry</p>
        <pre>[enable_become_plugin]
  password = VALUE</pre>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_BECOME_PASS</code></p>

      </li>
      <li>
        <p>Environment variable: <code>ANSIBLE_ENABLE_PASS</code></p>

      </li>
      <li>
        <p>Variable: ansible_become_password</p>

      </li>
      <li>
        <p>Variable: ansible_become_pass</p>

      </li>
      <li>
        <p>Variable: ansible_enable_pass</p>

      </li>
      </ul>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- enable is really implemented in the network connection handler and as such can only be used with network connections.
- This plugin ignores the 'become\_exe' and 'become\_user' settings as it uses an API and not an executable.







Authors
~~~~~~~

- Ansible Networking Team (@ansible-network)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
