# (c) 2023 Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function


__metaclass__ = type

import pytest

from ansible_collections.ansible.netcommon.plugins.plugin_utils.version import Version


@pytest.mark.parametrize("left", ["6.0.0", 6, 6.0])
@pytest.mark.parametrize("right", ["4.0.0", 4, 4.0])
def test_versions_different(left, right):
    assert Version(str(left)) > right


@pytest.mark.parametrize("value", ["6.0.0", 6, 6.0])
def test_versions_same(value):
    assert Version(str(value)) == value


def test_version_error():
    with pytest.raises(TypeError):
        Version("1.2.3") < [1, 2, 3]

    # with pytest.raises(TypeError):
    Version("1.2.3") == [1, 2, 3]
