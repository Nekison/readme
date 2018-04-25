"""Provide test cases for rtdb_sync_pub.filter module.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import unittest

from rtdb_sync_pub import filter


class TestFilterAllowedCommands(unittest.TestCase):
    """filter_commands function test case."""

    def test_return_iterable(self):
        """Test that monitor() method produce an iterable."""
        result = filter.filter_allowed_commands([])

        try:
            iter(result)
        except TypeError:
            self.fail("filter_allowed_commands() return value is not iterable")


class TestFilterTargetDatabase(unittest.TestCase):
    """filter_commands function test case."""

    def test_return_iterable(self):
        """Test that monitor() method produce an iterable."""
        result = filter.filter_target_database([])

        try:
            iter(result)
        except TypeError:
            self.fail("filter_target_database() return value is not iterable")


class TestCommandFilterQueue(unittest.TestCase):
    """CommandFilterQueue test case."""

    def setUp(self):
        """Command filter queue test case setup."""
        self.filter_queue = filter.CommandFilterQueue()

    def test_filter_return_iterable(self):
        """Test that filter() method produce an iterable."""
        result = self.filter_queue.filter(iter([]))

        try:
            iter(result)
        except TypeError:
            self.fail("filter() return value is not iterable")


if __name__ == '__main__':
    unittest.main()
