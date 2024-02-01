#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2024, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type


DOCUMENTATION = """
module: cli_restore
author: Sagar Paul (@KB-perByte)
short_description: Restore device configuration to network devices over network_cli
description:
- This module provides platform agnostic way of restore text based configuration to
  network devices over network_cli connection plugin.
version_added: 6.1.0
extends_documentation_fragment:
- ansible.netcommon.network_agnostic
options:
  filename:
    description:
    - Filename of the backup file to be restored.
    type: str
  force:
    description:
    - The force keyword replaces the current running configuration file with the specified saved
      configuration file without prompting you for confirmation.
    type: bool
    default: False
"""

EXAMPLES = """
- name: Restore IOS-XE configuration
  ansible.netcommon.cli_restore:
    filename: test.cfg
    force: false
"""

RETURN = """
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection


def validate_args(module, device_operations):
    """validate param if it is supported on the platform"""
    feature_list = []

    for feature in feature_list:
        if module.params[feature]:
            supports_feature = device_operations.get(f"supports_{feature}")
            if supports_feature is None:
                module.fail_json(
                    msg=f"This platform does not specify whether {feature} is supported or not. "
                    "Please report an issue against this platform's cliconf plugin."
                )
            elif not supports_feature:
                module.fail_json(msg=f"Option {feature} is not supported on this platform")


def main():
    """main entry point for execution"""
    argument_spec = dict(
        force=dict(default=False, type="bool"),
        filename=dict(),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    result = {"changed": False}
    connection = Connection(module._socket_path)
    running = connection.restore(force=module.params["force"], filename=module.params["filename"])
    result["__restore__"] = running

    module.exit_json(**result)


if __name__ == "__main__":
    main()
