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
