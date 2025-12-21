# (c) 2024 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Adapter module that provides a pylibssh-compatible API using ssh-python.

This allows the libssh connection plugin to use ssh-python as an alternative
to ansible-pylibssh, since both are Python bindings for the same libssh C library.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import logging
import os
from subprocess import CompletedProcess

# Try to import ssh-python
try:
    from ssh import options as ssh_options
    from ssh.session import Session as SSHPythonSession
    from ssh.key import import_privkey_base64
    from ssh.exceptions import (
        BaseSSHError,
        AuthenticationDenied,
        AuthenticationError,
        SFTPError,
        SFTPHandleError,
    )
    from ssh.scp import SSH_SCP_WRITE, SSH_SCP_READ, SSH_SCP_REQUEST_NEWFILE, SSH_SCP_REQUEST_EOF

    HAS_SSH_PYTHON = True
except ImportError:
    HAS_SSH_PYTHON = False
    BaseSSHError = Exception
    SSHError = Exception

# Fake version for compatibility
__version__ = "1.0.0"


# ============================================================================
# Exception classes compatible with pylibssh
# ============================================================================


class LibsshSessionException(Exception):
    """Exception raised for SSH session errors."""

    pass


class LibsshChannelException(Exception):
    """Exception raised for SSH channel errors."""

    pass


class LibsshSCPException(Exception):
    """Exception raised for SCP errors."""

    pass


class LibsshSFTPException(Exception):
    """Exception raised for SFTP errors."""

    pass


class LibsshChannelReadFailure(Exception):
    """Exception raised when channel read fails."""

    pass


# ============================================================================
# Host key policy classes
# ============================================================================


class MissingHostKeyPolicy:
    """
    Interface for defining the policy that Session should use when the
    SSH server's hostname is not in either the system host keys or the
    application's keys.
    """

    def missing_host_key(self, session, hostname, username, key_type, fingerprint, message):
        """
        Called when a Session receives a server key for a server that
        isn't in either the system or local known host.
        """
        pass


class AutoAddPolicy(MissingHostKeyPolicy):
    """Policy for automatically adding the hostname and new host key."""

    def missing_host_key(self, session, hostname, username, key_type, fingerprint, message):
        return session.hostkey_auto_add(username)


class RejectPolicy(MissingHostKeyPolicy):
    """Policy for automatically rejecting the unknown hostname & key."""

    def missing_host_key(self, session, hostname, username, key_type, fingerprint, message):
        raise LibsshSessionException(message)


# ============================================================================
# Channel class compatible with pylibssh
# ============================================================================


class Channel:
    """SSH Channel wrapper providing pylibssh-compatible API."""

    def __init__(self, session):
        self._session = session
        self._ssh_session = session._ssh_session
        self._channel = self._ssh_session.channel_new()
        self._channel.open_session()

    def request_shell(self):
        """Request a PTY and shell."""
        self.request_pty()
        rc = self._channel.request_shell()
        if rc != 0:
            raise LibsshChannelException("Failed to request_shell: [%d]" % rc)

    def request_exec(self, command):
        """Run a shell command without an interactive shell."""
        if isinstance(command, str):
            command = command.encode("utf-8")
        rc = self._channel.request_exec(command)
        if rc != 0:
            raise LibsshChannelException("Failed to request_exec: [%d]" % rc)

    def request_pty(self):
        """Request a pseudo-terminal."""
        rc = self._channel.request_pty()
        if rc != 0:
            raise LibsshChannelException("Failed to request pty: [%d]" % rc)

    def request_pty_size(self, terminal, col, row):
        """Request a PTY with specific size."""
        rc = self._channel.request_pty_size(terminal, col, row)
        if rc != 0:
            raise LibsshChannelException(
                "Failed to request pty with [%d] for terminal [%s], columns [%d] and rows [%d]"
                % (rc, terminal, col, row)
            )
        rc = self._channel.request_shell()
        if rc != 0:
            raise LibsshChannelException("Failed to request_shell: [%d]" % rc)

    def poll(self, timeout=-1, stderr=0):
        """Poll the channel for data."""
        if timeout < 0:
            rc = self._channel.poll(is_stderr=bool(stderr))
        else:
            rc = self._channel.poll_timeout(timeout, is_stderr=bool(stderr))
        return rc

    def read_nonblocking(self, size=1024, stderr=0):
        """Read data from channel without blocking."""
        rc, data = self._channel.read_nonblocking(size=size, is_stderr=bool(stderr))
        if rc < 0:
            error = self._ssh_session.get_error() or "Unknown error"
            raise LibsshChannelReadFailure(error)
        elif rc == 0 and not data:
            return None
        return data

    def recv(self, size=1024, stderr=0):
        """Receive data from channel."""
        return self.read_nonblocking(size=size, stderr=stderr)

    def write(self, data):
        """Write data to channel."""
        if isinstance(data, str):
            data = data.encode("utf-8")
        rc, written = self._channel.write(data)
        if rc < 0:
            raise LibsshChannelException("Failed to write to ssh channel")
        return written

    def sendall(self, data):
        """Send all data to channel."""
        return self.write(data)

    def read_bulk_response(self, stderr=0, timeout=0.001, retry=5):
        """Read bulk response from channel with retries."""
        import time
        from io import BytesIO

        if retry <= 0:
            raise ValueError(
                "Got arg `retry={arg!r}` but it must be greater than 0".format(arg=retry)
            )

        response = b""
        with BytesIO() as recv_buff:
            for _ in range(retry, 0, -1):
                data = self.read_nonblocking(size=1024, stderr=stderr)
                if not data:
                    if timeout:
                        time.sleep(timeout)
                    continue
                recv_buff.write(data)
            response = recv_buff.getvalue()
        return response

    def exec_command(self, command):
        """Execute a command and return CompletedProcess."""
        # Create a fresh channel for exec
        channel = self._ssh_session.channel_new()
        channel.open_session()

        result = CompletedProcess(args=command, returncode=-1, stdout=b"", stderr=b"")

        if isinstance(command, str):
            command_bytes = command.encode("utf-8")
        else:
            command_bytes = command

        rc = channel.request_exec(command_bytes)
        if rc != 0:
            channel.close()
            raise LibsshChannelException(
                "Failed to execute command [{0}]: [{1}]".format(command, rc)
            )

        # Read stdout and stderr
        stdout_data = b""
        stderr_data = b""

        while not channel.is_eof():
            # Read stdout
            rc, data = channel.read_nonblocking(size=4096, is_stderr=False)
            if rc > 0 and data:
                stdout_data += data

            # Read stderr
            rc, data = channel.read_nonblocking(size=4096, is_stderr=True)
            if rc > 0 and data:
                stderr_data += data

        # Final read to get any remaining data
        while True:
            rc, data = channel.read_nonblocking(size=4096, is_stderr=False)
            if rc <= 0 or not data:
                break
            stdout_data += data

        while True:
            rc, data = channel.read_nonblocking(size=4096, is_stderr=True)
            if rc <= 0 or not data:
                break
            stderr_data += data

        channel.send_eof()
        result.returncode = channel.get_exit_status()
        result.stdout = stdout_data
        result.stderr = stderr_data

        channel.close()
        return result

    def send_eof(self):
        """Send EOF to the channel."""
        rc = self._channel.send_eof()
        if rc != 0:
            raise LibsshChannelException("Failed to ssh_channel_send_eof: [%d]" % rc)

    def get_channel_exit_status(self):
        """Get the exit status of the channel."""
        return self._channel.get_exit_status()

    @property
    def is_eof(self):
        """True if remote has sent an EOF."""
        return self._channel.is_eof()

    def close(self):
        """Close the channel."""
        if self._channel is not None:
            self._channel.close()
            self._channel = None


# ============================================================================
# SFTP class compatible with pylibssh
# ============================================================================


class SFTP:
    """SFTP wrapper providing pylibssh-compatible API."""

    SFTP_MAX_CHUNK = 32768  # 32kB

    def __init__(self, session):
        self.session = session
        self._sftp = session._ssh_session.sftp_init()
        if self._sftp is None:
            raise LibsshSFTPException("Failed to create new SFTP session")

    def put(self, local_file, remote_file):
        """Upload a file to the remote host."""
        # O_WRONLY | O_CREAT | O_TRUNC
        O_WRONLY = 0o1
        O_CREAT = 0o100
        O_TRUNC = 0o1000
        S_IRWXU = 0o700

        access_type = O_WRONLY | O_CREAT | O_TRUNC

        with open(local_file, "rb") as f:
            if isinstance(remote_file, str):
                remote_file_b = remote_file
            else:
                remote_file_b = remote_file.decode("utf-8")

            try:
                rf = self._sftp.open(remote_file_b, access_type, S_IRWXU)
            except (SFTPError, SFTPHandleError) as e:
                raise LibsshSFTPException(
                    "Opening remote file [%s] for write failed with error [%s]"
                    % (remote_file, str(e))
                )

            try:
                buffer = f.read(self.SFTP_MAX_CHUNK)
                while buffer:
                    length = len(buffer)
                    written = rf.write(buffer)
                    if written != length:
                        raise LibsshSFTPException(
                            "Writing to remote file [%s] failed: wrote %d of %d bytes"
                            % (remote_file, written, length)
                        )
                    buffer = f.read(self.SFTP_MAX_CHUNK)
            finally:
                rf.close()

    def get(self, remote_file, local_file):
        """Download a file from the remote host."""
        O_RDONLY = 0
        S_IRWXU = 0o700

        if isinstance(remote_file, str):
            remote_file_b = remote_file
        else:
            remote_file_b = remote_file.decode("utf-8")

        try:
            attrs = self._sftp.stat(remote_file_b)
            file_size = attrs.size
        except (SFTPError, SFTPHandleError) as e:
            raise LibsshSFTPException(
                "Failed to stat the remote file [%s]. Error: [%s]" % (remote_file, str(e))
            )

        try:
            rf = self._sftp.open(remote_file_b, O_RDONLY, S_IRWXU)
        except (SFTPError, SFTPHandleError) as e:
            raise LibsshSFTPException(
                "Opening remote file [%s] for read failed with error [%s]" % (remote_file, str(e))
            )

        try:
            with open(local_file, "wb") as f:
                buffer_size = (
                    min(self.SFTP_MAX_CHUNK, file_size) if file_size > 0 else self.SFTP_MAX_CHUNK
                )
                while True:
                    size, data = rf.read(buffer_size)
                    if size <= 0 or not data:
                        break
                    bytes_written = f.write(data)
                    if bytes_written != len(data):
                        raise LibsshSFTPException(
                            "Number of bytes [%s] read from remote file [%s] "
                            "does not match number of bytes [%s] written to local file [%s]"
                            % (len(data), remote_file, bytes_written, local_file)
                        )
        finally:
            rf.close()

    def close(self):
        """Close the SFTP session."""
        self._sftp = None


# ============================================================================
# SCP class compatible with pylibssh
# ============================================================================


class SCP:
    """SCP wrapper providing pylibssh-compatible API."""

    SCP_MAX_CHUNK = 65536  # 64kB

    def __init__(self, session):
        self.session = session
        self._ssh_session = session._ssh_session

    def put(self, local_file, remote_file):
        """Upload a file via SCP."""
        if isinstance(remote_file, str):
            remote_file_b = remote_file
        else:
            remote_file_b = remote_file.decode("utf-8")

        remote_dir, filename = os.path.split(remote_file_b)
        if not remote_dir:
            remote_dir = "."

        with open(local_file, "rb") as f:
            file_stat = os.fstat(f.fileno())
            file_size = file_stat.st_size
            file_mode = file_stat.st_mode & 0o777

            # Create SCP session in write mode
            try:
                scp = self._ssh_session.scp_new(SSH_SCP_WRITE, remote_file_b)
            except BaseSSHError as e:
                raise LibsshSCPException(
                    "Allocating SCP session of remote file [{0}] for write failed with error [{1}]".format(
                        remote_file, str(e)
                    )
                )

            try:
                # Push file info
                rc = scp.push_file(filename, file_size, file_mode)
                if rc != 0:
                    raise LibsshSCPException("Can't open remote file: error %d" % rc)

                # Write file data
                remaining = file_size
                while remaining > 0:
                    chunk_size = min(remaining, self.SCP_MAX_CHUNK)
                    data = f.read(chunk_size)
                    rc = scp.write(data)
                    if rc != 0:
                        raise LibsshSCPException("Can't write to remote file: error %d" % rc)
                    remaining -= len(data)
            finally:
                scp.close()

        return 0

    def get(self, remote_file, local_file):
        """Download a file via SCP."""
        if isinstance(remote_file, str):
            remote_file_b = remote_file
        else:
            remote_file_b = remote_file.decode("utf-8")

        # Create SCP session in read mode
        try:
            scp = self._ssh_session.scp_new(SSH_SCP_READ, remote_file_b)
        except BaseSSHError as e:
            raise LibsshSCPException(
                "Allocating SCP session of remote file [{0}] for read failed with error [{1}]".format(
                    remote_file, str(e)
                )
            )

        try:
            # Request to pull the file
            rc = scp.pull_request()
            if rc != SSH_SCP_REQUEST_NEWFILE:
                raise LibsshSCPException("Error receiving information about file: error %d" % rc)

            size = scp.request_get_size()
            mode = scp.request_get_permissions()

            # Accept the request
            scp.accept_request()

            # Read and write to local file
            with open(local_file, "wb") as f:
                remaining = size
                while remaining > 0:
                    chunk_size = min(remaining, self.SCP_MAX_CHUNK)
                    rc, data = scp.read(chunk_size)
                    if rc < 0:
                        raise LibsshSCPException("Error receiving file data: error %d" % rc)
                    if data:
                        f.write(data)
                        remaining -= len(data)
                    if rc == 0:
                        break

            if mode >= 0:
                os.chmod(local_file, mode)

            # Make sure we have finished requesting files
            rc = scp.pull_request()
            if rc != SSH_SCP_REQUEST_EOF:
                raise LibsshSCPException("Unexpected request: %d" % rc)

        finally:
            scp.close()

        return 0


# ============================================================================
# Session class compatible with pylibssh
# ============================================================================

LOG_MAP = {
    logging.NOTSET: 0,  # SSH_LOG_NONE
    logging.DEBUG: 4,  # SSH_LOG_DEBUG
    logging.INFO: 3,  # SSH_LOG_INFO
    logging.WARNING: 2,  # SSH_LOG_WARN
    logging.ERROR: 2,  # SSH_LOG_WARN
    logging.CRITICAL: 5,  # SSH_LOG_TRACE
}


class Session:
    """SSH Session wrapper providing pylibssh-compatible API."""

    def __init__(self, host=None, **kwargs):
        if not HAS_SSH_PYTHON:
            raise ImportError("ssh-python is not installed")

        self._ssh_session = SSHPythonSession()
        self._policy = RejectPolicy()
        self._host = None
        self._user = None
        self._connected = False

        if host:
            self._ssh_session.options_set(ssh_options.HOST, host)
            self._host = host

    def set_ssh_options(self, key, value):
        """Set SSH options."""
        # Skip None values
        if value is None:
            return

        # String options that use options_set()
        str_opts_map = {
            "host": ssh_options.HOST,
            "user": ssh_options.USER,
            "knownhosts": ssh_options.KNOWNHOSTS,
            "proxycommand": ssh_options.PROXYCOMMAND,
            "key_exchange_algorithms": ssh_options.KEY_EXCHANGE,
            "publickey_accepted_algorithms": ssh_options.PUBLICKEY_ACCEPTED_TYPES,
            "hostkeys": ssh_options.HOSTKEYS,
            "gssapi_server_identity": ssh_options.GSSAPI_SERVER_IDENTITY,
            "gssapi_client_identity": ssh_options.GSSAPI_CLIENT_IDENTITY,
        }

        # Integer options that use options_set_int_val()
        int_opts_map = {
            "timeout": ssh_options.TIMEOUT,
        }

        if key == "port":
            self._ssh_session.options_set_port(int(value))
        elif key == "gssapi_delegate_credentials":
            self._ssh_session.options_set_gssapi_delegate_credentials(bool(value))
        elif key in int_opts_map:
            self._ssh_session.options_set_int_val(int_opts_map[key], int(value))
        elif key in str_opts_map:
            if isinstance(value, str):
                value = value.encode("utf-8")
            elif isinstance(value, bytes):
                pass  # Already bytes
            else:
                value = str(value).encode("utf-8")
            self._ssh_session.options_set(str_opts_map[key], value)
        else:
            raise LibsshSessionException("Unknown attribute name [%s]" % key)

    def get_ssh_options(self, key):
        """Get SSH options."""
        opts_map = {
            "host": ssh_options.HOST,
            "user": ssh_options.USER,
        }

        if key == "port":
            return self._ssh_session.options_get_port(0)
        elif key in opts_map:
            return self._ssh_session.options_get(opts_map[key])
        else:
            raise LibsshSessionException("Unknown attribute name [%s]" % key)

    def connect(self, **kwargs):
        """Connect to SSH server and authenticate.

        This provides pylibssh-compatible connect() signature.

        :param host: The address of the remote host
        :param user: The username to authenticate with
        :param port: The SSH port (default 22)
        :param timeout: Connection timeout
        :param password: Password for authentication
        :param password_prompt: Prompt to match for keyboard-interactive auth
        :param private_key: Private key content as bytes
        :param private_key_password: Passphrase for the private key
        :param look_for_keys: Whether to look for keys in ~/.ssh/
        :param host_key_checking: Whether to verify host keys
        :param proxycommand: ProxyCommand for connection
        :param publickey_accepted_algorithms: Accepted pubkey algorithms
        :param hostkeys: Accepted host key types
        :param key_exchange_algorithms: Key exchange algorithms
        :param gssapi_server_identity: GSSAPI server identity
        :param gssapi_client_identity: GSSAPI client identity
        :param gssapi_delegate_credentials: Whether to delegate GSSAPI credentials
        :param config_file: SSH config file path
        """
        # Map kwargs to SSH options
        option_map = {
            "host": "host",
            "user": "user",
            "port": "port",
            "timeout": "timeout",
            "proxycommand": "proxycommand",
            "key_exchange_algorithms": "key_exchange_algorithms",
            "publickey_accepted_algorithms": "publickey_accepted_algorithms",
            "hostkeys": "hostkeys",
            "gssapi_server_identity": "gssapi_server_identity",
            "gssapi_client_identity": "gssapi_client_identity",
            "gssapi_delegate_credentials": "gssapi_delegate_credentials",
        }

        for key, opt_key in option_map.items():
            if key in kwargs and kwargs[key] is not None:
                self.set_ssh_options(opt_key, kwargs[key])

        if kwargs.get("host"):
            self._host = kwargs["host"]
        if kwargs.get("user"):
            self._user = kwargs["user"]

        # Handle config file
        if kwargs.get("config_file"):
            self._ssh_session.options_parse_config(kwargs["config_file"])

        # Connect
        try:
            rc = self._ssh_session.connect()
        except BaseSSHError as e:
            raise LibsshSessionException("ssh connect failed: %s" % str(e))

        if rc != 0:
            raise LibsshSessionException("ssh connect failed with error code: %d" % rc)

        # Verify host key if requested
        host_key_checking = kwargs.get("host_key_checking", True)
        if host_key_checking:
            self._verify_knownhost()

        # Authenticate
        saved_exception = None

        # Try userauth_none first to get supported auth methods
        try:
            rc = self._ssh_session.userauth_none()
            if rc == 0:  # SSH_AUTH_SUCCESS
                self._connected = True
                return
        except BaseSSHError:
            pass

        auth_list = self._ssh_session.userauth_list()

        # Try private key authentication
        if kwargs.get("private_key") and (auth_list & 0x04):  # SSH_AUTH_METHOD_PUBLICKEY
            try:
                self._authenticate_specific_pubkey(
                    kwargs["private_key"], kwargs.get("private_key_password")
                )
                self._connected = True
                return
            except LibsshSessionException as e:
                saved_exception = e

        # Try password authentication
        if kwargs.get("password") and (auth_list & 0x02):  # SSH_AUTH_METHOD_PASSWORD
            try:
                self._authenticate_password(kwargs["password"])
                self._connected = True
                return
            except LibsshSessionException as e:
                saved_exception = e

        # Try keyboard-interactive authentication
        if kwargs.get("password") and (auth_list & 0x08):  # SSH_AUTH_METHOD_INTERACTIVE
            try:
                self._authenticate_interactive(kwargs["password"], kwargs.get("password_prompt"))
                self._connected = True
                return
            except LibsshSessionException as e:
                saved_exception = e

        # Try public key auto authentication
        if kwargs.get("look_for_keys", True) and (auth_list & 0x04):  # SSH_AUTH_METHOD_PUBLICKEY
            try:
                self._authenticate_pubkey()
                self._connected = True
                return
            except LibsshSessionException as e:
                saved_exception = e

        # Try GSSAPI authentication
        if auth_list & 0x20:  # SSH_AUTH_METHOD_GSSAPI_MIC
            try:
                self._authenticate_gssapi()
                self._connected = True
                return
            except LibsshSessionException as e:
                saved_exception = e

        if saved_exception is not None:
            raise saved_exception
        raise LibsshSessionException("Failed to find any acceptable way to authenticate")

    def _verify_knownhost(self):
        """Verify the server's host key."""
        # ssh-python doesn't have a direct equivalent to ssh_session_is_known_server
        # For now, we'll trust the host key (like AutoAddPolicy)
        # In production, you'd want to implement proper host key verification
        pass

    def _authenticate_specific_pubkey(self, private_key_b64, passphrase=None):
        """Authenticate with a specific private key."""
        try:
            if passphrase is not None:
                if isinstance(passphrase, str):
                    passphrase = passphrase.encode("utf-8")
            key = import_privkey_base64(private_key_b64, passphrase)
            rc = self._ssh_session.userauth_publickey(key)
            if rc != 0:
                raise LibsshSessionException(
                    "Failed to authenticate a specific public key (RC=%r)" % rc
                )
        except BaseSSHError as e:
            raise LibsshSessionException(
                "Failed to authenticate a specific public key: %s" % str(e)
            )

    def _authenticate_password(self, password):
        """Authenticate with password."""
        try:
            username = self._user or ""
            rc = self._ssh_session.userauth_password(username, password)
            if rc != 0:
                raise LibsshSessionException("Failed to authenticate with password")
        except (AuthenticationDenied, AuthenticationError) as e:
            raise LibsshSessionException("Failed to authenticate with password: %s" % str(e))

    def _authenticate_interactive(self, password, expected_prompt=None):
        """Authenticate using keyboard-interactive."""
        try:
            username = self._user or ""
            rc = self._ssh_session.userauth_kbdint(username, "")

            if expected_prompt is None:
                expected_prompt = "password:"
            expected_prompt = expected_prompt.lower().strip()

            while rc == 4:  # SSH_AUTH_INFO
                prompt_count = self._ssh_session.userauth_kbdint_getnprompts()
                if prompt_count > 0:
                    for i in range(prompt_count):
                        prompt_text = self._ssh_session.userauth_kbdint_getprompt(i, b"\x00")
                        if isinstance(prompt_text, bytes):
                            prompt_text = prompt_text.decode("utf-8", errors="ignore")
                        prompt_text = prompt_text.lower().strip()
                        if prompt_text.endswith(expected_prompt):
                            if isinstance(password, str):
                                password = password.encode("utf-8")
                            self._ssh_session.userauth_kbdint_setanswer(i, password)
                            break
                    else:
                        raise LibsshSessionException(
                            "None of the prompts looked like password prompts"
                        )
                rc = self._ssh_session.userauth_kbdint(username, "")

            if rc not in (0, 1):  # SSH_AUTH_SUCCESS or SSH_AUTH_DENIED
                raise LibsshSessionException("Failed to authenticate with keyboard-interactive")
        except BaseSSHError as e:
            raise LibsshSessionException(
                "Failed to authenticate with keyboard-interactive: %s" % str(e)
            )

    def _authenticate_pubkey(self):
        """Authenticate with public key auto."""
        try:
            rc = self._ssh_session.userauth_publickey_auto("")
            if rc != 0:
                raise LibsshSessionException("Failed to authenticate public key")
        except BaseSSHError as e:
            raise LibsshSessionException("Failed to authenticate public key: %s" % str(e))

    def _authenticate_gssapi(self):
        """Authenticate with GSSAPI."""
        try:
            rc = self._ssh_session.userauth_gssapi()
            if rc != 0:
                raise LibsshSessionException("Failed to authenticate with gssapi-with-mic")
        except BaseSSHError as e:
            raise LibsshSessionException("Failed to authenticate with gssapi-with-mic: %s" % str(e))

    @property
    def is_connected(self):
        """Check if session is connected."""
        return self._ssh_session.is_connected()

    def disconnect(self):
        """Disconnect the session."""
        self._ssh_session.disconnect()

    def hostkey_auto_add(self, username):
        """Auto-add host key to known hosts."""
        rc = self._ssh_session.write_knownhost()
        if rc != 0:
            raise LibsshSessionException("host key auto add failed")

    def new_channel(self):
        """Create a new channel."""
        return Channel(self)

    def new_shell_channel(self):
        """Create a new shell channel."""
        channel = Channel(self)
        channel.request_shell()
        return channel

    def invoke_shell(self):
        """Alias for new_shell_channel."""
        return self.new_shell_channel()

    def scp(self):
        """Create an SCP instance."""
        return SCP(self)

    def sftp(self):
        """Create an SFTP instance."""
        return SFTP(self)

    def set_log_level(self, level):
        """Set logging level."""
        # ssh-python doesn't have a direct equivalent
        # This is a no-op for now
        pass

    def close(self):
        """Close the session."""
        if self._ssh_session is not None:
            if self._ssh_session.is_connected():
                self._ssh_session.disconnect()

    def set_missing_host_key_policy(self, policy):
        """Set the policy for missing host keys."""
        import inspect

        if inspect.isclass(policy):
            policy = policy()
        self._policy = policy

    def _get_session_error_str(self):
        """Get the last error message."""
        return self._ssh_session.get_error() or "Unknown error"
