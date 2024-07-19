
.. Created with antsibull-docs 2.9.0

ansible.netcommon.vlan_expander filter -- The vlan\_expander filter plugin.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This filter plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.vlan_expander``.

New in ansible.netcommon 2.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- Expand shorthand list of VLANs to list all VLANs. Inverse of vlan\_parser
- Using the parameters below - \ :literal:`vlans\_data | ansible.netcommon.vlan\_expander`\








Keyword parameters
------------------

This describes keyword parameters of the filter. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
example: ``input | ansible.netcommon.vlan_expander(key1=value1, key2=value2, ...)``

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
      <div class="ansibleOptionAnchor" id="parameter-data"></div>
      <p style="display: inline;"><strong>data</strong></p>
      <a class="ansibleOptionLink" href="#parameter-data" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
        / <span style="color: red;">required</span>
      </p>

    </td>
    <td valign="top">
      <p>This option represents a string containing the range of vlans.</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- The filter plugin extends vlans when data provided in range or comma separated.


Examples
--------

.. code-block:: yaml


    # Using vlan_expander

    - name: Setting host facts for vlan_expander filter plugin
      ansible.builtin.set_fact:
        vlan_ranges: "1,10-12,15,20-22"

    - name: Invoke vlan_expander filter plugin
      ansible.builtin.set_fact:
        extended_vlans: "{{ vlan_ranges | ansible.netcommon.vlan_expander }}"


    # Task Output
    # -----------
    #
    # TASK [Setting host facts for vlan_expander filter plugin]
    # ok: [host] => changed=false
    #   ansible_facts:
    #     vlan_ranges: 1,10-12,15,20-22

    # TASK [Invoke vlan_expander filter plugin]
    # ok: [host] => changed=false
    #   ansible_facts:
    #     extended_vlans:
    #     - 1
    #     - 10
    #     - 11
    #     - 12
    #     - 15
    #     - 20
    #     - 21
    #     - 22







Authors
~~~~~~~

- Akira Yokochi (@akira6592)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
