# (c) 2026 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest.mock import MagicMock, patch

import pytest

from ansible_collections.ansible.netcommon.plugins.plugin_utils.connection_base import (
    NetworkConnectionBase,
)


@pytest.fixture()
def connection():
    with patch.multiple(
        NetworkConnectionBase,
        __init__=lambda self, *a, **kw: None,
        __abstractmethods__=frozenset(),
    ):
        conn = NetworkConnectionBase.__new__(NetworkConnectionBase)
        conn.__dict__["_sub_plugin"] = {"obj": MagicMock(), "type": "cliconf"}
        return conn


class TestGetattr:
    def test_delegates_to_sub_plugin(self, connection):
        plugin = connection._sub_plugin["obj"]
        plugin.get_config = MagicMock(return_value="running-config")
        result = connection.get_config()
        assert result == "running-config"

    def test_edit_config_returns_wrapped(self, connection):
        plugin = connection._sub_plugin["obj"]
        plugin.edit_config = MagicMock(return_value="ok")
        wrapped = connection.edit_config
        assert wrapped is not plugin.edit_config
        assert callable(wrapped)

    def test_private_attr_raises(self, connection):
        with pytest.raises(AttributeError):
            connection._nonexistent_private

    def test_missing_attr_raises(self, connection):
        plugin = connection._sub_plugin["obj"]
        plugin.no_such_method = None
        delattr(plugin, "no_such_method")
        with pytest.raises(AttributeError, match="has no attribute 'no_such_method'"):
            connection.no_such_method

    def test_no_plugin_raises(self, connection):
        connection.__dict__["_sub_plugin"] = {}
        with pytest.raises(AttributeError):
            connection.get_config


class TestWrapEditConfig:
    def test_success_returns_result(self, connection):
        plugin = connection._sub_plugin["obj"]
        plugin.edit_config = MagicMock(return_value={"diff": "+"})
        result = connection.edit_config(candidate=["hostname R1"])
        assert result == {"diff": "+"}
        plugin.edit_config.assert_called_once_with(candidate=["hostname R1"])

    def test_exception_calls_set_cli_prompt_context(self, connection):
        plugin = connection._sub_plugin["obj"]
        plugin.edit_config = MagicMock(side_effect=RuntimeError("config failed"))
        plugin.set_cli_prompt_context = MagicMock()

        with pytest.raises(RuntimeError, match="config failed"):
            connection.edit_config()

        plugin.set_cli_prompt_context.assert_called_once()

    def test_exception_reraises_original(self, connection):
        plugin = connection._sub_plugin["obj"]
        error = ValueError("bad config")
        plugin.edit_config = MagicMock(side_effect=error)
        plugin.set_cli_prompt_context = MagicMock()

        with pytest.raises(ValueError, match="bad config"):
            connection.edit_config()

    def test_exception_without_set_cli_prompt_context(self, connection):
        plugin = connection._sub_plugin["obj"]
        plugin.edit_config = MagicMock(side_effect=RuntimeError("fail"))
        del plugin.set_cli_prompt_context

        with pytest.raises(RuntimeError, match="fail"):
            connection.edit_config()

    def test_set_cli_prompt_context_error_suppressed(self, connection):
        plugin = connection._sub_plugin["obj"]
        plugin.edit_config = MagicMock(side_effect=RuntimeError("config error"))
        plugin.set_cli_prompt_context = MagicMock(side_effect=Exception("prompt context error"))

        with pytest.raises(RuntimeError, match="config error"):
            connection.edit_config()

    def test_no_plugin_skips_prompt_reset(self, connection):
        plugin = connection._sub_plugin["obj"]
        original_edit = MagicMock(side_effect=RuntimeError("fail"))
        wrapped = connection._wrap_edit_config(original_edit)
        connection.__dict__["_sub_plugin"] = {"obj": None}

        with pytest.raises(RuntimeError, match="fail"):
            wrapped()

    def test_passes_args_and_kwargs(self, connection):
        plugin = connection._sub_plugin["obj"]
        plugin.edit_config = MagicMock(return_value="ok")
        connection.edit_config("arg1", key="val")
        plugin.edit_config.assert_called_once_with("arg1", key="val")
