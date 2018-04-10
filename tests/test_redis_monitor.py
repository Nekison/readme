"""Provide test cases for rtdb_sync_pub.redis_monitor module.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import itertools
import unittest

import redis

from rtdb_sync_pub import redis_monitor


class TestRedisMonitor(unittest.TestCase):
    """RedisMonitor test case."""

    def setUp(self):
        """Redis Monitor test case setup."""
        pool = redis.ConnectionPool(host="redis", port=6379, db=0)
        self.redis = redis.Redis(connection_pool=pool)
        self.monitor = redis_monitor.RedisMonitor(pool)

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

        self.assertTrue(all(
            isinstance(el, bytes) for el in itertools.islice(monitor_result, 1)
        ))


if __name__ == '__main__':
    unittest.main()
