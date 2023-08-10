.. _ansible.netcommon.vlan_parser_filter:


*****************************
ansible.netcommon.vlan_parser
*****************************

**The vlan_parser filter plugin.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The filter plugin converts a list of vlans to IOS like vlan configuration.
- Converts list to a list of range of numbers into multiple lists.
- ``vlans_data | ansible.netcommon.vlan_parser(first_line_len = 20, other_line_len=20``)




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>data</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>This option represents a list containing vlans.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>first_line_len</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">48</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The first line of the list can be first_line_len characters long.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>other_line_len</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">44</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The subsequent list lines can be other_line_len characters.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
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




Status
------


Authors
~~~~~~~

- Steve Dodd (@idahood)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
