#
# Copyright 2018 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
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
            True if module_name == "grpc_nw_config" else False
        )
        persistent_connection = self._play_context.connection.split(".")[-1]
        warnings = []

        if persistent_connection != "grpc" and module_name == "grpc_nw_config":
            return {
                "failed": True,
                "msg": "Connection type %s is not valid for netconf_config module. "
                "Valid connection type is grpc"
                % self._play_context.connection,
            }
        if module_name == "grpc_nw_config":
            args = self._task.args
            pc = copy.deepcopy(self._play_context)
            pc.connection = "ansible.netcommon.grpc"
            pc.port = int(args.get("port") or self._play_context.port or 57777)

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

            socket_path = connection.run()
            display.vvvv("socket_path: %s" % socket_path, pc.remote_addr)
            if not socket_path:
                return {
                    "failed": True,
                    "msg": "unable to open shell. Please see: "
                    + "https://docs.ansible.com/ansible/network_debug_troubleshooting.html#unable-to-open-shell",
                }

            task_vars["ansible_socket"] = socket_path

        result = super(ActionModule, self).run(task_vars=task_vars)
        if warnings:
            if "warnings" in result:
                result["warnings"].extend(warnings)
            else:
                result["warnings"] = warnings
        return result
