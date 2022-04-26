# (c) 2022 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from functools import total_ordering


@total_ordering
class Version:
    """Simple class to compare arbitrary versions"""

    def __init__(self, version_string):
        self.components = version_string.split(".")

    def __eq__(self, other):
        other = _coerce(other)
        if not isinstance(other, Version):
            return NotImplemented

        return self.components == other.components

    def __ne__(self, other):
        other = _coerce(other)
        if not isinstance(other, Version):
            return NotImplemented

        return self.components != other.components

    def __lt__(self, other):
        other = _coerce(other)
        if not isinstance(other, Version):
            return NotImplemented

        return self.components < other.components


def _coerce(other):
    if isinstance(other, str):
        other = Version(other)
    return other
