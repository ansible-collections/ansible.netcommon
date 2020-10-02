# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


"""
The index_of plugin common code
"""
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from ansible.module_utils.common.collections import is_sequence
from ansible.module_utils.six import string_types, integer_types
from ansible.module_utils._text import to_native

# Note, this file can only be used on the control node
# where ansible is installed
# limit imports to filter and lookup plugins
try:
    from ansible.template import Templar
    from ansible.errors import AnsibleError
except ImportError:
    pass


def _raise_error(msg):
    """ Raise an error message, prepend with filter name

    :param msg: The message
    :type msg: str
    :raises: AnsibleError
    """
    error = "Error when using plugin 'index_of': {msg}".format(msg=msg)
    raise AnsibleError(error)


def _list_to_and_str(lyst):
    """ Convert a list to a command delimited string
    with the last entry being an and

    :param lyst: The list to turn into a str
    :type lyst: list
    :return: The nicely formatted string
    :rtype: str
    """
    res = "{most} and {last}".format(most=", ".join(lyst[:-1]), last=lyst[-1])
    return res


def _to_well_known_type(obj):
    """ Convert an ansible internal type to a well-known type
    ie AnsibleUnicode => str

    :param obj: the obj to convert
    :type obj: unknown
    """
    return json.loads(json.dumps(obj))


def _check_reqs(obj, wantlist):
    """ Check the args passed, ensure given a list

    :param obj: The object passed to the filter plugin
    :type obj: unknown
    """
    errors = []
    if not is_sequence(obj):
        msg = "a list is required, was passed a '{type}'.".format(
            type=type(_to_well_known_type(obj)).__name__
        )
        errors.append(msg)
    if not isinstance(wantlist, bool):
        msg = "'wantlist' is required to be a bool, was passed a '{type}'.".format(
            type=type(_to_well_known_type(wantlist)).__name__
        )
        errors.append(msg)
    if errors:
        _raise_error(" ".join(errors))


def _run_test(entry, test, right):
    """ Run a test

    :param test: The test to run
    :type test: a lambda from the qual_map
    :param entry: The x for the lambda
    :type entry: str int or bool
    :param right: The y for the lamba
    :type right: str int bool or list
    :return: If the test passed
    :rtype: book
    """

    try:
        if test.startswith("!"):
            kind = "reject"
            test = test[1:]
            if test == "=":
                test = "=="
        elif test.startswith('not '):
            kind = "reject"
            test = test[4:]
        else:
            kind = "select"

        if not isinstance(right, list) and test == "in":
            right = [right]

        if right is None:
            template_data = "{{{{ [entry]|{kind}(test)|list }}}}".format(
                kind=kind
            )
        else:
            template_data = "{{{{ [entry]|{kind}(test, right)|list }}}}".format(
                kind=kind
            )

        vars = {"entry": entry, "test": test, "right": right}
        templar = Templar(loader=None, variables=vars)
        ret = templar.template(template_data)
        if ret:
            return True
        return False

    except Exception as exc:
        msg = (
            "Error encountered when testing value "
            "'{entry}' (type={entry_type}) against "
            "'{right}' (type={right_type}) with '{test}'. "
            "Error was: {error}."
        ).format(
            entry=entry,
            entry_type=type(_to_well_known_type(entry)).__name__,
            right=right,
            right_type=type(_to_well_known_type(entry)).__name__,
            test=test,
            error=to_native(exc),
        )
        _raise_error(msg)


def index_of(
    data, test, value=None, key=None, wantlist=False, fail_on_missing=False
):  # *args, **kwargs):
    """ Find the index or indices of entries in list of objects"

    :param data: The data passed in (data|index_of(...))
    :type data: unknown
    :param test: the test to use
    :type test: jinj2 test
    :param value: The value to use for the test
    :type value: unknown
    :param key: The key to use when a list of dicts is passed
    :type key: valid key type
    :param want_list: always return a list, even if 1 index
    :type want_list: bool
    :param fail_on_missing: Should we fail if key not found?
    :type fail_on_missing: bool
    """
    _check_reqs(data, wantlist)
    res = list()
    if key is None:
        for idx, entry in enumerate(data):
            result = _run_test(entry, test, value)
            if result:
                res.append(idx)

    elif isinstance(key, (string_types, integer_types, bool)):

        if not all(isinstance(entry, dict) for entry in data):
            all_tipes = [
                type(_to_well_known_type(entry)).__name__ for entry in data
            ]
            msg = (
                "When a key name is provided, all list entries are required to "
                "be dictionaries, got {str_tipes}"
            ).format(str_tipes=_list_to_and_str(all_tipes))
            _raise_error(msg)
        errors = []
        for idx, dyct in enumerate(data):
            if key in dyct:
                entry = dyct.get(key)
                result = _run_test(entry, test, value)
                if result:
                    res.append(idx)
            elif fail_on_missing:
                msg = (
                    "'{key}' was not found in '{dyct}' at [{index}]"
                ).format(key=key, dyct=dyct, index=idx)
                errors.append(msg)
        if errors:
            _raise_error(
                ("{errors}. fail_on_missing={fom}").format(
                    errors=_list_to_and_str(errors), fom=str(fail_on_missing)
                )
            )
    else:
        msg = "Unknown key type, key ({key}) was a {type}. ".format(
            key=key, type=type(_to_well_known_type(key)).__name__
        )
        _raise_error(msg)
    if len(res) == 1 and not wantlist:
        return res[0]
    return res
