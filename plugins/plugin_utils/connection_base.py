# (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
# (c) 2015 Toshio Kuratomi <tkuratomi@ansible.com>
# (c) 2017, Peter Sprygada <psprygad@redhat.com>
# (c) 2017 Ansible Project
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import os
from difflib import SequenceMatcher, unified_diff
from io import BytesIO

from ansible import constants as C
from ansible.errors import AnsibleError
from ansible.plugins.connection import ConnectionBase
from ansible.plugins.loader import connection_loader
from ansible.utils.display import Display
from ansible.utils.path import unfrackpath

display = Display()


__all__ = ["NetworkConnectionBase"]

BUFSIZE = 65536


class NetworkConnectionBase(ConnectionBase):
    """
    A base class for network-style connections.
    """

    force_persistence = True
    # Do not use _remote_is_local in other connections
    _remote_is_local = True

    def __init__(self, play_context, new_stdin, *args, **kwargs):
        super(NetworkConnectionBase, self).__init__(
            play_context, new_stdin, *args, **kwargs
        )
        self._messages = []
        self._conn_closed = False

        self._network_os = self._play_context.network_os

        self._local = connection_loader.get("local", play_context, "/dev/null")
        self._local.set_options()

        self._sub_plugin = {}
        self._cached_variables = (None, None, None)

        # reconstruct the socket_path and set instance values accordingly
        self._ansible_playbook_pid = kwargs.get("ansible_playbook_pid")
        self._update_connection_state()

        # Track the send sequence for testing, increment before send
        self._send_sequence = -1

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            if not name.startswith("_"):
                plugin = self._sub_plugin.get("obj")
                if plugin:
                    method = getattr(plugin, name, None)
                    if method is not None:
                        return method
            raise AttributeError(
                "'%s' object has no attribute '%s'"
                % (self.__class__.__name__, name)
            )

    def exec_command(self, cmd, in_data=None, sudoable=True):
        return self._local.exec_command(cmd, in_data, sudoable)

    def queue_message(self, level, message):
        """
        Adds a message to the queue of messages waiting to be pushed back to the controller process.

        :arg level: A string which can either be the name of a method in display, or 'log'. When
            the messages are returned to task_executor, a value of log will correspond to
            ``display.display(message, log_only=True)``, while another value will call ``display.[level](message)``
        """
        self._messages.append((level, message))

    def pop_messages(self):
        messages, self._messages = self._messages, []
        return messages

    def put_file(self, in_path, out_path):
        """Transfer a file from local to remote"""
        return self._local.put_file(in_path, out_path)

    def fetch_file(self, in_path, out_path):
        """Fetch a file from remote to local"""
        return self._local.fetch_file(in_path, out_path)

    def reset(self):
        """
        Reset the connection
        """
        if self._socket_path:
            self.queue_message(
                "vvvv",
                "resetting persistent connection for socket_path %s"
                % self._socket_path,
            )
            self.close()
        self.queue_message("vvvv", "reset call on connection instance")

    def close(self):
        self._conn_closed = True
        if self._connected:
            self._connected = False

    def set_options(self, task_keys=None, var_options=None, direct=None):
        super(NetworkConnectionBase, self).set_options(
            task_keys=task_keys, var_options=var_options, direct=direct
        )
        if self.get_option("persistent_log_messages"):
            warning = (
                "Persistent connection logging is enabled for %s. This will log ALL interactions"
                % self._play_context.remote_addr
            )
            logpath = getattr(C, "DEFAULT_LOG_PATH")
            if logpath is not None:
                warning += " to %s" % logpath
            self.queue_message(
                "warning",
                "%s and WILL NOT redact sensitive configuration like passwords. USE WITH CAUTION!"
                % warning,
            )

        if (
            self._sub_plugin.get("obj")
            and self._sub_plugin.get("type") != "external"
        ):
            try:
                self._sub_plugin["obj"].set_options(
                    task_keys=task_keys, var_options=var_options, direct=direct
                )
            except AttributeError:
                pass

    def _update_connection_state(self):
        """
        Reconstruct the connection socket_path and check if it exists

        If the socket path exists then the connection is active and set
        both the _socket_path value to the path and the _connected value
        to True.  If the socket path doesn't exist, leave the socket path
        value to None and the _connected value to False
        """
        ssh = connection_loader.get("ssh", class_only=True)
        control_path = ssh._create_control_path(
            self._play_context.remote_addr,
            self._play_context.port,
            self._play_context.remote_user,
            self._play_context.connection,
            self._ansible_playbook_pid,
        )

        tmp_path = unfrackpath(C.PERSISTENT_CONTROL_PATH_DIR)
        socket_path = unfrackpath(control_path % dict(directory=tmp_path))

        if os.path.exists(socket_path):
            self._connected = True
            self._socket_path = socket_path

    def _log_messages(self, message):
        if self.get_option("persistent_log_messages"):
            self.queue_message("log", message)

    def _test_fixture(self, make_dir=False):
        """Generate the fixture file and directory if requested."""
        test_parameters = self.get_option("test_parameters")

        fixture_dir = os.path.join(
            test_parameters["fixture_directory"], self.transport
        )

        if make_dir and not os.path.exists(fixture_dir):
            os.makedirs(fixture_dir)

        fixture_file = os.path.join(
            fixture_dir,
            "%05d.json" % self._send_sequence,
        )
        return fixture_file

    def _playback_network_cli(self, command):
        """Send the fixture response rather than the actual command."""

        self._send_sequence += 1

        fixture_file = self._test_fixture()

        if not os.path.exists(fixture_file):
            raise AnsibleError(
                "Fixture file %s does not exist." % fixture_file
            )

        with open(fixture_file, "r") as f:
            fixture = json.load(f)

        if fixture["command"] != command.decode("utf-8"):
            raise AssertionError(
                "Fixture command %s does not match command %s."
                % (fixture["command"], command)
            )
        if fixture["response_type"] == "json":
            return json.dumps(fixture["response"])
        return "\n".join(fixture["response"])

    def _compare_record_network_cli(self, command, response):
        """Proxy the response to the send() method"""
        test_parameters = self.get_option("test_parameters")
        if not test_parameters:
            return response

        # Don't record the terminal commands
        if command.decode("utf-8").startswith("terminal"):
            return response

        self._send_sequence += 1

        mode_record = test_parameters["mode"] == "record"

        fixture_file = self._test_fixture(make_dir=mode_record)

        if mode_record:
            try:
                response_for_fixture = json.loads(response)
                response_type = "json"
            except json.decoder.JSONDecodeError:
                response_for_fixture = response.splitlines()
                response_type = "text"

            with open(fixture_file, "w") as f:
                json.dump(
                    {
                        "command": command.decode("utf-8"),
                        "response": response_for_fixture,
                        "response_type": response_type,
                    },
                    f,
                    indent=4,
                    sort_keys=True,
                )
                f.write("\n")
        elif test_parameters["mode"] == "compare":
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
            if fixture["response_type"] == "json":
                try:
                    response_json = json.loads(response)
                except json.decoder.JSONDecodeError:
                    raise AssertionError(
                        "Response from device is not valid JSON, but fixture is.",
                        fixture_file,
                        response,
                    )
                response_lines = json.dumps(
                    response_json,
                    indent=4,
                    sort_keys=True,
                ).splitlines()
                fixture_lines = json.dumps(
                    fixture["response"],
                    indent=4,
                    sort_keys=True,
                ).splitlines()
            else:
                response_lines = response.splitlines()
                fixture_lines = fixture["response"]

            self.compare(
                response_lines=response_lines,
                fixture_lines=fixture_lines,
                match_threshold=test_parameters["match_threshold"],
            )

    def _compare_record_httpapi(
        self, path, data, response, resp_data, **kwargs
    ):

        test_parameters = self.get_option("test_parameters")

        if not test_parameters:
            return response

        self._send_sequence += 1

        response = {
            "body": json.loads(resp_data),
            "data": json.loads(data),
            "headers": dict(response.headers),
            "path": path,
            "reason": response.reason,
            "status": response.status,
            "url": response.url,
            "send_kwargs": kwargs,
            "version": response.version,
        }

        mode_record = test_parameters["mode"] == "record"

        fixture_file = self._test_fixture(make_dir=mode_record)

        response_lines = json.dumps(
            response,
            indent=4,
            sort_keys=True,
        ).splitlines()

        if mode_record:
            with open(fixture_file, "w") as f:
                f.writelines(response_lines)
        elif test_parameters["mode"] == "compare":
            with open(fixture_file, "r") as f:
                fixture_str = f.read()

            fixture = json.loads(fixture_str)

            if fixture["path"] != path:
                raise AssertionError(
                    (
                        "Path sent to device does not match the recorded path",
                        fixture["path"],
                        path,
                    ),
                )

            fixture_lines = fixture_str.splitlines()
            self.compare(
                response_lines=response_lines,
                fixture_lines=fixture_lines,
                match_threshold=test_parameters["match_threshold"],
            )

    def _playback_httpapi(self, path):
        """Send the fixture response rather than the actual command."""

        self._send_sequence += 1

        fixture_file = self._test_fixture()

        if not os.path.exists(fixture_file):
            raise AnsibleError(
                "Fixture file %s does not exist." % fixture_file
            )

        with open(fixture_file, "r") as f:
            fixture = json.load(f)

        if fixture["path"] != path:
            raise AssertionError(
                "Fixture path does not match request path.",
                fixture["path"],
                path,
            )

        response_buffer = BytesIO()
        response_buffer.write(bytes(json.dumps(fixture["body"]), "utf-8"))
        response_buffer.seek(0)

        test_http_response = TestHTTPResponse(
            headers=fixture["headers"].items(),
            reason=fixture["reason"],
            status=fixture["status"],
            url=fixture["url"],
            version=fixture["version"],
        )

        return test_http_response, response_buffer

    def compare(self, response_lines, fixture_lines, match_threshold):
        match = SequenceMatcher(
            None,
            response_lines,
            fixture_lines,
        ).ratio()

        if match <= match_threshold:
            diff = "\n".join(
                unified_diff(
                    response_lines,
                    fixture_lines,
                    fromfile="response",
                    tofile="fixture",
                    n=0,
                    lineterm="\n",
                )
            )
            raise AssertionError(
                "Response from device does not match fixture.",
                match,
                diff,
            )

        return match


class TestHTTPResponse:
    """Class to mimic a HTTPResponse object for testing."""

    def __init__(self, headers, reason, status, url, version):
        self.headers = headers
        self.reason = reason
        self.status = status
        self.url = url
        self.version = version
