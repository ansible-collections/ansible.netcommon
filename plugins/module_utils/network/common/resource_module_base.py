from __future__ import absolute_import, division, print_function

__metaclass__ = type

from copy import deepcopy

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network import (
    get_resource_connection,
)


class RmbaseEngine(object):  # pylint: disable=R0902
    """ Base class for Network Resource Modules
    """

    ACTION_STATES = ["merged", "replaced", "overridden", "deleted"]

    def __init__(self, *_args, **kwargs):

        self._connection = None
        self._module = kwargs.get("module", None)
        self.state = self._module.params["state"]

        self._get_connection()

    def _get_connection(self):
        if self.state not in ["rendered", "parsed"]:
            if self._connection:
                return self._connection
            self._connection = get_resource_connection(self._module)
            return self._connection
        return None
