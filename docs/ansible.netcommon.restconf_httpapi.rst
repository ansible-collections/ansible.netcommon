
.. Created with antsibull-docs 2.9.0

ansible.netcommon.restconf httpapi -- HttpApi Plugin for devices supporting Restconf API
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This httpapi plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.restconf``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This HttpApi plugin provides methods to connect to Restconf API endpoints.








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
      <div class="ansibleOptionAnchor" id="parameter-root_path"></div>
      <p style="display: inline;"><strong>root_path</strong></p>
      <a class="ansibleOptionLink" href="#parameter-root_path" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Specifies the location of the Restconf root.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;/restconf&#34;</code></p>
      <p style="margin-top: 8px;"><b>Configuration:</b></p>
      <ul>
      <li>
        <p>Variable: ansible_httpapi_restconf_root</p>

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
