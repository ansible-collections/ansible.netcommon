#
# (c) 2018 Red Hat Inc.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import os
import re
import time

from ansible.errors import AnsibleError
from ansible.module_utils._text import to_text
from ansible.module_utils.six import PY3
from ansible.module_utils.six.moves.urllib.parse import urlsplit
from ansible.plugins.action.normal import ActionModule as _ActionModule
from ansible.utils.display import Display
from ansible.utils.hashing import checksum, checksum_s
from ansible.vars.clean import remove_internal_keys


display = Display()

DEXEC_PREFIX = "ANSIBLE_NETWORK_IMPORT_MODULES:"


class ActionModule(_ActionModule):
    def run(self, tmp=None, task_vars=None):
        config_module = hasattr(self, "_config_module") and self._config_module
        if config_module and self._task.args.get("src"):
            try:
                self._handle_src_option()
            except AnsibleError as exc:
                return dict(failed=True, msg=to_text(exc))

        host = task_vars["ansible_host"]
        dexec_eligible = self._check_dexec_eligibility(host)

        # attempt to run using dexec
        if dexec_eligible:
            try:
                filename, module = self._find_load_module()
                display.vvvv(f"{DEXEC_PREFIX} found {self._task.action} at {filename}", host)

                if hasattr(module, "main"):
                    display.vvvv(f"{DEXEC_PREFIX} executing {self._task.action}", host)
                    result = self._execute_module(
                        module_name=self._task.action, task_vars=task_vars
                    )
                    display.vvvv(f"{DEXEC_PREFIX} execution complete", host)
                else:
                    display.vvvv(
                        f"{DEXEC_PREFIX} {self._task.action} does not define main(), falling back",
                        host,
                    )
                    dexec_eligible = False
            except Exception as e:
                display.warning(
                    f"{DEXEC_PREFIX} direct execution failed: {to_text(e)}. Falling back.", host
                )
                dexec_eligible = False

        if not dexec_eligible:
            result = super(ActionModule, self).run(tmp=tmp, task_vars=task_vars)

        if config_module and self._task.args.get("backup") and not result.get("failed"):
            self._handle_backup_option(result, task_vars, self._task.args.get("backup_options"))

        return result

    def _handle_backup_option(self, result, task_vars, backup_options):
        filename = None
        backup_path = None
        try:
            non_config_regexes = self._connection.cliconf.get_option("non_config_lines", task_vars)
        except (AttributeError, KeyError):
            non_config_regexes = []
        try:
            content = self._sanitize_contents(
                contents=result.pop("__backup__"), filters=non_config_regexes
            )
        except KeyError:
            raise AnsibleError("Failed while reading configuration backup")

        if backup_options:
            filename = backup_options.get("filename")
            backup_path = backup_options.get("dir_path")

        tstamp = time.strftime("%Y-%m-%d@%H:%M:%S", time.localtime(time.time()))
        if not backup_path:
            cwd = self._get_working_path()
            backup_path = os.path.join(cwd, "backup")
        if not filename:
            filename = "%s_config.%s" % (
                task_vars["inventory_hostname"],
                tstamp,
            )

        dest = os.path.join(backup_path, filename)
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        changed = False
        # Do not overwrite the destination if the contents match.
        if not os.path.exists(dest) or checksum(dest) != checksum_s(content):
            try:
                with open(dest, "w") as output_file:
                    output_file.write(content)
            except Exception as exc:
                result["failed"] = True
                result["msg"] = "Could not write to destination file %s: %s" % (
                    dest,
                    to_text(exc),
                )
                return
            changed = True

        result["backup_path"] = dest
        result["changed"] = changed

        result["date"], result["time"] = tstamp.split("@")
        if not (backup_options and backup_options.get("filename")):
            result["filename"] = os.path.basename(result["backup_path"])
            result["shortname"] = os.path.splitext(result["backup_path"])[0]

    def _get_working_path(self):
        cwd = self._loader.get_basedir()
        if self._task._role is not None:
            cwd = self._task._role._role_path
        return cwd

    def _handle_src_option(self, convert_data=True):
        src = self._task.args.get("src")
        working_path = self._get_working_path()

        if os.path.isabs(src) or urlsplit("src").scheme:
            source = src
        else:
            source = self._loader.path_dwim_relative(working_path, "templates", src)
            if not source:
                source = self._loader.path_dwim_relative(working_path, src)

        if not os.path.exists(source):
            raise AnsibleError("path specified in src not found")

        try:
            with open(source, "r") as f:
                template_data = to_text(f.read())
        except IOError as e:
            raise AnsibleError(
                f"unable to load src file {source}, I/O error({e.errno}): {e.strerror}"
            )

        # Create a template search path in the following order:
        # [working_path, self_role_path, dependent_role_paths, dirname(source)]
        searchpath = [working_path]
        if self._task._role is not None:
            searchpath.append(self._task._role._role_path)
            if hasattr(self._task, "_block:"):
                dep_chain = self._task._block.get_dep_chain()
                if dep_chain is not None:
                    for role in dep_chain:
                        searchpath.append(role._role_path)
        searchpath.append(os.path.dirname(source))
        self._templar.environment.loader.searchpath = searchpath
        self._task.args["src"] = self._templar.template(template_data)

    def _get_network_os(self, task_vars):
        if "network_os" in self._task.args and self._task.args["network_os"]:
            display.vvvv("Getting network OS from task argument")
            network_os = self._task.args["network_os"]
        elif self._play_context.network_os:
            display.vvvv("Getting network OS from inventory")
            network_os = self._play_context.network_os
        elif (
            "network_os" in task_vars.get("ansible_facts", {})
            and task_vars["ansible_facts"]["network_os"]
        ):
            display.vvvv("Getting network OS from fact")
            network_os = task_vars["ansible_facts"]["network_os"]
        else:
            raise AnsibleError("ansible_network_os must be specified on this host")

        return network_os

    def _check_dexec_eligibility(self, host):
        """Check if current python and task are eligble"""
        dexec = self.get_connection_option("import_modules")

        # log early about dexec
        if dexec:
            display.vvvv(f"{DEXEC_PREFIX} enabled", host)

            # disable dexec when not PY3
            if not PY3:
                dexec = False
                display.vvvv(f"{DEXEC_PREFIX} disabled for Python 2", host)

            # disable dexec when running async
            if self._task.async_val:
                dexec = False
                display.vvvv(f"{DEXEC_PREFIX} disabled for async task", host)
        else:
            display.vvvv(f"{DEXEC_PREFIX} disabled", host)
            display.vvvv(f"{DEXEC_PREFIX} module execution time may be extended", host)

        return dexec

    def _find_load_module(self):
        """Use the task action to find a module
        and import it.

        :return filename: The module's filename
        :rtype filename: str
        :return module: The loaded module file
        :rtype module: module
        """
        import importlib

        mloadr = self._shared_loader_obj.module_loader

        # 2.10
        try:
            context = mloadr.find_plugin_with_context(
                self._task.action, collection_list=self._task.collections
            )
            filename = context.plugin_resolved_path
            module = importlib.import_module(context.plugin_resolved_name)
        # 2.9
        except AttributeError:
            fullname, filename = mloadr.find_plugin_with_name(
                self._task.action, collection_list=self._task.collections
            )
            module = importlib.import_module(fullname)
        return filename, module

    def _exec_module(self, module):
        """exec the module's main() since modules
        print their result, we need to replace stdout
        with a buffer. If main() fails, we assume that as stderr
        Once we collect stdout/stderr, use our super to json load
        it or handle a traceback

        :param module: An loaded module
        :type module: A module file that was loaded
        :return module_result: The result of the module
        :rtype module_result: dict
        """
        import io
        import sys

        from ansible.module_utils._text import to_native

        # preserve previous stdout, replace with buffer
        sys_stdout = sys.stdout
        sys.stdout = io.StringIO()

        stdout = ""
        stderr = ""
        # run the module, catch the SystemExit so we continue
        try:
            module.main()
        except SystemExit:
            # module exited cleanly
            stdout = sys.stdout.getvalue()
        except Exception as exc:
            # dirty module or connection traceback
            stderr = to_native(exc)

        # restore stdout & stderr
        sys.stdout = sys_stdout

        # parse the response
        dict_out = {
            "stdout": stdout,
            "stdout_lines": stdout.splitlines(),
            "stderr": stderr,
            "stderr_lines": stderr.splitlines(),
        }

        # Patch for ansible-core 2.19+ compatibility
        try:
            profile = getattr(self._task._role, "name", "legacy")
            data = self._parse_returned_data(dict_out, profile)
        except TypeError:
            # Fallback for older versions that don't support the profile parameter
            data = self._parse_returned_data(dict_out)

        # Clean up the response like action _execute_module
        remove_internal_keys(data)

        # split stdout/stderr into lines if needed
        if "stdout" in data and "stdout_lines" not in data:
            # if the value is 'False', a default won't catch it.
            txt = data.get("stdout", None) or ""
            data["stdout_lines"] = txt.splitlines()
        if "stderr" in data and "stderr_lines" not in data:
            # if the value is 'False', a default won't catch it.
            txt = data.get("stderr", None) or ""
            data["stderr_lines"] = txt.splitlines()

        return data

    def _sanitize_contents(self, contents, filters):
        """remove lines from contents that match
        regexes specified in the `filters` list
        """
        for x in filters:
            contents = re.sub(x, "", contents)
        return contents.strip()
