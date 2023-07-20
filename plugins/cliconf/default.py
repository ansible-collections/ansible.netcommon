# (c) 2023 Red Hat Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
author: Ansible Networking Team (@ansible-network)
name: default
short_description: General purpose cliconf plugin for new platforms
description:
- This plugin attemts to provide low level abstraction apis for sending and receiving CLI
  commands from arbitrary network devices.
version_added: 5.2.0
"""

import json

from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils.common._collections_compat import Mapping
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import to_list
from ansible_collections.ansible.netcommon.plugins.plugin_utils.cliconf_base import CliconfBase


class Cliconf(CliconfBase):
    __rpc__ = CliconfBase.__rpc__ + [
        "run_commands",
    ]

    def __init__(self, *args, **kwargs):
        super(Cliconf, self).__init__(*args, **kwargs)
        self._device_info = {}

    def get_device_info(self):
        if not self._device_info:
            device_info = {}

            device_info["network_os"] = "default"
        return self._device_info

    def get_config(self, flags=None, format=None):
        raise NotImplementedError

    def edit_config(self, candidate=None, commit=True, replace=None, comment=None):
        raise NotImplementedError

    def get(
        self,
        command=None,
        prompt=None,
        answer=None,
        sendonly=False,
        newline=True,
        output=None,
        check_all=False,
    ):
        if not command:
            raise ValueError("must provide value of command to execute")

        return self.send_command(
            command=command,
            prompt=prompt,
            answer=answer,
            sendonly=sendonly,
            newline=newline,
            check_all=check_all,
        )

    def run_commands(self, commands=None, check_rc=True):
        if commands is None:
            raise ValueError("'commands' value is required")

        responses = list()
        for cmd in to_list(commands):
            if not isinstance(cmd, Mapping):
                cmd = {"command": cmd}

            try:
                out = self.send_command(**cmd)
            except AnsibleConnectionFailure as e:
                if check_rc:
                    raise
                out = getattr(e, "err", e)

            responses.append(out)

        return responses

    def get_device_operations(self):
        return {
            "supports_diff_replace": False,
            "supports_commit": False,
            "supports_rollback": False,
            "supports_defaults": False,
            "supports_onbox_diff": False,
            "supports_commit_comment": False,
            "supports_multiline_delimiter": False,
            "supports_diff_match": False,
            "supports_diff_ignore_lines": False,
            "supports_generate_diff": False,
            "supports_replace": False,
        }

    def get_capabilities(self):
        result = super(Cliconf, self).get_capabilities()
        result["device_operations"] = self.get_device_operations()
        result.update(self.get_option_values())
        return json.dumps(result)
