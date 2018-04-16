"""Provide test cases for rtdb_sync_pub.redis_command_filter module.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import unittest

from rtdb_sync_pub import redis_command_filter


class TestFilterCommands(unittest.TestCase):
    """filter_commands function test case."""

    def test_return_iterable(self):
        """Test that monitor() method produce an iterable."""
        filter_commands_result = redis_command_filter.filter_commands([])

        try:
            iter(filter_commands_result)
        except TypeError:
            self.fail("filter_commands() return value is not iterable")


if __name__ == '__main__':
    unittest.main()
