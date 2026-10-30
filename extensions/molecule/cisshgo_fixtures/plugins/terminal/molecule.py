# SPDX-License-Identifier: GPL-3.0-or-later

"""Small terminal plugin used only by the cisshgo Molecule scenarios."""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import re

from ansible.plugins.terminal import TerminalBase


DOCUMENTATION = """
name: molecule
short_description: Generic CLI terminal for cisshgo Molecule fixtures
description:
  - Provides prompt handling for the local cisshgo test platform.
"""


class TerminalModule(TerminalBase):
    terminal_stdout_re = [
        re.compile(rb"[\r\n][a-zA-Z0-9][a-zA-Z0-9_.-]*(?:\([^\r\n]*\))?[>#]\s*$"),
    ]
    terminal_stderr_re = [
        re.compile(rb"% ?Error"),
        re.compile(rb"invalid input", re.I),
    ]
    terminal_config_prompt = re.compile(r"^.*\([^\r\n]+\)#$")

    def on_open_shell(self):
        for command in ("terminal length 0", "terminal width 511"):
            self._exec_cli_command(command)
