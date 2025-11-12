# (c) 2018, Ansible Inc,
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import os
import tempfile

from ansible.module_utils.common.text.converters import to_bytes, to_text
from ansible.plugins.action import ActionBase
from ansible.plugins.loader import lookup_loader
from ansible.utils.display import Display
from ansible.utils.hashing import checksum


display = Display()


class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(task_vars=task_vars)

        if "changed" not in result:
            result["changed"] = False

        persistent_connection = self._play_context.connection.split(".")[-1]
        if persistent_connection != "network_cli":
            # It is supported only with network_cli
            return {
                "failed": True,
                "msg": (
                    "connection type %s is not valid for net_put module, please use fully "
                    "qualified name of network_cli connection type" % self._play_context.connection
                ),
            }

        try:
            self._src = self._task.args.get("src")
        except KeyError as exc:
            return {
                "failed": True,
                "msg": "missing required argument: %s" % exc,
            }

        self._check_destination = self._task.args.get("check_destination", True)
        self._decrypt = self._task.args.get("decrypt", True)
        self._dest = self._task.args.get("dest", self._src)
        self._mode = self._task.args.get("mode", "binary")
        self._protocol = self._task.args.get("protocol", "scp")

        working_path = self._get_working_path()
        if os.path.isabs(self._src):
            self._src_real_file = self._loader.get_real_file(self._src, decrypt=self._decrypt)
        elif self._loader.path_dwim_relative(working_path, "templates", self._src) != "":
            self._src_real_file = self._loader.path_dwim_relative(
                working_path, "templates", self._src
            )
        elif self._loader.path_dwim_relative(working_path, self._src):
            self._src_real_file = self._loader.path_dwim_relative(working_path, self._src)

        try:
            fetched_fd, fetched_fp = tempfile.mkstemp(prefix="")
            rendered_fd, rendered_fp = tempfile.mkstemp(prefix="")

            if "binary" == self._mode:
                self._rendered_real_file = self._src_real_file
            elif "text" == self._mode:
                self._rendered_real_file = rendered_fp
                lookup = lookup_loader.get(
                    "ansible.builtin.template", loader=self._loader, templar=self._templar
                )
                template_result = lookup.run([self._src], variables=task_vars)

                with open(self._rendered_real_file, "wb") as fh:
                    fh.write(to_bytes(template_result[0]))
            self._rendered_checksum = checksum(self._rendered_real_file)

            display.vv(
                "The rendered (if applicable) source file %s checksum is %s"
                % (self._rendered_real_file, self._rendered_checksum)
            )

            try:
                self._connection.get_file(self._dest, fetched_fp, self._protocol)
            except Exception as exc:
                error = to_text(exc).lower()
                if not (
                    "error receiving information about file" in error
                    or "no such file or directory" in error
                ):
                    raise exc
            self._dest_checksum = checksum(fetched_fp)

            if self._dest_checksum != self._rendered_checksum:
                result["changed"] = True

                if self._task._diff:
                    if "binary" == self._mode:
                        result["prepared"] = (
                            "File checksum mismatch, will replace files! The source checksum is "
                            "%s and the destination is %s"
                            % (self._rendered_checksum, self._dest_checksum)
                        )

                    elif "text" == self._mode:
                        with open(fetched_fp, "r") as fh:
                            result["diff"] = {
                                "before": to_text(fh.read()),
                                "after": template_result[0],
                            }

                if not self._task.check_mode:
                    self._connection.copy_file(
                        self._loader.get_real_file(self._rendered_real_file),
                        self._dest,
                        self._protocol,
                    )

            return result
        finally:
            os.remove(fetched_fp)
            os.remove(rendered_fp)

    def _get_working_path(self):
        cwd = self._loader.get_basedir()
        if self._task._role is not None:
            cwd = self._task._role._role_path
        return cwd
