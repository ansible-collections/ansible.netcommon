.. _ansible.netcommon.parse_cli_filter:


***************************
ansible.netcommon.parse_cli
***************************

**parse_cli filter plugin.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The filter plugins converts the output of a network device CLI command into structured JSON output.
- Using the parameters below - ``xml_data | ansible.netcommon.parse_cli(template.yml``)
- This plugin is deprecated and will be removed in a future release after 2027-02-01, please Use ansible.utils.cli_parse instead.




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
                    <b>output</b>
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
                        <div>This source data on which parse_cli invokes.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tmpl</b>
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
                        <div>The spec file should be valid formatted YAML. It defines how to parse the CLI output and return JSON data.</div>
                        <div>For example <code>cli_data | ansible.netcommon.parse_cli(template.yml</code>), in this case <code>cli_data</code> represents cli output.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - The parse_cli filter will load the spec file and pass the command output through it, returning JSON output. The YAML spec file defines how to parse the CLI output



Examples
--------

.. code-block:: yaml

    # Using parse_cli

    # outputConfig

    # ip dhcp pool Data
    #   import all
    #   network 192.168.1.0 255.255.255.0
    #   update dns
    #   default-router 192.168.1.1
    #   dns-server 192.168.1.1 8.8.8.8
    #   option 42 ip 192.168.1.1
    #   domain-name test.local
    #   lease 8

    # pconnection.yml

    # ---
    # vars:
    #   dhcp_pool:
    #     name: "{{ item.name }}"
    #     network: "{{ item.network_ip }}"
    #     subnet: "{{ item.network_subnet }}"
    #     dns_servers: "{{ item.dns_servers_1 }}{{ item.dns_servers_2 }}"
    #     domain_name: "{{ item.domain_name_0 }}{{ item.domain_name_1 }}{{ item.domain_name_2 }}{{ item.domain_name_3 }}"
    #     options: "{{ item.options_1 }}{{ item.options_2 }}"
    #     lease_days: "{{ item.lease_days }}"
    #     lease_hours: "{{ item.lease_hours }}"
    #     lease_minutes: "{{ item.lease_minutes }}"

    # keys:
    #   dhcp_pools:
    #     value: "{{ dhcp_pool }}"
    #     items: "^ip dhcp pool (
    #           ?P<name>[^\\n]+)\\s+(?:import (?P<import_all>all)\\s*)?(?:network (?P<network_ip>[\\d.]+)
    #           (?P<network_subnet>[\\d.]+)?\\s*)?(?:update dns\\s*)?(?:host (?P<host_ip>[\\d.]+)
    #           (?P<host_subnet>[\\d.]+)\\s*)?(?:domain-name (?P<domain_name_0>[\\w._-]+)\\s+)?
    #           (?:default-router (?P<default_router>[\\d.]+)\\s*)?(?:dns-server
    #           (?P<dns_servers_1>(?:[\\d.]+ ?)+ ?)+\\s*)?(?:domain-name (?P<domain_name_1>[\\w._-]+)\\s+)?
    #           (?P<options_1>(?:option [^\\n]+\\n*\\s*)*)?(?:domain-name (?P<domain_name_2>[\\w._-]+)\\s+)?(?P<options_2>(?:option [^\\n]+\\n*\\s*)*)?
    #           (?:dns-server (?P<dns_servers_2>(?:[\\d.]+ ?)+ ?)+\\s*)?(?:domain-name
    #           (?P<domain_name_3>[\\w._-]+)\\s*)?(lease (?P<lease_days>\\d+)(?: (?P<lease_hours>\\d+))?(?: (?P<lease_minutes>\\d+))?\\s*)?(?:update arp)?"

    # playbook

    - name: Add config data
      ansible.builtin.set_fact:
        opconfig: "{{lookup('ansible.builtin.file', 'outputConfig') }}"

    - name: Parse Data
      ansible.builtin.set_fact:
        output: "{{ opconfig | parse_cli('pconnection.yml') }}"


    # Task Output
    # -----------
    #
    # TASK [Add config data]
    # ok: [host] => changed=false
    #   ansible_facts:
    #     xml: |-
    #       ip dhcp pool Data
    #         import all
    #         network 192.168.1.0 255.255.255.0
    #         update dns
    #         default-router 192.168.1.1
    #         dns-server 192.168.1.1 8.8.8.8
    #         option 42 ip 192.168.1.1
    #         domain-name test.local
    #         lease 8

    # TASK [Parse Data]
    # ok: [host] => changed=false
    #   ansible_facts:
    #     output:
    #       dhcp_pools:
    #       - dns_servers: 192.168.1.1 8.8.8.8
    #         domain_name: test.local
    #         lease_days: 8
    #         lease_hours: null
    #         lease_minutes: null
    #         name: Data
    #         network: 192.168.1.0
    #         options: |-
    #           option 42 ip 192.168.1.1
    #         subnet: 255.255.255.0




Status
------


Authors
~~~~~~~

- Peter Sprygada (@privateip)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
