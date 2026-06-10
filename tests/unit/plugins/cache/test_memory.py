# -*- coding: utf-8 -*-
# Copyright 2024 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

from unittest import TestCase

from ansible_collections.ansible.netcommon.plugins.cache.memory import CacheModule


class TestMemoryCacheModule(TestCase):
    def setUp(self):
        self.cache = CacheModule()

    def test_persistent_attribute_exists(self):
        """CacheModule must expose _persistent for ansible-core >= 2.19 CachePluginAdjudicator."""
        self.assertTrue(hasattr(self.cache, "_persistent"))

    def test_persistent_is_false(self):
        """RAM-only cache must declare _persistent = False."""
        self.assertFalse(self.cache._persistent)

    def test_set_and_get(self):
        self.cache.set("host1", {"os": "eos"})
        self.assertEqual(self.cache.get("host1"), {"os": "eos"})

    def test_get_missing_key_returns_none(self):
        self.assertIsNone(self.cache.get("nonexistent"))

    def test_keys(self):
        self.cache.set("a", 1)
        self.cache.set("b", 2)
        self.assertEqual(sorted(self.cache.keys()), ["a", "b"])

    def test_flush(self):
        self.cache.set("a", 1)
        self.cache.flush()
        self.assertIsNone(self.cache.get("a"))
        self.assertEqual(list(self.cache.keys()), [])

    def test_populate_and_lookup(self):
        self.cache.populate("host1", {"os": "eos"})
        self.assertEqual(self.cache.lookup("host1"), {"os": "eos"})

    def test_invalidate(self):
        self.cache.set("a", 1)
        self.cache.set("b", 2)
        self.cache.invalidate()
        self.assertEqual(list(self.cache.keys()), [])

    def test_overwrite_existing_key(self):
        self.cache.set("key", "old")
        self.cache.set("key", "new")
        self.assertEqual(self.cache.get("key"), "new")

    def test_independent_instances(self):
        other = CacheModule()
        self.cache.set("key", "value")
        self.assertIsNone(other.get("key"))
