"""Compatibility support for pytest-ansible with ansible-devel."""

import os


def pytest_sessionstart(session):
    """Install ansible-devel's collection finder when pytest-ansible cannot."""
    if not getattr(session.config.option, "ansible_unit_inject_only", False):
        return

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
    else:
        # pytest-ansible already installs the finder from this import path.
        return

    collection_paths = os.environ.get("ANSIBLE_COLLECTIONS_PATH") or os.environ.get(
        "ANSIBLE_COLLECTIONS_PATHS", ""
    )
    paths = [path for path in collection_paths.split(os.pathsep) if path]
    if paths:
        _AnsibleCollectionFinder(paths=paths)._install()
