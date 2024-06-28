
.. Created with antsibull-docs 2.9.0

ansible.netcommon.parse_cli filter -- parse\_cli filter plugin.
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This filter plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.parse_cli``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- The filter plugins converts the output of a network device CLI command into structured JSON output.
- Using the parameters below - \ :literal:`xml\_data | ansible.netcommon.parse\_cli(template.yml`\ )








Keyword parameters
------------------

This describes keyword parameters of the filter. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
example: ``input | ansible.netcommon.parse_cli(key1=value1, key2=value2, ...)``

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
      <div class="ansibleOptionAnchor" id="parameter-output"></div>
      <p style="display: inline;"><strong>output</strong></p>
      <a class="ansibleOptionLink" href="#parameter-output" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">any</span>
        / <span style="color: red;">required</span>
      </p>

    </td>
    <td valign="top">
      <p>This source data on which parse_cli invokes.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-tmpl"></div>
      <p style="display: inline;"><strong>tmpl</strong></p>
      <a class="ansibleOptionLink" href="#parameter-tmpl" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>The spec file should be valid formatted YAML. It defines how to parse the CLI output and return JSON data.</p>
      <p>For example <code class='docutils literal notranslate'>cli_data | ansible.netcommon.parse_cli(template.yml</code>), in this case <code class='docutils literal notranslate'>cli_data</code> represents cli output.</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

- The parse\_cli filter will load the spec file and pass the command output through it, returning JSON output. The YAML spec file defines how to parse the CLI output


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







Authors
~~~~~~~

- Peter Sprygada (@privateip)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
