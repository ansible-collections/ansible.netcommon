"""Compatibility support for pytest-ansible with ansible-devel."""

import os


def pytest_sessionstart(session):
    """Install ansible-devel's collection finder when pytest-ansible cannot."""
    try:
        from pytest_ansible.units import HAS_COLLECTION_FINDER
    except ImportError:
        return
    if HAS_COLLECTION_FINDER:
        return

    try:
        from ansible.utils.collection_loader._collection_finder import (
            _AnsibleCollectionFinder,
        )
    except ImportError:
        try:
            from ansible.module_utils._internal._collection_loader._collection_finder import (
                _AnsibleCollectionFinder,
            )
        except ImportError:
            return

    paths = []
    for envvar in ("ANSIBLE_COLLECTIONS_PATH", "ANSIBLE_COLLECTIONS_PATHS"):
        paths.extend(
            path
            for path in os.environ.get(envvar, "").split(os.pathsep)
            if path and path not in paths
        )
    if paths:
        _AnsibleCollectionFinder(paths=paths)._install()
