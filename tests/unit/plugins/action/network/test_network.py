# (c) 2021 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import tempfile

from ansible.errors import AnsibleError
from ansible.playbook.role import Role
from ansible.playbook.task import Task
from ansible.plugins.loader import action_loader
from ansible.template import Templar
import pytest

from ansible_collections.ansible.netcommon.tests.unit.compat.mock import (
    MagicMock,
)
from ansible_collections.ansible.netcommon.tests.unit.mock.loader import (
    DictDataLoader,
)


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


@pytest.mark.parametrize(
    "backup_path", ["", "/tmp/", "backup_file", "/tmp/backup_file"]
)
@pytest.mark.parametrize("has_role", [True, False])
def test_backup_options(plugin, backup_path, has_role):
    plugin._task.args = {}
    content = "This is the backup content"
    dirname, basename = os.path.split(backup_path)

    # This doesn't need to be conditional, but doing so tests the equivalent
    # `if backup_options:` in the action plugin itself.
    if backup_path:
        plugin._task.args["backup_options"] = {
            "dir_path": dirname,
            "filename": basename,
        }

    # Test with role_path
    if has_role:
        plugin._task._role = MagicMock(Role)
        role_path = "/var/tmp"
        plugin._task._role._role_path = role_path

    result = {"__backup__": content}
    task_vars = dict(inventory_hostname="example.com")
    plugin._handle_backup_option(result, task_vars)
    assert not result.get("failed")

    with open(result["backup_path"]) as backup_file:
        assert backup_file.read() == content

    if basename:
        # check that presented and returned backup paths match
        if dirname:
            assert os.path.samefile(backup_path, result["backup_path"])
        elif has_role:
            final_path = os.path.join(role_path, "backup", backup_path)
            assert os.path.samefile(final_path, result["backup_path"])
        else:
            final_path = os.path.join("backup", backup_path)
            assert os.path.samefile(final_path, result["backup_path"])

        # check for idempotency
        result = {"__backup__": content}
        plugin._handle_backup_option(result, task_vars)
        assert not result.get("failed")
        assert result["changed"] is False
    else:
        assert result["date"] in result["backup_path"]
        assert result["time"] in result["backup_path"]

    assert os.path.exists(result["backup_path"])
    os.remove(result["backup_path"])


def test_backup_no_content(plugin):
    result = {}
    task_vars = {}
    with pytest.raises(
        AnsibleError, match="Failed while reading configuration backup"
    ):
        plugin._handle_backup_option(result, task_vars)


def test_backup_options_error(plugin):
    result = {"__backup__": ""}
    task_vars = {}

    with tempfile.NamedTemporaryFile() as existing_file:
        plugin._task.args = {
            "backup_options": {
                "dir_path": existing_file.name,
                "filename": "backup_file",
            }
        }
        plugin._handle_backup_option(result, task_vars)

    assert result["failed"] is True
    assert result["msg"] == (
        "Could not write to destination file {0}/backup_file: [Errno 20] Not a directory: '{0}/backup_file'".format(
            existing_file.name
        )
    )
