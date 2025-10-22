# (c) 2018, Ansible Inc,
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import os
import tempfile

from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
from ansible.utils.hashing import checksum


display = Display()


class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(task_vars=task_vars)

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

        self._src_real_file = self._loader.get_real_file(self._src, decrypt=self._decrypt)

        try:
            fetched_fd, fetched_fp = tempfile.mkstemp(prefix="")
            rendered_fd, rendered_fp = tempfile.mkstemp(prefix="")

            if self._mode == "binary":
                self._rendered_real_file = self._src_real_file
            elif self._mode == "text":
                self._rendered_real_file = rendered_fp
                template_result = self._execute_module(
                    module_name="ansible.builtin.template",
                    module_args={"dest": self._rendered_real_file, "src": self._src_real_file},
                    task_vars=task_vars,
                )
            self._rendered_checksum = checksum(self._rendered_real_file)

            display.vv(
                "The rendered (if applicable) source file %s checksum is %s"
                % (self._rendered_real_file, self._rendered_checksum)
            )

            try:
                self._connection._ssh_type_conn.fetch_file(self._dest, fetched_fp, self._protocol)
            except Exception as exc:
                if not (
                    "Error receiving information about file" in exc.message
                    and "No such file or directory" in exc.message
                ):
                    raise exc
                display.vv("The file is not present on the remote device")
            finally:
                self._connection._ssh_type_conn.reset()
                self._dest_checksum = checksum(fetched_fp)

            try:
                if self._dest_checksum != self._rendered_checksum:
                    self._connection._ssh_type_conn.put_file(
                        self._loader.get_real_file(self._rendered_real_file),
                        self._dest,
                        self._protocol,
                    )
            finally:
                self._connection._ssh_type_conn.reset()

            return result
        finally:
            os.remove(fetched_fp)
            os.remove(rendered_fp)
