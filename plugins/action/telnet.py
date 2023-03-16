# (c) 2017, Ansible Project
#
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import telnetlib
from time import sleep

from ansible.module_utils._text import to_bytes, to_text
from ansible.module_utils.six import text_type
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display

display = Display()


class ActionModule(ActionBase):
    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        if self._task.environment and any(self._task.environment):
            self._display.warning(
                "The telnet task does not support the environment keyword"
            )

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        if self._play_context.check_mode:
            # in --check mode, always skip this module execution
            result["skipped"] = True
            result["msg"] = "The telnet task does not support check mode"
        else:
            result["changed"] = True
            result["failed"] = False

            host = to_text(
                self._task.args.get("host", self._play_context.remote_addr)
            )
            user = to_text(
                self._task.args.get("user", self._play_context.remote_user)
            )
            password = to_text(
                self._task.args.get("password", self._play_context.password)
            )

            # FIXME, default to play_context?
            port = int(self._task.args.get("port", 23))
            timeout = int(self._task.args.get("timeout", 120))
            pause = int(self._task.args.get("pause", 1))

            send_newline = self._task.args.get("send_newline", False)

            login_prompt = to_text(
                self._task.args.get("login_prompt", "login: ")
            )
            password_prompt = to_text(
                self._task.args.get("password_prompt", "Password: ")
            )
            prompts = self._task.args.get("prompts", ["\\$ "])
            commands = self._task.args.get("command") or self._task.args.get(
                "commands"
            )

            if isinstance(commands, text_type):
                commands = commands.split(",")

            if isinstance(commands, list) and commands:
                tn = telnetlib.Telnet(host, port, timeout)

                output = []
                try:
                    if send_newline:
                        tn.write(b"\n")

                    index, match, out = tn.expect(
                        [to_bytes(login_prompt)], timeout=timeout
                    )
                    if not match:
                        raise TimeoutError(login_prompt)

                    tn.write(to_bytes(user + "\n"))

                    if password:
                        index, match, out = tn.expect(
                            [to_bytes(password_prompt)], timeout=timeout
                        )
                        if not match:
                            raise TimeoutError(password_prompt)

                        tn.write(to_bytes(password + "\n"))

                    for cmd in commands:
                        display.vvvvv(">>> %s" % cmd)
                        index, match, out = tn.expect(
                            list(map(to_bytes, prompts)), timeout=timeout
                        )
                        if not match:
                            raise TimeoutError(prompts)
                        tn.write(to_bytes(cmd + "\n"))
                        display.vvvvv("<<< %s" % cmd)
                        output.append(out)
                        sleep(pause)

                    tn.write(b"exit\n")

                except EOFError as e:
                    result["failed"] = True
                    result["msg"] = "Telnet action failed: %s" % to_text(e)
                except TimeoutError as e:
                    result["failed"] = True
                    result["msg"] = (
                        "Telnet timed out trying to find prompt(s): '%s'"
                        % to_text(e)
                    )
                finally:
                    if tn:
                        tn.close()
                    result["output"] = output
            else:
                result["failed"] = True
                result["msg"] = "Telnet requires a command to execute"

        return result
