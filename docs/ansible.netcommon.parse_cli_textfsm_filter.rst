.. _ansible.netcommon.parse_cli_textfsm_filter:


***********************************
ansible.netcommon.parse_cli_textfsm
***********************************

**parse_cli_textfsm filter plugin.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The network filters also support parsing the output of a CLI command using the TextFSM library. To parse the CLI output with TextFSM use this filter.
- Using the parameters below - ``data | ansible.netcommon.parse_cli_textfsm(template.yml``)




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
                    <b>template</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The template to compare it with.</div>
                        <div>For example <code>data | ansible.netcommon.parse_cli_textfsm(template.yml</code>), in this case <code>data</code> represents this option.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">raw</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>This source data on which parse_cli_textfsm invokes.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Use of the TextFSM filter requires the TextFSM library to be installed.



Examples
--------

.. code-block:: yaml

    # Using parse_cli_textfsm

    - name: "Fetch command output"
      cisco.ios.ios_command:
        commands:
          - show lldp neighbors
      register: lldp_output

    - name: "Invoke parse_cli_textfsm"
      ansible.builtin.set_fact:
        device_neighbors: "{{ lldp_output.stdout[0] | parse_cli_textfsm('~/ntc-templates/templates/cisco_ios_show_lldp_neighbors.textfsm') }}"

    - name: "Debug"
      ansible.builtin.debug:
        msg: "{{ device_neighbors }}"

    # Task Output
    # -----------
    #
    # TASK [Fetch command output]
    # ok: [rtr-1]

    # TASK [Invoke parse_cli_textfsm]
    # ok: [rtr-1]

    # TASK [Debug]
    # ok: [rtr-1] => {
    #     "msg": [
    #         {
    #             "CAPABILITIES": "R",
    #             "LOCAL_INTERFACE": "Gi0/0",
    #             "NEIGHBOR": "rtr-3",
    #             "NEIGHBOR_INTERFACE": "Gi0/0"
    #         },
    #         {
    #             "CAPABILITIES": "R",
    #             "LOCAL_INTERFACE": "Gi0/1",
    #             "NEIGHBOR": "rtr-1",
    #             "NEIGHBOR_INTERFACE": "Gi0/1"
    #         }
    #     ]
    # }




Status
------


Authors
~~~~~~~

- Peter Sprygada (@privateip)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
