# (c) 2022 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import os
import re

from ansible.errors import AnsibleError


class TestConnection:
    def __init__(self, play_context, new_stdin, *args, **kwargs):
        super(Connection, self).__init__(
            play_context, new_stdin, *args, **kwargs
        )
        # Track the send sequence for testing, increment before send
        self._send_sequence = -1

    def _connect(self):
        if self.get_option("test_parameters").get("mode") == "playback":
            return
        return super(Connection, self)._connect()

    def _send_playback(self, command):
        """Send the fixture response rather than the actual command."""

        test_parameters = self.get_option("test_parameters")

        self._send_sequence += 1

        fixture_file = os.path.join(
            test_parameters["fixture_directory"],
            "%s.json" % self._send_sequence,
        )
        if not os.path.exists(fixture_file):
            raise AnsibleError(
                "Fixture file %s does not exist." % fixture_file
            )

        with open(fixture_file, "r") as f:
            fixture = json.load(f)

        if fixture["command"] != command:
            raise AssertionError(
                "Fixture command %s does not match command %s."
                % (fixture["command"], command)
            )
        return fixture["response"]

    def _post_send(self, command, response):
        test_parameters = self.get_option("test_parameters")
        if not test_parameters:
            return response

        self._send_sequence += 1

        fixture_file = os.path.join(
            test_parameters["fixture_directory"],
            "%s.json" % self._send_sequence,
        )

        if test_parameters["mode"] == "record":
            record_response(command, response, fixture_file, test_parameters)
        elif test_parameters["mode"] == "compare":
            compare_response(command, response, fixture_file, test_parameters)


def record_response(command, response, fixture_file, test_parameters):
    os.makedirs(test_parameters["fixture_directory"], exist_ok=True)

    with open(fixture_file, "w") as f:
        json.dump(
            {"command": command.decode("utf-8"), "response": response},
            f,
        )
        f.write("\n")


def compare_response(command, response, fixture_file, test_parameters):
    with open(fixture_file, "r") as f:
        fixture = json.load(f)
    if fixture["command"] != command.decode("utf-8"):
        raise AssertionError(
            (
                "Command sent to device does not match the recorded command",
                fixture["command"],
                command.decode("utf-8"),
            ),
        )
    fixture_lines = fixture["response"].splitlines()
    response_lines = response.splitlines()
    if len(fixture_lines) != len(response_lines):
        raise AssertionError(
            (
                "Response length does not match the recorded response",
                len(fixture["response"]),
                len(response),
            ),
        )
    for idx, line in enumerate(fixture_lines):
        if line != response_lines[idx]:
            if any(
                re.match(re_exempt, line)
                for re_exempt in test_parameters["exempted"]
            ):
                continue
            raise AssertionError(
                (
                    "Response line does not match the recorded response line",
                    line,
                    response[idx],
                ),
            )
