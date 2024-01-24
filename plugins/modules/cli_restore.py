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
  config:
    description:
    - The config to be pushed to the network device. This argument is mutually exclusive
      with C(rollback) and either one of the option should be given as input. To ensure
      idempotency and correct diff the configuration lines should be similar to how they
      appear if present in the running configuration on device including the indentation.
    type: str
  commit:
    description:
    - The C(commit) argument instructs the module to push the configuration to the
      device. This is mapped to module check mode.
    type: bool
  rollback:
    description:
    - The C(rollback) argument instructs the module to rollback the current configuration
      to the identifier specified in the argument.  If the specified rollback identifier
      does not exist on the remote device, the module will fail. To rollback to the
      most recent commit, set the C(rollback) argument to 0. This option is mutually
      exclusive with C(config).
    type: int
  commit_comment:
    description:
    - The C(commit_comment) argument specifies a text string to be used when committing
      the configuration. If the C(commit) argument is set to False, this argument
      is silently ignored. This argument is only valid for the platforms that support
      commit operation with comment.
    type: str
"""

EXAMPLES = """
- name: Restore nxos configuration
  ansible.netcommon.cli_restore:
    config: "{{ lookup('file', 'backup_nxos.cfg') }}"
"""

RETURN = """
backup_path:
  description: The full path to the backup file
  returned: always
  type: str
  sample: /playbooks/ansible/backup/hostname_config.2016-07-16@22:28:34
"""

import json

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection


def validate_args(module, device_operations):
    """validate param if it is supported on the platform"""
    feature_list = []
    import q

    for feature in feature_list:
        if module.params[feature]:
            q(feature)
            supports_feature = device_operations.get("supports_%s" % feature)
            q(supports_feature)
            if supports_feature is None:
                module.fail_json(
                    msg="Thisdfvdfdsd platform does not specify whether %s is supported or not. "
                    "Please report an issue against this platform's cliconf plugin." % feature
                )
            elif not supports_feature:
                module.fail_json(msg="Option %s is not supported on this platform" % feature)


def run(module, device_operations, connection, candidate, running, rollback_id):
    result = {}
    resp = {}
    config_diff = []
    banner_diff = {}

    commit_comment = module.params["commit_comment"]

    commit = not module.check_mode

    if rollback_id is not None:
        resp = connection.rollback(rollback_id, commit)
        if "diff" in resp:
            result["changed"] = True

    elif device_operations.get("supports_onbox_diff"):
        if candidate and not isinstance(candidate, list):
            candidate = candidate.strip("\n").splitlines()

        kwargs = {
            "candidate": candidate,
            "commit": commit,
            "replace": None,
            "comment": commit_comment,
        }
        resp = connection.edit_config(**kwargs)

        if "diff" in resp:
            result["changed"] = True
            result["diff"] = resp["diff"]

    elif device_operations.get("supports_generate_diff"):
        kwargs = {"candidate": candidate, "running": running}

        diff_response = connection.get_diff(**kwargs)

        config_diff = diff_response.get("config_diff")
        banner_diff = diff_response.get("banner_diff")

        if config_diff:
            if isinstance(config_diff, list):
                candidate = config_diff
            else:
                candidate = config_diff.splitlines()

            kwargs = {
                "candidate": candidate,
                "commit": commit,
                "replace": None,
                "comment": commit_comment,
            }
            if commit:
                connection.edit_config(**kwargs)
            result["changed"] = True
            result["commands"] = config_diff.split("\n")

        if banner_diff:
            candidate = json.dumps(banner_diff)

            kwargs = {"candidate": candidate, "commit": commit}
            if commit:
                connection.edit_banner(**kwargs)
            result["changed"] = True

    if module._diff:
        if "diff" in resp:
            result["diff"] = {"prepared": resp["diff"]}
        else:
            diff = ""
            if config_diff:
                if isinstance(config_diff, list):
                    diff += "\n".join(config_diff)
                else:
                    diff += config_diff
            if banner_diff:
                diff += json.dumps(banner_diff)
            result["diff"] = {"prepared": diff}

    if result.get("changed"):
        msg = (
            "To ensure idempotency and correct diff the input configuration lines should be"
            " similar to how they appear if present in"
            " the running configuration on device including the indentation"
        )
        if "warnings" in result:
            result["warnings"].append(msg)
        else:
            result["warnings"] = msg
    return result


def main():
    """main entry point for execution"""
    argument_spec = dict(
        config=dict(type="str"),
        commit=dict(type="bool"),
        commit_comment=dict(type="str"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=[
            "config",
        ],
        supports_check_mode=False,
    )

    result = {"changed": False}

    connection = Connection(module._socket_path)
    capabilities = module.from_json(connection.get_capabilities())
    import q

    q(capabilities)
    if capabilities:
        device_operations = capabilities.get("device_operations", dict())
        validate_args(module, device_operations)
    else:
        device_operations = dict()

    candidate = module.params["config"]
    candidate = to_text(candidate, errors="surrogate_then_replace") if candidate else None

    if candidate:
        try:
            result.update(
                run(
                    module,
                    device_operations,
                    connection,
                    candidate,
                    None,
                    None,
                )
            )
        except Exception as exc:
            module.fail_json(msg=to_text(exc))

    module.exit_json(**result)


if __name__ == "__main__":
    main()
