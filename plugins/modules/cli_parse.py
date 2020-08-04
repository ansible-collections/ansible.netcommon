#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The cli_parse module
"""

from __future__ import absolute_import, division, print_function

# pylint: disable=invalid-name
__metaclass__ = type
# pylint: enable=invalid-name


DOCUMENTATION = """
module: cli_parse
author: Bradley Thornton (@cidrblock)
short_description: Parse cli output or text using a variety of parsers
description:
- Parse cli output or text using a variety of parsers
version_added: 0.0.1
options:
    command:
        type: str
        description:
        - The command to run on the host
    text:
        type: str
        description:
        - Text to be parsed
    parser:
        type: dict
        description:
        - Parser specfic parameters
        suboptions:
            name:
                type: str
                description:
                - The name of the parser to use
                required: True
            command:
                type: str
                description:
                - The command used to locate the parser's template
            os:
                type: str
                description: Provide an os to the parser
            template_path:
                type: str
                description:
                - Path of the parser template on the Ansible controller.
                - This can be a relative or an absolute path.
    set_fact:
        description:
        - Set the resulting parsed data as a fact
        type: str


notes:
- The default search path for a parser template is templates/{{ short_os }}_{{ command }}.{{ extension }}
- => short_os derived from ansible_network_os or ansible_distribution and set to lower case
- => command is the command passed to the module with spaces replaced with _
- => extension is specific to the parser used (native=yaml, textfsm=textfsm, ttp=ttp)
- The default Ansible search path for the templates directory is used for parser templates as well
- Some parsers require third-party python libraries be installed on the Ansible control node
- e.g. Pyats requires pyats and genie
- e.g. ntc_templates requires ntc_templates
- e.g. textfsm requires textfsm
- e.g. ttp requires ttp
- e.g. xml requires xml_to_dict
"""

EXAMPLES = r"""

# Using the native parser

# -------------
# templates/nxos_show_interface.yaml
# - example: Ethernet1/1 is up
#   getval: '(?P<name>\S+) is (?P<oper_state>\S+)'
#   result:
#     "{{ name }}":
#         name: "{{ name }}"
#         state:
#         operating: "{{ oper_state }}"
#   shared: True
#
# - example: admin state is up, Dedicated Interface
#   getval: 'admin state is (?P<admin_state>\S+)'
#   result:
#     "{{ name }}":
#         name: "{{ name }}"
#         state:
#         admin: "{{ admin_state }}"
#
# - example: "  Hardware: Ethernet, address: 5254.005a.f8b5 (bia 5254.005a.f8b5)"
#   getval: '\s+Hardware: (?P<hardware>.*), address: (?P<mac>\S+)'
#   result:
#     "{{ name }}":
#         hardware: "{{ hardware }}"
#         mac_address: "{{ mac }}"

- name: Run command and parse with native
  ansible.netcommon.cli_parse:
    command: "show interface"
    parser:
      name: ansible.netcommon.native
    set_fact: interfaces_fact


- name: Pass text and template_path
  ansible.netcommon.cli_parse:
    text: "{{ previous_command['stdout'] }}"
    parser:
      name: ansible.netcommon.native
      template_path: "{{ role_path }}/templates/nxos_show_interface.yaml"


# Using the ntc_templates parser

# -------------
# The ntc_templates use 'vendor_platform' for the file name
# it will be derived from ansible_network_os if not provided
# e.g. cisco.ios.ios => cisco_ios

- name: Run command and parse with ntc_templates
  ansible.netcommon.cli_parse:
    command: "show interface"
    parser:
      name: ansible.netcommon.ntc_templates
  register: parser_output

- name: Pass text and command
  ansible.netcommon.cli_parse:
    text: "{{ previous_command['stdout'] }}"
    parser:
      name: ansible.netcommon.ntc_templates
      command: show interface
  register: parser_output


# Using the pyats parser

# -------------
# The pyats parser uses 'os' to locate the appropriate parser
# it will be derived from ansible_network_os if not provided
# in the case of pyats: cisco.ios.ios => iosxe

- name: Run command and parse with pyats
  ansible.netcommon.cli_parse:
    command: "show interface"
    parser:
        name: ansible.netcommon.pyats
  register: parser_output

- name: Pass text and command
  ansible.netcommon.cli_parse:
    text: "{{ previous_command['stdout'] }}"
    parser:
        name: ansible.netcommon.pyats
        command: show interface
  register: parser_output

- name: Provide an OS to the pyats to use an ios parser
  ansible.netcommon.cli_parse:
    text: "{{ previous_command['stdout'] }}"
    parser:
        name: ansible.netcommon.pyats
        command: show interface
        os: ios
  register: parser_output


# Using the textfsm parser

# -------------
# templates/nxos_show_version.textfsm
#
# Value UPTIME ((\d+\s\w+.s.,?\s?){4})
# Value LAST_REBOOT_REASON (.+)
# Value OS (\d+.\d+(.+)?)
# Value BOOT_IMAGE (.*)
# Value PLATFORM (\w+)
#
# Start
#   ^\s+(NXOS: version|system:\s+version)\s+${OS}\s*$$
#   ^\s+(NXOS|kickstart)\s+image\s+file\s+is:\s+${BOOT_IMAGE}\s*$$
#   ^\s+cisco\s+${PLATFORM}\s+[cC]hassis
#   ^\s+cisco\s+Nexus\d+\s+${PLATFORM}
#   # Cisco N5K platform
#   ^\s+cisco\s+Nexus\s+${PLATFORM}\s+[cC]hassis
#   ^\s+cisco\s+.+-${PLATFORM}\s*
#   ^Kernel\s+uptime\s+is\s+${UPTIME}
#   ^\s+Reason:\s${LAST_REBOOT_REASON} -> Record

- name: Run command and parse with textfsm
  ansible.netcommon.cli_parse:
    command: "show version"
    parser:
      name: ansible.netcommon.textfsm
  register: parser_output

- name: Pass text and command
  ansible.netcommon.cli_parse:
    text: "{{ nxos_textfsm_command['stdout'] }}"
    parser:
      name: ansible.netcommon.textfsm
      command: show version
  register: parser_output

# Using the ttp parser

# -------------
# templates/nxos_show_interface.ttp
#
# {{ interface }} is {{ state }}
# admin state is {{ admin_state }}{{ ignore(".*") }}

- name: Run command and parse with ttp
  ansible.netcommon.cli_parse:
    command: "show interface"
    parser:
      name: ansible.netcommon.ttp
    set_fact: new_fact_key

- name: Pass text and template_path
  ansible.netcommon.cli_parse:
    text: "{{ previous_command['stdout'] }}"
    parser:
      name: ansible.netcommon.ttp
      template_path: "{{ role_path }}/templates/nxos_show_interface.ttp"
  register: parser_output

# Using the XML parser

# -------------
- name: Run command and parse with xml
  ansible.netcommon.cli_parse:
    command: "show interface | xml"
    parser:
      name: ansible.netcommon.xml
  register: parser_output

- name: Pass text and parse with xml
  ansible.netcommon.cli_parse:
    text: "{{ previous_command['stdout'] }}"
    parser:
      name: ansible.netcommon.xml
  register: parser_output
"""

RETURN = r"""
parsed:
  description: The structured data resulting from the parsing of the text
  returned: always
  type: dict
  sample:
stdout:
  description: The output from the command run
  returned: when provided a command
  type: str
  sample:
stdout_lines:
  description: The output od the command run split into lines
  returned: when provided a command
  type: list
  sample:
"""

# pylint: disable=wrong-import-position
from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import (
    Connection,
    ConnectionError as AnsibleConnectionError,
)

# pylint: enable=wrong-import-position

SPEC = {
    "argument_spec": {
        "command": {"type": "str"},
        "text": {"type": "str"},
        "parser": {
            "type": "dict",
            "required": True,
            "options": {
                "name": {"type": "str", "required": True},
                "command": {"type": "str"},
                "os": {"type": "str"},
                "template_path": {"type": "str"},
            },
            "mutually_exclusive": [["command", "template_path"]],
        },
        "set_fact": {"type": "str"},
    },
    "required_one_of": [["command", "text"]],
    "mutually_exclusive": [["command", "text"]],
}


def main():
    """entry point for module execution
    """

    module = AnsibleModule(**SPEC)

    if len(module.params.get("parser").get("name").split(".")) != 3:
        module.fail_json(
            msg="Parser name should be provided as a full name including collection"
        )

    command = module.params.get("command")

    if command:
        socket_path = module._socket_path  # pylint:disable=protected-access
        if socket_path:
            # pylint:disable=protected-access
            connection = Connection(module._socket_path)
            # pylint:enable=protected-access
            try:
                response = connection.get(command=command)
                module.exit_json(stdout=response)
            except AnsibleConnectionError as exc:
                module.fail_json(msg=to_text(exc))
        else:
            return_code, out, err = module.run_command(command)
            if return_code:
                module.fail_json(msg=err)
            module.exit_json(stdout=out)

    module.exit_json()


if __name__ == "__main__":
    main()
