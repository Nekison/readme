"""Provide test cases for rtdb_sync_pub.redis_monitor module.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import unittest

import redis

from rtdb_sync_pub import redis_monitor


class TestRedisMonitor(unittest.TestCase):
    """RedisMonitor test case."""

    def setUp(self):
        """Redis Monitor test case setup."""
        self.redis = redis.Redis("redis")
        self.monitor = redis_monitor.RedisMonitor()

    def test_monitor_return_iterable(self):
        """Test that monitor() method produce an iterable."""
        monitor_result = self.monitor.monitor()

        self.redis.set("foo", "bar")

        try:
            iter(monitor_result)
        except TypeError:
            self.fail("monitor() return value is not iterable")

    def test_monitor_return_iterable_of_binary_strings(self):
        """Test that monitor() method produce an iterable."""
        monitor_result = self.monitor.monitor()

        self.redis.set("foo", "bar")

        self.assertTrue(all(isinstance(el, bytes) for el in monitor_result))


if __name__ == '__main__':
    unittest.main()
