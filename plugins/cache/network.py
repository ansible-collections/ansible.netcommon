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

from ansible.plugins.loader import cache_loader

CACHE_CONFIG = {"memory": {}, "jsonfile": {"_uri": "/tmp/"}}


class NetworkCache:
    def __init__(self, mode="memory"):
        self._cache = cache_loader.get(mode, **CACHE_CONFIG[mode])

    def lookup(self, key):
        out = self._cache.get(key)
        return out

    def populate(self, key, value):
        self._cache.set(key, value)

    def invalidate(self):
        self._cache.flush()

    def keys(self):
        return self._cache.keys()
