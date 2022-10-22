#
# Copyright 2018 Red Hat Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy
import sys

from ansible.utils.display import Display
from ansible_collections.ansible.netcommon.plugins.action.network import (
    ActionModule as ActionNetworkModule,
)

display = Display()


class ActionModule(ActionNetworkModule):
    def run(self, tmp=None, task_vars=None):
        del tmp  # tmp no longer has any effect

        module_name = self._task.action.split(".")[-1]
        self._config_module = (
            True if module_name == "netconf_config" else False
        )
        persistent_connection = self._play_context.connection.split(".")[-1]
        warnings = []

        if (
            persistent_connection not in ["netconf", "local"]
            and module_name == "netconf_config"
        ):
            return {
                "failed": True,
                "msg": "Connection type %s is not valid for netconf_config module. "
                "Valid connection type is netconf or local (deprecated)"
                % self._play_context.connection,
            }
        elif (
            persistent_connection not in ["netconf"]
            and module_name != "netconf_config"
        ):
            return {
                "failed": True,
                "msg": "Connection type %s is not valid for %s module. "
                "Valid connection type is netconf."
                % (self._play_context.connection, module_name),
            }

        if (
            self._play_context.connection == "local"
            and module_name == "netconf_config"
        ):
            args = self._task.args
            pc = copy.deepcopy(self._play_context)
            pc.connection = "ansible.netcommon.netconf"
            pc.port = int(args.get("port") or self._play_context.port or 830)

            pc.remote_user = (
                args.get("username") or self._play_context.connection_user
            )
            pc.password = args.get("password") or self._play_context.password
            pc.private_key_file = (
                args.get("ssh_keyfile") or self._play_context.private_key_file
            )

            connection = self._shared_loader_obj.connection_loader.get(
                "ansible.netcommon.persistent",
                pc,
                sys.stdin,
                task_uuid=self._task._uuid,
            )

            # TODO: Remove below code after ansible minimal is cut out
            if connection is None:
                pc.connection = "netconf"
                connection = self._shared_loader_obj.connection_loader.get(
                    "persistent", pc, sys.stdin, task_uuid=self._task._uuid
                )

            display.vvv(
                "using connection plugin %s (was local)" % pc.connection,
                pc.remote_addr,
            )

            timeout = args.get("timeout")
            command_timeout = (
                int(timeout)
                if timeout
                else connection.get_option("persistent_command_timeout")
            )
            connection.set_options(
                direct={
                    "persistent_command_timeout": command_timeout,
                    "look_for_keys": args.get("look_for_keys"),
                    "hostkey_verify": args.get("hostkey_verify"),
                    "allow_agent": args.get("allow_agent"),
                }
            )

            socket_path = connection.run()
            display.vvvv("socket_path: %s" % socket_path, pc.remote_addr)
            if not socket_path:
                return {
                    "failed": True,
                    "msg": "unable to open shell. Please see: "
                    + "https://docs.ansible.com/ansible/network_debug_troubleshooting.html#unable-to-open-shell",
                }

            task_vars["ansible_socket"] = socket_path
            warnings.append(
                [
                    "connection local support for this module is deprecated and will be removed in version 2.14, use connection %s"
                    % pc.connection
                ]
            )

        result = super(ActionModule, self).run(task_vars=task_vars)
        if warnings:
            if "warnings" in result:
                result["warnings"].extend(warnings)
            else:
                result["warnings"] = warnings
        return result
