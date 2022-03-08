#
# (c) 2020 Red Hat Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    short_description: RAM backed, non persistent cache.
    description:
        - RAM backed cache that is not persistent.
        - Tailored for networking use case.
    version_added: 2.0.0
    author:
        - Ansible Networking Team (@ansible-network)
    name: memory
"""

from ansible.plugins import AnsiblePlugin


class CacheModule(AnsiblePlugin):
    def __init__(self, *args, **kwargs):
        super(CacheModule, self).__init__(*args, **kwargs)
        self._cache = {}

    def get(self, key):
        return self._cache.get(key)

    def set(self, key, value):
        self._cache[key] = value

    def keys(self):
        return self._cache.keys()

    def flush(self):
        self._cache = {}

    def lookup(self, key):
        return self.get(key)

    def populate(self, key, value):
        self.set(key, value)

    def invalidate(self):
        self.flush()
