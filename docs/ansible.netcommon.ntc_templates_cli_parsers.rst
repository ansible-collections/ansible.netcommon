.. _ansible.netcommon.ntc_templates_cli_parsers:


*******************************
ansible.netcommon.ntc_templates
*******************************

**Define configurable options for ``ntc_templates`` sub-plugin of ``cli_parse`` module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This plugin documentation provides the configurable options that can be passed to the *ansible.utils.cli_parse* plugins when *ansible.netcommon.ntc_templates* is used as a value for *name* option.







Examples
--------

.. code-block:: yaml

    - name: "Run command and parse with ntc_templates"
      ansible.utils.cli_parse:
        command: "show interface"
        parser:
          name: ansible.netcommon.ntc_templates
      register: nxos_ntc_templates_command

    - name: "Pass text and command"
      ansible.utils.cli_parse:
        text: "{{ nxos_ntc_templates_command['stdout'] }}"
        parser:
          name: ansible.netcommon.ntc_templates
          command: show interface
      register: nxos_ntc_templates_text




Status
------


Authors
~~~~~~~

- Bradley Thornton (@cidrblock)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
