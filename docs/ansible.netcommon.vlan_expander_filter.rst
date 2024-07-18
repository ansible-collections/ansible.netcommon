.. _ansible.netcommon.vlan_expander_filter:


*******************************
ansible.netcommon.vlan_expander
*******************************

**The vlan_expander filter plugin.**


Version added: 2.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Expand shorthand list of VLANs to list all VLANs. Inverse of vlan_parser
- Using the parameters below - ``vlans_data | ansible.netcommon.vlan_expander``




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
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>This option represents a string containing the range of vlans.</div>
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




Status
------


Authors
~~~~~~~

- Akira Yokochi (@akira6592)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
