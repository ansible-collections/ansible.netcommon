#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

"""
The type5_pw plugin code
"""
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import string

from ansible.errors import AnsibleFilterError
from ansible.module_utils._text import to_text
from ansible.module_utils.six import string_types
from ansible.utils.encrypt import passlib_or_crypt, random_password


def _raise_error(msg):
    raise AnsibleFilterError(msg)


def type5_pw(password, salt=None):
    if not isinstance(password, string_types):
        _raise_error(
            "type5_pw password input should be a string, but was given a input of %s"
            % (type(password).__name__)
        )

    salt_chars = "".join((to_text(string.ascii_letters), to_text(string.digits), "./"))
    if salt is not None and not isinstance(salt, string_types):
        _raise_error(
            "type5_pw salt input should be a string, but was given a input of %s"
            % (type(salt).__name__)
        )
    elif not salt:
        salt = random_password(length=4, chars=salt_chars)
    elif not set(salt) <= set(salt_chars):
        _raise_error("type5_pw salt used inproper characters, must be one of %s" % (salt_chars))

    encrypted_password = passlib_or_crypt(password, "md5_crypt", salt=salt)

    return encrypted_password
