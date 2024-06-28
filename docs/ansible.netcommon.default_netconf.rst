
.. Created with antsibull-docs 2.9.0

ansible.netcommon.default netconf -- Use default netconf plugin to run standard netconf commands as per RFC
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This netconf plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.default``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- This default plugin provides low level abstraction apis for sending and receiving netconf commands as per Netconf RFC specification.








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
      <div class="ansibleOptionAnchor" id="parameter-ncclient_device_handler"></div>
      <p style="display: inline;"><strong>ncclient_device_handler</strong></p>
      <a class="ansibleOptionLink" href="#parameter-ncclient_device_handler" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>Specifies the ncclient device handler name for network os that support default netconf implementation as per Netconf RFC specification. To identify the ncclient device handler name refer ncclient library documentation.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">&#34;default&#34;</code></p>
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
