# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2021 Red Hat Inc.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network import (
    get_resource_connection,
)


class RmEngineBase(object):  # pylint: disable=R0902
    """ Base class for Network Resource Modules
    """

    ACTION_STATES = ["merged", "replaced", "overridden", "deleted", "purged"]

    def __init__(self, *_args, **kwargs):

        self._connection = None
        self._module = kwargs.get("module", None)
        self.state = None
        # backward compatibility for modules, in which, module is not passed
        # to the NetworkTemplate
        if self._module:
            if "state" in self._module.params.keys():
                self.state = self._module.params["state"]

            self._get_connection()

    def _get_connection(self):
        if self.state not in ["rendered", "parsed"]:
            if self._connection:
                return self._connection
            self._connection = get_resource_connection(self._module)
            return self._connection
        return None
