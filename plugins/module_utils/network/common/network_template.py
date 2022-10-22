# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2020 Nilashish Chakraborty, <nchakrab@redhat.com>
#
# Simplified BSD License (see LICENSES/BSD-2-Clause.txt or https://opensource.org/licenses/BSD-2-Clause)
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# moved actual class in `rm_base.network_template`
# this is kept here for backwards compatibility
# TODO: Remove after 2023-01-01
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.rm_base.network_template import (  # noqa: F401
    NetworkTemplate,
)
