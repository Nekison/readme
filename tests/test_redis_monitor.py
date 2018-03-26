# Copyright (c) 2018, Sorbotics LLC.
# All rights reserved.

import unittest

from rtdb_sync_pub import redis_monitor


class TestRedisMonitor(unittest.TestCase):

    def setUp(self):
        self.monitor = redis_monitor.RedisMonitor()

    def test_monitor_return_iterable(self):
        """ Test that monitor() method produce an iterable.
        """
        monitorResult = self.monitor.monitor()

        try:
            iter(monitorResult)
        except TypeError:
            self.fail("monitor() return value is not iterable")


if __name__ == '__main__':
    unittest.main()
