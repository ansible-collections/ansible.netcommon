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
