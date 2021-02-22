.. _ansible.netcommon.pyats_cli_parsers:


***********************
ansible.netcommon.pyats
***********************

**Define configurable options for ``pyats`` sub-plugin of ``cli_parse`` module**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This plugin documentation provides the configurable options that can be passed to the *ansible.utils.cli_parse* plugins when *ansible.netcommon.pyats* is used as a value for *name* option.







Examples
--------

.. code-block:: yaml

    - name: "Run command and parse with pyats"
      ansible.utils.cli_parse:
        command: "show interface"
        parser:
          name: ansible.netcommon.pyats
      register: nxos_pyats_command

    - name: "Pass text and command"
      ansible.utils.cli_parse:
        text: "{{ nxos_pyats_command['stdout'] }}"
        parser:
          name: ansible.netcommon.pyats
          command: show interface
      register: nxos_pyats_text




Status
------


Authors
~~~~~~~

- Bradley Thornton (@cidrblock)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
