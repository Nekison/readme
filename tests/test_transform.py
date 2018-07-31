"""Provide test cases for rtdb_sync_pub.transform module.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import unittest

from rtdb_sync_pub import transform


class TestPrefixKeyName(unittest.TestCase):
    """prefix_key_name function test case."""

    def test_return_iterable(self):
        """Test that prefix_key_name() function produce an iterable."""
        result = transform.prefix_key_name([], "")

        try:
            iter(result)
        except TypeError:
            self.fail("prefix_key_name() return value is not iterable")


class TestSetAgent(unittest.TestCase):
    """set_agent function test case."""

    def test_return_iterable(self):
        """Test that set_agent() function produce an iterable."""
        result = transform.set_agent([], "")

        try:
            iter(result)
        except TypeError:
            self.fail("set_agent() return value is not iterable")
