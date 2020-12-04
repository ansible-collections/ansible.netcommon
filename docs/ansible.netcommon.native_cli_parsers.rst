.. _ansible.netcommon.native_cli_parsers:


************************
ansible.netcommon.native
************************

**Define configurable options for ``native`` sub-plugin of ``cli_parse`` module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This plugin documentation provides the configurable options that can be passed to the *ansible.utils.cli_parse* plugins when *ansible.netcommon.native* is used as a value for *name* option.







Examples
--------

.. code-block:: yaml

    - name: "Run command and parse with native"
      ansible.utils.cli_parse:
        command: "show interface"
        parser:
          name: ansible.netcommon.native
        set_fact: POpqMQoJWTiDpEW
      register: nxos_native_command

    - name: "Pass text and template_path"
      ansible.utils.cli_parse:
        text: "{{ nxos_native_command['stdout'] }}"
        parser:
          name: ansible.netcommon.native
          template_path: "/home/user/templates/nxos_show_interface.yaml"
      register: nxos_native_text




Status
------


Authors
~~~~~~~

- Bradley Thornton (@cidrblock)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
