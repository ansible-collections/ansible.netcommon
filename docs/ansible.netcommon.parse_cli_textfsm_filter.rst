
.. Created with antsibull-docs 2.9.0

ansible.netcommon.parse_cli_textfsm filter -- parse\_cli\_textfsm filter plugin.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

This filter plugin is part of the `ansible.netcommon collection <https://galaxy.ansible.com/ui/repo/published/ansible/netcommon/>`_ (version 6.1.0).

It is not included in ``ansible-core``.
To check whether it is installed, run ``ansible-galaxy collection list``.

To install it, use: :code:`ansible-galaxy collection install ansible.netcommon`.

To use it in a playbook, specify: ``ansible.netcommon.parse_cli_textfsm``.

New in ansible.netcommon 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------

- The network filters also support parsing the output of a CLI command using the TextFSM library. To parse the CLI output with TextFSM use this filter.
- Using the parameters below - \ :literal:`data | ansible.netcommon.parse\_cli\_textfsm(template.yml`\ )








Keyword parameters
------------------

This describes keyword parameters of the filter. These are the values ``key1=value1``, ``key2=value2`` and so on in the following
example: ``input | ansible.netcommon.parse_cli_textfsm(key1=value1, key2=value2, ...)``

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
      <div class="ansibleOptionAnchor" id="parameter-template"></div>
      <p style="display: inline;"><strong>template</strong></p>
      <a class="ansibleOptionLink" href="#parameter-template" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">string</span>
      </p>

    </td>
    <td valign="top">
      <p>The template to compare it with.</p>
      <p>For example <code class='docutils literal notranslate'>data | ansible.netcommon.parse_cli_textfsm(template.yml</code>), in this case <code class='docutils literal notranslate'>data</code> represents this option.</p>
    </td>
  </tr>
  <tr>
    <td valign="top">
      <div class="ansibleOptionAnchor" id="parameter-value"></div>
      <p style="display: inline;"><strong>value</strong></p>
      <a class="ansibleOptionLink" href="#parameter-value" title="Permalink to this option"></a>
      <p style="font-size: small; margin-bottom: 0;">
        <span style="color: purple;">any</span>
        / <span style="color: red;">required</span>
      </p>

    </td>
    <td valign="top">
      <p>This source data on which parse_cli_textfsm invokes.</p>
    </td>
  </tr>
  </tbody>
  </table>




Notes
-----

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







Authors
~~~~~~~

- Peter Sprygada (@privateip)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

Collection links
~~~~~~~~~~~~~~~~

* `Issue Tracker <https://github.com/ansible-collections/ansible.netcommon/issues>`__
* `Repository (Sources) <https://github.com/ansible-collections/ansible.netcommon>`__
