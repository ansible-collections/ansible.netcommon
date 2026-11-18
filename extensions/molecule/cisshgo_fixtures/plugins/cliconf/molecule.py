# SPDX-License-Identifier: GPL-3.0-or-later

"""Minimal cliconf implementation for the cisshgo Molecule test platform."""

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import json

from ansible.module_utils.common.text.converters import to_text
from ansible.plugins.cliconf import CliconfBase


DOCUMENTATION = """
name: molecule
short_description: Generic cliconf for cisshgo Molecule fixtures
description:
  - Implements the small set of CLI operations exercised by netcommon Molecule scenarios.
"""


def _to_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


class Cliconf(CliconfBase):
    __rpc__ = [
        "get",
        "get_capabilities",
        "get_config",
        "edit_config",
        "get_diff",
        "run_commands",
        "restore",
    ]

    def get_device_info(self):
        return {"network_os": "molecule"}

    def get_device_operations(self):
        return {
            "supports_diff_replace": False,
            "supports_commit": False,
            "supports_rollback": False,
            "supports_defaults": False,
            "supports_onbox_diff": False,
            "supports_commit_comment": False,
            "supports_multiline_delimiter": False,
            "supports_generate_diff": True,
            "supports_replace": False,
            "supports_config_replace": False,
            "supports_diff_match": True,
            "supports_diff_ignore_lines": True,
        }

    def get_option_values(self):
        return {"diff_match": ["line"], "diff_replace": ["line"]}

    def get_config(self, source="running", flags=None, format=None):
        command = "show running-config"
        if flags:
            command = "{0} {1}".format(command, " ".join(_to_list(flags)))
        return self.send_command(command)

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
            raise ValueError("a command is required")
        return self.send_command(
            command=command,
            prompt=prompt,
            answer=answer,
            sendonly=sendonly,
            newline=newline,
            check_all=check_all,
        )

    def get_capabilities(self):
        result = {
            "rpc": self.__rpc__,
            "device_info": self.get_device_info(),
            "network_api": "cliconf",
            "device_operations": self.get_device_operations(),
        }
        result.update(self.get_option_values())
        return json.dumps(result)

    def get_diff(
        self,
        candidate=None,
        running=None,
        diff_match="line",
        diff_ignore_lines=None,
        path=None,
        diff_replace="line",
    ):
        if candidate is None:
            raise ValueError("candidate configuration is required")

        running_text = to_text(running or "", errors="surrogate_or_strict")
        running_lines = [line.strip().lower() for line in running_text.splitlines()]
        running_text_lower = "\n".join(running_lines)
        candidate_lines = _to_list(candidate)
        if len(candidate_lines) == 1 and isinstance(candidate_lines[0], str):
            candidate_lines = candidate_lines[0].strip("\n").splitlines()
        changes = []
        context_exists = True

        for raw_line in candidate_lines:
            line = to_text(raw_line, errors="surrogate_or_strict").strip()
            if not line:
                continue
            normalized = line.lower()
            if line.startswith("no "):
                target = line[3:].strip().lower()
                if target in running_text_lower:
                    changes.append(line)
                continue
            if raw_line[:1].isspace():
                if not context_exists or normalized not in running_lines:
                    changes.append(line)
                continue
            context_exists = normalized in running_lines
            if not context_exists:
                changes.append(line)

        return {"config_diff": "\n".join(changes)}

    def run_commands(self, commands=None, check_rc=True):
        if commands is None:
            raise ValueError("commands are required")
        responses = []
        for command in _to_list(commands):
            if isinstance(command, dict):
                responses.append(self.send_command(**command))
            else:
                responses.append(self.send_command(command=command))
        return responses

    def edit_config(self, candidate=None, commit=True, replace=None, diff=False, comment=None):
        operations = self.get_device_operations()
        self.check_edit_config_capability(
            operations,
            candidate=candidate,
            commit=commit,
            replace=replace,
            comment=comment,
        )
        if replace:
            raise ValueError("The cisshgo Molecule platform does not implement config replacement")

        responses = []
        self.send_command("configure terminal")
        for command in _to_list(candidate):
            responses.append(self.send_command(command))
        self.send_command("end")
        return {"request": _to_list(candidate), "response": responses}

    def restore(self, filename=None, path=""):
        if not filename:
            raise ValueError("'filename' is required for restore")
        return self.send_command("configure replace {0}{1} best-effort".format(path, filename))
