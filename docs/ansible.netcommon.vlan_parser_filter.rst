
.. Created with antsibull-docs 2.9.0

ansible.netcommon.vlan_parser filter -- The vlan\_parser filter plugin.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This filter plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.vlan_parser``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- The filter plugin converts a list of vlans to IOS like vlan configuration.
- Converts list to a list of range of numbers into multiple lists.
- \ :literal:`vlans\_data | ansible.netcommon.vlan\_parser(first\_line\_len = 20, other\_line\_len=20`\ )








Keyword parameters
------------------

This describes keyword parameters of the filter. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
example: ``input | ansible.netcommon.vlan_parser(key1=value1, key2=value2, ...)``

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
        <span style="color: purple;">list</span>
        / <span style="color: purple;">elements=string</span>
        / <span style="color: red;">required</span>
      </p>

    </td>
    <td valign="top">
      <p>This option represents a list containing vlans.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-first_line_len"></div>
      <p style="display: inline;"><strong>first_line_len</strong></p>
      <a class="ansibleOptionLink" href="#parameter-first_line_len" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>

    </td>
    <td valign="top">
      <p>The first line of the list can be first_line_len characters long.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">48</code></p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-other_line_len"></div>
      <p style="display: inline;"><strong>other_line_len</strong></p>
      <a class="ansibleOptionLink" href="#parameter-other_line_len" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">integer</span>
      </p>

    </td>
    <td valign="top">
      <p>The subsequent list lines can be other_line_len characters.</p>
      <p style="margin-top: 8px;"><b style="color: blue;">Default:</b> <code style="color: blue;">44</code></p>
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


    # Using vlan_parser

    - name: Setting host facts for vlan_parser filter plugin
      ansible.builtin.set_fact:
        vlans:
          [
            100,
            1688,
            3002,
            3003,
            3004,
            3005,
            3102,
            3103,
            3104,
            3105,
            3802,
            3900,
            3998,
            3999,
          ]

    - name: Invoke vlan_parser filter plugin
      ansible.builtin.set_fact:
        vlans_ranges: "{{ vlans | ansible.netcommon.vlan_parser(first_line_len = 20, other_line_len=20) }}"


    # Task Output
    # -----------
    #
    # TASK [Setting host facts for vlan_parser filter plugin]
    # ok: [host] => changed=false
    #   ansible_facts:
    #     vlans:
    #     - 100
    #     - 1688
    #     - 3002
    #     - 3003
    #     - 3004
    #     - 3005
    #     - 3102
    #     - 3103
    #     - 3104
    #     - 3105
    #     - 3802
    #     - 3900
    #     - 3998
    #     - 3999

    # TASK [Invoke vlan_parser filter plugin]
    # ok: [host] => changed=false
    #   ansible_facts:
    #     msg:
    #     - 100,1688,3002-3005
    #     - 3102-3105,3802,3900
    #     - 3998,3999







Authors
~~~~~~~

- Steve Dodd (@idahood)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
