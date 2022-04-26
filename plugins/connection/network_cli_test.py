# (c) 2016 Red Hat Inc.
# (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os

from ansible_collections.ansible.netcommon.plugins.connection.network_cli import (
    DOCUMENTATION,
    Connection as RealConnection,
)
from ansible_collections.ansible.netcommon.plugins.plugin_utils.test_connection import (
    TestConnection,
    record_response,
    compare_response,
)


DOCUMENTATION += """
extends_documentation_fragment:
- ansible.netcommon.connection_persistent
- ansible.netcommon.test_parameters
"""


class Connection(TestConnection, RealConnection):
    def send(
        self,
        command,
        prompt=None,
        answer=None,
        newline=True,
        sendonly=False,
        prompt_retry_check=False,
        check_all=False,
        strip_prompt=True,
    ):
        # Check for testing
        if self.get_option("test_parameters").get("mode") == "playback":
            return self._send_playback(command)
        response = super(Connection, self).send(
            command,
            prompt=None,
            answer=None,
            newline=True,
            sendonly=False,
            prompt_retry_check=False,
            check_all=False,
            strip_prompt=True,
        )

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

        return response
