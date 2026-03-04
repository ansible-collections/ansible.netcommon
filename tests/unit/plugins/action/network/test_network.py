# (c) 2021 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import tempfile

from unittest.mock import MagicMock

import pytest

from ansible.errors import AnsibleError
from ansible.playbook.role import Role
from ansible.playbook.task import Task
from ansible.plugins.loader import action_loader
from ansible.template import Templar

from ansible_collections.ansible.netcommon.tests.unit.mock.loader import DictDataLoader


@pytest.fixture
def plugin():
    task = MagicMock(Task)
    task.action = "network"
    task._role = None
    connection = MagicMock()
    play_context = MagicMock()
    play_context.check_mode = False
    fake_loader = DictDataLoader({})
    templar = Templar(loader=fake_loader)

    plugin = action_loader.get(
        "ansible.netcommon.network",
        task=task,
        connection=connection,
        play_context=play_context,
        loader=fake_loader,
        templar=templar,
        shared_loader_obj=None,
    )
    return plugin


# If you think this looks weird, you are correct! These two params are not
# correlated in any way, and there would normally be no reason to combine the
# two. However: when running in a container, writing to the playbook directory
# fails, but succeeds otherwise.
# By always making sure we are writing to somewhere in /tmp when we write the
# file, the test will pass in both containerized and non-containerized
# environments, and by using role_path to do it, we still manage to test all of
# the branches in the method.
# TODO: At some point, writing to the playbook dir should start working in a
# container. At that point, we should be able to disentangle these params and
# remove this comment.
@pytest.mark.parametrize("backup_dir,role_path", [("", "/tmp"), ("/tmp", "")])
@pytest.mark.parametrize("backup_file", ["", "backup_file"])
def test_backup_options(plugin, backup_dir, backup_file, role_path):
    plugin._task.args = {}
    content = "This is the backup content"

    # This doesn't need to be conditional, but doing so tests the equivalent
    # `if backup_options:` in the action plugin itself.
    backup_options = None
    if backup_dir or backup_file:
        backup_options = {
            "dir_path": backup_dir,
            "filename": backup_file,
        }

    # Test with role_path
    if role_path:
        plugin._task._role = MagicMock(Role)
        plugin._task._role._role_path = role_path

    result = {"__backup__": content}
    task_vars = dict(inventory_hostname="example.com")

    try:
        # result is updated in place, nothing is returned
        plugin._handle_backup_option(result, task_vars, backup_options)
        assert not result.get("failed")

        with open(result["backup_path"]) as backup_file_obj:
            assert backup_file_obj.read() == content

        if backup_dir:
            backup_path = backup_dir
        elif role_path:
            backup_path = os.path.join(role_path, "backup")
        else:
            backup_path = "backup"

        if backup_file:
            backup_path = os.path.join(backup_path, backup_file)
        else:
            backup_path = os.path.join(
                backup_path,
                "example.com_config.{0}@{1}".format(result["date"], result["time"]),
            )

        # check that expected and returned backup paths match
        assert os.path.samefile(backup_path, result["backup_path"])

        if backup_file:
            # check for idempotency
            result = {"__backup__": content}
            plugin._handle_backup_option(result, task_vars, backup_options)
            assert not result.get("failed")
            assert result["changed"] is False

    finally:
        if os.path.exists(result["backup_path"]):
            os.remove(result["backup_path"])


def test_backup_no_content(plugin):
    result = {}
    task_vars = {}
    with pytest.raises(AnsibleError, match="Failed while reading configuration backup"):
        plugin._handle_backup_option(result, task_vars, backup_options=None)


def test_backup_options_error(plugin):
    result = {"__backup__": ""}
    task_vars = {}

    with tempfile.NamedTemporaryFile() as existing_file:
        backup_options = {
            "dir_path": existing_file.name,
            "filename": "backup_file",
        }
        plugin._handle_backup_option(result, task_vars, backup_options)

    assert result["failed"] is True
    assert result["msg"] == (
        "Could not write to destination file {0}/backup_file: [Errno 20] Not a directory: '{0}/backup_file'".format(
            existing_file.name
        )
    )


def test_src_option_absolute_path(plugin, tmp_path):
    """Test _handle_src_option with absolute path"""
    src_file = tmp_path / "config.txt"
    src_file.write_text("hostname router1")

    # Mock templar to return data as-is
    plugin._templar.template = lambda data: data

    plugin._task.args = {"src": str(src_file)}
    plugin._handle_src_option()

    assert plugin._task.args["src"] == "hostname router1"
    assert os.path.dirname(str(src_file)) in plugin._templar.environment.loader.searchpath


def test_src_option_relative_path_in_templates(plugin, tmp_path, monkeypatch):
    """Test _handle_src_option with relative path in templates directory"""
    working_dir = tmp_path / "playbook"
    templates_dir = working_dir / "templates"
    templates_dir.mkdir(parents=True)
    src_file = templates_dir / "config.j2"
    src_file.write_text("hostname router1")

    monkeypatch.setattr(plugin._loader, "get_basedir", lambda: str(working_dir))

    def mock_path_dwim_relative(path, *args):
        # Handle both 2-arg (path, filename) and 3-arg (path, dirname, filename) calls
        if len(args) == 1:
            # 2-arg call: path_dwim_relative(path, filename)
            filename = args[0]
            return str(working_dir / filename)
        elif len(args) == 2:
            # 3-arg call: path_dwim_relative(path, dirname, filename)
            dirname, filename = args
            if dirname == "templates":
                return str(templates_dir / filename)
            return None
        return None

    monkeypatch.setattr(plugin._loader, "path_dwim_relative", mock_path_dwim_relative)
    # Mock templar to return data as-is
    plugin._templar.template = lambda data: data

    plugin._task.args = {"src": "config.j2"}
    plugin._handle_src_option()

    assert plugin._task.args["src"] == "hostname router1"
    assert str(templates_dir) in plugin._templar.environment.loader.searchpath


def test_src_option_relative_path_in_working_dir(plugin, tmp_path, monkeypatch):
    """Test _handle_src_option with relative path in working directory"""
    working_dir = tmp_path / "playbook"
    working_dir.mkdir(parents=True)
    src_file = working_dir / "config.txt"
    src_file.write_text("hostname router1")

    monkeypatch.setattr(plugin._loader, "get_basedir", lambda: str(working_dir))

    def mock_path_dwim_relative(path, *args):
        # Handle both 2-arg (path, filename) and 3-arg (path, dirname, filename) calls
        if len(args) == 1:
            # 2-arg call: path_dwim_relative(path, filename)
            filename = args[0]
            return str(working_dir / filename)
        elif len(args) == 2:
            # 3-arg call: path_dwim_relative(path, dirname, filename)
            dirname, filename = args
            if dirname == "":
                return str(working_dir / filename)
            return None
        return None

    monkeypatch.setattr(plugin._loader, "path_dwim_relative", mock_path_dwim_relative)
    # Mock templar to return data as-is
    plugin._templar.template = lambda data: data

    plugin._task.args = {"src": "config.txt"}
    plugin._handle_src_option()

    assert plugin._task.args["src"] == "hostname router1"
    assert str(working_dir) in plugin._templar.environment.loader.searchpath


def test_src_option_with_role_path(plugin, tmp_path, monkeypatch):
    """Test _handle_src_option with role path"""
    role_path = tmp_path / "roles" / "test_role"
    role_path.mkdir(parents=True)
    src_file = role_path / "config.j2"
    src_file.write_text("hostname router1")

    plugin._task._role = MagicMock(Role)
    plugin._task._role._role_path = str(role_path)

    monkeypatch.setattr(plugin._loader, "get_basedir", lambda: str(tmp_path))

    def mock_path_dwim_relative(path, *args):
        # Handle both 2-arg (path, filename) and 3-arg (path, dirname, filename) calls
        if len(args) == 1:
            # 2-arg call: path_dwim_relative(path, filename)
            filename = args[0]
            return str(role_path / filename)
        elif len(args) == 2:
            # 3-arg call: path_dwim_relative(path, dirname, filename)
            dirname, filename = args
            if dirname == "templates":
                # Return None so it falls through to 2-arg call
                return None
            return str(role_path / filename)
        return None

    monkeypatch.setattr(plugin._loader, "path_dwim_relative", mock_path_dwim_relative)
    # Mock templar to return data as-is
    plugin._templar.template = lambda data: data

    plugin._task.args = {"src": "config.j2"}
    plugin._handle_src_option()

    assert str(role_path) in plugin._templar.environment.loader.searchpath
    assert plugin._templar.environment.loader.searchpath[0] == str(role_path)
    assert plugin._templar.environment.loader.searchpath[1] == str(role_path)


def test_src_option_file_not_found(plugin, tmp_path, monkeypatch):
    """Test _handle_src_option raises error when file not found"""
    working_dir = tmp_path / "playbook"
    working_dir.mkdir(parents=True)

    monkeypatch.setattr(plugin._loader, "get_basedir", lambda: str(working_dir))

    def mock_path_dwim_relative(path, *args):
        # Handle both 2-arg (path, filename) and 3-arg (path, dirname, filename) calls
        if len(args) == 1:
            # 2-arg call: path_dwim_relative(path, filename)
            filename = args[0]
            return str(working_dir / "nonexistent.txt")
        elif len(args) == 2:
            # 3-arg call: path_dwim_relative(path, dirname, filename)
            dirname, filename = args
            return str(working_dir / "nonexistent.txt")
        return None

    monkeypatch.setattr(plugin._loader, "path_dwim_relative", mock_path_dwim_relative)

    plugin._task.args = {"src": "nonexistent.txt"}

    with pytest.raises(AnsibleError, match="path specified in src not found"):
        plugin._handle_src_option()


def test_src_option_io_error(plugin, tmp_path, monkeypatch):
    """Test _handle_src_option handles IO errors when reading file"""
    src_file = tmp_path / "config.txt"
    src_file.write_text("hostname router1")

    plugin._task.args = {"src": str(src_file)}

    # Mock open to raise IOError
    def mock_open(*args, **kwargs):
        raise IOError(13, "Permission denied")

    monkeypatch.setattr("builtins.open", mock_open)

    with pytest.raises(AnsibleError, match="unable to load src file"):
        plugin._handle_src_option()


def test_src_option_template_processing(plugin, tmp_path):
    """Test _handle_src_option processes Jinja2 templates

    NOTE: This test will fail when template processing is removed (deprecated as of 2028-01-01).
    The functionality of processing Jinja2 templates directly via the `src` option is deprecated
    in favor of using `ansible.builtin.template`. When the deprecation is removed, this test
    should be updated or removed to reflect that templates are no longer processed.
    """
    src_file = tmp_path / "config.j2"
    src_file.write_text("hostname {{ inventory_hostname }}")

    plugin._task.args = {"src": str(src_file)}

    # Mock templar to return processed template
    def mock_template(data):
        return data.replace("{{ inventory_hostname }}", "router1")

    plugin._templar.template = mock_template

    plugin._handle_src_option()

    assert plugin._task.args["src"] == "hostname router1"


def test_src_option_searchpath_order(plugin, tmp_path, monkeypatch):
    """Test _handle_src_option sets correct searchpath order"""
    working_dir = tmp_path / "playbook"
    role_path = tmp_path / "roles" / "test_role"
    src_file = role_path / "config.j2"
    src_file.parent.mkdir(parents=True)
    src_file.write_text("hostname router1")

    plugin._task._role = MagicMock(Role)
    plugin._task._role._role_path = str(role_path)

    monkeypatch.setattr(plugin._loader, "get_basedir", lambda: str(working_dir))

    def mock_path_dwim_relative(path, *args):
        # Handle both 2-arg (path, filename) and 3-arg (path, dirname, filename) calls
        if len(args) == 1:
            # 2-arg call: path_dwim_relative(path, filename)
            return str(src_file)
        elif len(args) == 2:
            # 3-arg call: path_dwim_relative(path, dirname, filename)
            return str(src_file)
        return None

    monkeypatch.setattr(plugin._loader, "path_dwim_relative", mock_path_dwim_relative)
    # Mock templar to return data as-is
    plugin._templar.template = lambda data: data

    plugin._task.args = {"src": "config.j2"}
    plugin._handle_src_option()

    searchpath = plugin._templar.environment.loader.searchpath
    # Should be: [working_path, role_path, dirname(source)]
    assert searchpath[0] == str(role_path)  # working_path when role exists
    assert searchpath[1] == str(role_path)  # self_role_path
    assert searchpath[-1] == str(role_path)  # dirname(source)


def test_src_option_without_role(plugin, tmp_path, monkeypatch):
    """Test _handle_src_option without role path"""
    working_dir = tmp_path / "playbook"
    working_dir.mkdir(parents=True)
    src_file = working_dir / "config.j2"
    src_file.write_text("hostname router1")

    plugin._task._role = None

    monkeypatch.setattr(plugin._loader, "get_basedir", lambda: str(working_dir))

    def mock_path_dwim_relative(path, *args):
        # Handle both 2-arg (path, filename) and 3-arg (path, dirname, filename) calls
        if len(args) == 1:
            # 2-arg call: path_dwim_relative(path, filename)
            return str(src_file)
        elif len(args) == 2:
            # 3-arg call: path_dwim_relative(path, dirname, filename)
            return str(src_file)
        return None

    monkeypatch.setattr(plugin._loader, "path_dwim_relative", mock_path_dwim_relative)
    # Mock templar to return data as-is
    plugin._templar.template = lambda data: data

    plugin._task.args = {"src": "config.j2"}
    plugin._handle_src_option()

    searchpath = plugin._templar.environment.loader.searchpath
    # Without role, searchpath should be: [working_path, dirname(source)]
    assert searchpath[0] == str(working_dir)
    assert searchpath[-1] == str(working_dir)


def test_get_network_os_from_task_args(plugin):
    """Test _get_network_os gets network_os from task args"""
    plugin._task.args = {"network_os": "ios"}
    task_vars = {}
    network_os = plugin._get_network_os(task_vars)
    assert network_os == "ios"


def test_get_network_os_from_play_context(plugin):
    """Test _get_network_os gets network_os from play context"""
    plugin._task.args = {}
    plugin._play_context.network_os = "eos"
    task_vars = {}
    network_os = plugin._get_network_os(task_vars)
    assert network_os == "eos"


def test_get_network_os_from_facts(plugin):
    """Test _get_network_os gets network_os from ansible_facts"""
    plugin._task.args = {}
    plugin._play_context.network_os = None
    task_vars = {"ansible_facts": {"network_os": "nxos"}}
    network_os = plugin._get_network_os(task_vars)
    assert network_os == "nxos"


def test_get_network_os_not_found(plugin):
    """Test _get_network_os raises error when network_os not found"""
    plugin._task.args = {}
    plugin._play_context.network_os = None
    task_vars = {}
    with pytest.raises(AnsibleError, match="ansible_network_os must be specified"):
        plugin._get_network_os(task_vars)


def test_get_network_os_prefers_task_args(plugin):
    """Test _get_network_os prefers task args over other sources"""
    plugin._task.args = {"network_os": "ios"}
    plugin._play_context.network_os = "eos"
    task_vars = {"ansible_facts": {"network_os": "nxos"}}
    network_os = plugin._get_network_os(task_vars)
    assert network_os == "ios"


def test_check_dexec_eligibility_enabled(plugin):
    """Test _check_dexec_eligibility when dexec is enabled"""
    plugin.get_connection_option = MagicMock(return_value=True)
    plugin._task.async_val = None
    result = plugin._check_dexec_eligibility("test_host")
    assert result is True


def test_check_dexec_eligibility_disabled(plugin):
    """Test _check_dexec_eligibility when dexec is disabled"""
    plugin.get_connection_option = MagicMock(return_value=False)
    result = plugin._check_dexec_eligibility("test_host")
    assert result is False


def test_check_dexec_eligibility_disabled_for_async(plugin):
    """Test _check_dexec_eligibility is disabled for async tasks"""
    plugin.get_connection_option = MagicMock(return_value=True)
    plugin._task.async_val = 10  # async value set
    result = plugin._check_dexec_eligibility("test_host")
    assert result is False


def test_sanitize_contents_no_filters(plugin):
    """Test _sanitize_contents with no filters"""
    content = "line1\nline2\nline3"
    result = plugin._sanitize_contents(content, [])
    assert result == "line1\nline2\nline3"


def test_sanitize_contents_with_filters(plugin):
    """Test _sanitize_contents with regex filters"""
    content = "line1\n! comment line\nline2\n! another comment\nline3"
    filters = [r"!.*"]
    result = plugin._sanitize_contents(content, filters)
    assert "comment" not in result
    assert "line1" in result
    assert "line2" in result
    assert "line3" in result


def test_sanitize_contents_multiple_filters(plugin):
    """Test _sanitize_contents with multiple regex filters"""
    content = "line1\n! comment\nline2\n# another comment\nline3"
    filters = [r"!.*", r"#.*"]
    result = plugin._sanitize_contents(content, filters)
    assert "comment" not in result
    assert "line1" in result
    assert "line2" in result
    assert "line3" in result


def test_sanitize_contents_strips_whitespace(plugin):
    """Test _sanitize_contents strips leading/trailing whitespace"""
    content = "  line1\nline2  \n  "
    filters = []
    result = plugin._sanitize_contents(content, filters)
    assert result == "line1\nline2"


def test_backup_option_with_non_config_regexes(plugin, tmp_path):
    """Test _handle_backup_option with non_config_lines regexes"""
    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()
    src_file = backup_dir / "backup_file"
    src_file.write_text("config line\n! comment line\nanother config")

    plugin._connection.cliconf = MagicMock()
    plugin._connection.cliconf.get_option = MagicMock(return_value=[r"!.*"])

    result = {"__backup__": "config line\n! comment line\nanother config"}
    task_vars = {"inventory_hostname": "test_host"}

    try:
        plugin._handle_backup_option(
            result, task_vars, {"dir_path": str(backup_dir), "filename": "backup_file"}
        )
        assert not result.get("failed")

        with open(result["backup_path"]) as f:
            content = f.read()
            assert "comment" not in content
            assert "config line" in content
            assert "another config" in content
    finally:
        if os.path.exists(result["backup_path"]):
            os.remove(result["backup_path"])


def test_backup_option_non_config_regexes_attribute_error(plugin, tmp_path):
    """Test _handle_backup_option handles AttributeError when getting non_config_lines"""
    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()

    plugin._connection.cliconf = MagicMock()
    plugin._connection.cliconf.get_option = MagicMock(side_effect=AttributeError("No attribute"))

    result = {"__backup__": "config content"}
    task_vars = {"inventory_hostname": "test_host"}

    try:
        plugin._handle_backup_option(
            result, task_vars, {"dir_path": str(backup_dir), "filename": "backup_file"}
        )
        assert not result.get("failed")
    finally:
        if os.path.exists(result["backup_path"]):
            os.remove(result["backup_path"])


def test_backup_option_non_config_regexes_key_error(plugin, tmp_path):
    """Test _handle_backup_option handles KeyError when getting non_config_lines"""
    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()

    plugin._connection.cliconf = MagicMock()
    plugin._connection.cliconf.get_option = MagicMock(side_effect=KeyError("key"))

    result = {"__backup__": "config content"}
    task_vars = {"inventory_hostname": "test_host"}

    try:
        plugin._handle_backup_option(
            result, task_vars, {"dir_path": str(backup_dir), "filename": "backup_file"}
        )
        assert not result.get("failed")
    finally:
        if os.path.exists(result["backup_path"]):
            os.remove(result["backup_path"])


def test_backup_option_checksum_idempotency(plugin, tmp_path):
    """Test _handle_backup_option doesn't overwrite if checksum matches"""
    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()
    backup_file = backup_dir / "backup_file"
    content = "config content"
    backup_file.write_text(content)

    result = {"__backup__": content}
    task_vars = {"inventory_hostname": "test_host"}

    plugin._handle_backup_option(
        result, task_vars, {"dir_path": str(backup_dir), "filename": "backup_file"}
    )
    assert not result.get("failed")
    assert result["changed"] is False

    # Verify file content unchanged
    with open(backup_file) as f:
        assert f.read() == content


def test_backup_option_filename_and_shortname(plugin, tmp_path):
    """Test _handle_backup_option sets filename and shortname when not provided"""
    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()

    result = {"__backup__": "config content"}
    task_vars = {"inventory_hostname": "test_host"}

    try:
        plugin._handle_backup_option(result, task_vars, None)
        assert not result.get("failed")
        assert "filename" in result
        assert "shortname" in result
        assert result["filename"] == os.path.basename(result["backup_path"])
        assert result["shortname"] == os.path.splitext(result["backup_path"])[0]
    finally:
        if os.path.exists(result["backup_path"]):
            os.remove(result["backup_path"])


def test_backup_option_no_filename_shortname_when_provided(plugin, tmp_path):
    """Test _handle_backup_option doesn't set filename/shortname when filename provided"""
    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()

    result = {"__backup__": "config content"}
    task_vars = {"inventory_hostname": "test_host"}

    try:
        plugin._handle_backup_option(result, task_vars, {"filename": "custom_backup"})
        assert not result.get("failed")
        # filename and shortname should not be set when custom filename provided
        assert "filename" not in result or result.get("filename") != "custom_backup"
        assert "shortname" not in result
    finally:
        if os.path.exists(result["backup_path"]):
            os.remove(result["backup_path"])


def test_get_working_path_with_role(plugin):
    """Test _get_working_path returns role path when role exists"""
    role_path = "/path/to/role"
    plugin._task._role = MagicMock(Role)
    plugin._task._role._role_path = role_path
    plugin._loader.get_basedir = MagicMock(return_value="/path/to/playbook")

    result = plugin._get_working_path()
    assert result == role_path


def test_get_working_path_without_role(plugin):
    """Test _get_working_path returns loader basedir when no role"""
    plugin._task._role = None
    basedir = "/path/to/playbook"
    plugin._loader.get_basedir = MagicMock(return_value=basedir)

    result = plugin._get_working_path()
    assert result == basedir


def test_src_option_url_scheme(plugin, tmp_path, monkeypatch):
    """Test _handle_src_option handles URL scheme"""
    src_file = tmp_path / "config.txt"
    src_file.write_text("hostname router1")

    plugin._task.args = {"src": str(src_file)}
    plugin._templar.template = lambda data: data
    monkeypatch.setattr("os.path.isabs", lambda x: False)
    plugin._loader.path_dwim_relative = MagicMock(return_value=str(src_file))

    plugin._handle_src_option()
    assert plugin._task.args["src"] == "hostname router1"


def test_exec_module_with_raw_result(plugin):
    """Test _exec_module when module has _raw_result (2.19.1+)"""
    mock_module = MagicMock()
    mock_module._raw_result = {"changed": True, "msg": "Success"}
    mock_module.main = MagicMock()

    result = plugin._exec_module(mock_module)

    assert result == {"changed": True, "msg": "Success"}
    mock_module.main.assert_called_once()


def test_exec_module_without_raw_result(plugin):
    """Test _exec_module when module doesn't have _raw_result (uses stdout/stderr)"""
    import json

    mock_module = MagicMock()
    del mock_module._raw_result  # Ensure it doesn't exist
    mock_result = {"changed": False, "msg": "No changes"}

    def mock_main():
        # Simulate module writing JSON to stdout
        print(json.dumps(mock_result))

    mock_module.main = mock_main
    plugin._parse_returned_data = MagicMock(return_value=mock_result)

    result = plugin._exec_module(mock_module)

    assert result == mock_result
    plugin._parse_returned_data.assert_called_once()


def test_exec_module_handles_system_exit(plugin):
    """Test _exec_module handles SystemExit gracefully"""
    mock_module = MagicMock()
    mock_module._raw_result = {"changed": False}
    mock_module.main = MagicMock(side_effect=SystemExit(0))

    result = plugin._exec_module(mock_module)

    assert result == {"changed": False}


def test_exec_module_generates_stdout_lines(plugin):
    """Test _exec_module generates stdout_lines when missing"""
    import json

    mock_module = MagicMock()
    del mock_module._raw_result
    mock_result = {"stdout": "line1\nline2\nline3"}

    def mock_main():
        print(json.dumps(mock_result))

    mock_module.main = mock_main
    plugin._parse_returned_data = MagicMock(return_value=mock_result)

    result = plugin._exec_module(mock_module)

    assert "stdout_lines" in result
    assert result["stdout_lines"] == ["line1", "line2", "line3"]


def test_exec_module_generates_stderr_lines(plugin):
    """Test _exec_module generates stderr_lines when missing"""
    import json

    mock_module = MagicMock()
    del mock_module._raw_result
    mock_result = {"stderr": "error1\nerror2"}

    def mock_main():
        print(json.dumps(mock_result))

    mock_module.main = mock_main
    plugin._parse_returned_data = MagicMock(return_value=mock_result)

    result = plugin._exec_module(mock_module)

    assert "stderr_lines" in result
    assert result["stderr_lines"] == ["error1", "error2"]


def test_exec_module_handles_false_stdout(plugin):
    """Test _exec_module handles False stdout value"""
    import json

    mock_module = MagicMock()
    del mock_module._raw_result
    mock_result = {"stdout": False}

    def mock_main():
        print(json.dumps(mock_result))

    mock_module.main = mock_main
    plugin._parse_returned_data = MagicMock(return_value=mock_result)

    result = plugin._exec_module(mock_module)

    assert "stdout_lines" in result
    assert result["stdout_lines"] == []


def test_run_with_dexec_eligible_and_ansiblemodule(plugin, monkeypatch):
    """Test run() when dexec is eligible and module has AnsibleModule"""
    task_vars = {"ansible_host": "test_host"}
    plugin._task.args = {}
    plugin._config_module = False

    # Mock dexec eligibility
    plugin._check_dexec_eligibility = MagicMock(return_value=True)

    # Mock module finding and loading
    mock_module = MagicMock()
    mock_module.AnsibleModule = MagicMock()
    plugin._find_load_module = MagicMock(return_value=("/path/to/module.py", mock_module))

    # Mock patching and execution
    plugin._patch_update_module = MagicMock()
    plugin._exec_module = MagicMock(return_value={"changed": True})

    # Mock super().run() to ensure it's not called
    super_run = MagicMock(return_value={"changed": False})
    monkeypatch.setattr(plugin.__class__.__bases__[0], "run", super_run)

    result = plugin.run(task_vars=task_vars)

    assert result == {"changed": True}
    plugin._check_dexec_eligibility.assert_called_once_with("test_host")
    plugin._find_load_module.assert_called_once()
    plugin._patch_update_module.assert_called_once_with(mock_module, task_vars, "test_host")
    plugin._exec_module.assert_called_once_with(mock_module)
    super_run.assert_not_called()


def test_run_with_dexec_eligible_no_ansiblemodule(plugin, monkeypatch):
    """Test run() when dexec is eligible but module doesn't have AnsibleModule"""
    task_vars = {"ansible_host": "test_host"}
    plugin._task.args = {}
    plugin._config_module = False

    # Mock dexec eligibility
    plugin._check_dexec_eligibility = MagicMock(return_value=True)

    # Mock module finding - module without AnsibleModule
    mock_module = MagicMock()
    del mock_module.AnsibleModule  # Remove AnsibleModule attribute
    plugin._find_load_module = MagicMock(return_value=("/path/to/module.py", mock_module))

    # Mock super().run() - should be called when dexec falls back
    super_run = MagicMock(return_value={"changed": False})
    monkeypatch.setattr(plugin.__class__.__bases__[0], "run", super_run)

    result = plugin.run(task_vars=task_vars)

    assert result == {"changed": False}
    plugin._find_load_module.assert_called_once()
    super_run.assert_called_once_with(task_vars=task_vars)


def test_run_with_config_module_and_src_error(plugin, monkeypatch):
    """Test run() handles AnsibleError from _handle_src_option"""
    task_vars = {"ansible_host": "test_host"}
    plugin._task.args = {"src": "nonexistent.j2"}
    plugin._config_module = True

    # Mock _handle_src_option to raise error
    plugin._handle_src_option = MagicMock(side_effect=AnsibleError("File not found"))

    result = plugin.run(task_vars=task_vars)

    assert result["failed"] is True
    assert "File not found" in result["msg"]


def test_run_with_config_module_backup(plugin, monkeypatch, tmp_path):
    """Test run() handles backup option for config modules"""
    task_vars = {"ansible_host": "test_host", "inventory_hostname": "test_host"}
    plugin._task.args = {"backup": True}
    plugin._config_module = True

    # Mock dexec not eligible to use normal run
    plugin._check_dexec_eligibility = MagicMock(return_value=False)

    # Mock super().run() to return result with backup
    backup_dir = tmp_path / "backup"
    backup_dir.mkdir()
    super_run = MagicMock(
        return_value={"changed": True, "__backup__": "config content", "failed": False}
    )
    monkeypatch.setattr(plugin.__class__.__bases__[0], "run", super_run)

    # Mock connection for backup handling
    plugin._connection = MagicMock()
    plugin._connection.cliconf = MagicMock()
    plugin._connection.cliconf.get_option = MagicMock(return_value=[])

    result = plugin.run(task_vars=task_vars)

    assert result["changed"] is True
    assert "backup_path" in result


def test_run_with_config_module_backup_failed(plugin, monkeypatch):
    """Test run() doesn't handle backup when result has failed"""
    task_vars = {"ansible_host": "test_host"}
    plugin._task.args = {"backup": True}
    plugin._config_module = True

    # Mock dexec not eligible
    plugin._check_dexec_eligibility = MagicMock(return_value=False)

    # Mock super().run() to return failed result
    super_run = MagicMock(return_value={"failed": True, "msg": "Error occurred"})
    monkeypatch.setattr(plugin.__class__.__bases__[0], "run", super_run)

    result = plugin.run(task_vars=task_vars)

    assert result["failed"] is True
    assert "backup_path" not in result


def test_find_load_module_ansible_210(plugin, monkeypatch):
    """Test _find_load_module with Ansible 2.10+ path"""
    import importlib

    mock_context = MagicMock()
    mock_context.plugin_resolved_path = "/path/to/module.py"
    mock_context.plugin_resolved_name = "ansible_collections.test.module"

    mock_loader = MagicMock()
    mock_loader.find_plugin_with_context = MagicMock(return_value=mock_context)
    plugin._shared_loader_obj = MagicMock()
    plugin._shared_loader_obj.module_loader = mock_loader

    mock_module = MagicMock()
    monkeypatch.setattr(importlib, "import_module", MagicMock(return_value=mock_module))

    filename, module = plugin._find_load_module()

    assert filename == "/path/to/module.py"
    assert module == mock_module
    mock_loader.find_plugin_with_context.assert_called_once_with(
        plugin._task.action, collection_list=plugin._task.collections
    )


def test_find_load_module_ansible_29(plugin, monkeypatch):
    """Test _find_load_module with Ansible 2.9 path"""
    import importlib

    mock_loader = MagicMock()
    mock_loader.find_plugin_with_context = MagicMock(side_effect=AttributeError("No context"))
    mock_loader.find_plugin_with_name = MagicMock(
        return_value=("module.name", "/path/to/module.py")
    )
    plugin._shared_loader_obj = MagicMock()
    plugin._shared_loader_obj.module_loader = mock_loader

    mock_module = MagicMock()
    monkeypatch.setattr(importlib, "import_module", MagicMock(return_value=mock_module))

    filename, module = plugin._find_load_module()

    assert filename == "/path/to/module.py"
    assert module == mock_module
    mock_loader.find_plugin_with_name.assert_called_once_with(
        plugin._task.action, collection_list=plugin._task.collections
    )


def test_patch_update_module(plugin):
    """Test _patch_update_module patches module with DirectExecutionModule"""
    mock_module = MagicMock()
    task_vars = {"ansible_host": "test_host"}
    host = "test_host"

    # Mock _update_module_args
    plugin._update_module_args = MagicMock()

    plugin._patch_update_module(mock_module, task_vars, host)

    assert hasattr(mock_module, "AnsibleModule")
    plugin._update_module_args.assert_called_once_with(
        plugin._task.action, plugin._task.args, task_vars
    )
