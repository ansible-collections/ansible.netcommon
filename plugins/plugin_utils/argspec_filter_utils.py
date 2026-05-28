#
# -*- coding: utf-8 -*-
# Copyright 2023 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
"""
Shared utilities for filter plugins that use AnsibleArgSpecValidator.

In Ansible 2.19+, filter arguments may be wrapped in lazy containers from
ansible-core (lib/ansible/_internal/_templating/_lazy_containers.py). Those
containers subclass dict/list/tuple and resolve values on iteration (e.g.
``.items()``, ``__iter__``). They implement ``__deepcopy__`` but it deepcopies
``_templar`` and ``_lazy_options``, which can fail; ansible-core's
ArgumentSpecValidator (lib/ansible/module_utils/common/arg_spec.py) uses
deepcopy in ValidationResult, so passing lazy containers can raise. Converting
filter args to native types before AnsibleArgSpecValidator avoids that. This
implementation aligns with the lazy containers: we recurse over dict/list/tuple
(so lazy subclasses are iterated and thus resolved) and build plain native
containers. ansible-core does not currently expose a public API for "lazy to
native" conversion; the only mechanism is the private ``_non_lazy_copy()`` on
lazy container instances (ansible._internal._templating._lazy_containers). We
avoid importing from ``_internal`` so collections remain compatible with
future core changes; if core adds a public API later, this helper can be
updated to use it.
"""

from __future__ import absolute_import, division, print_function


__metaclass__ = type


def convert_to_native(value):
    """Convert Ansible lazy containers and wrapped types to native Python types.

    Use this for filter plugin argument dicts before passing them to
    AnsibleArgSpecValidator. Lazy containers (see ansible-core
    ``_lazy_containers.py``) subclass dict/list/tuple and resolve on iteration;
    this function iterates and recurses so resolved values become plain dicts,
    lists, and scalars, avoiding deepcopy failures in ArgumentSpecValidator.

    Recommendation: keep this implementation and avoid importing from
    ansible._internal (e.g. _non_lazy_copy()). If ansible-core adds a public
    "lazy to native" API later, this helper can be updated to use it.
    """
    import json

    if value is None:
        return None
    if isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (list, tuple)):
        return [convert_to_native(item) for item in value]
    if isinstance(value, dict):
        return {convert_to_native(k): convert_to_native(v) for k, v in value.items()}
    # For any other type, try to convert via JSON round-trip to get native types
    try:
        return json.loads(json.dumps(value))
    except (TypeError, ValueError):
        return value
