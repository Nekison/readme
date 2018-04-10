"""Provide Redis monitoring facilities.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

__all__ = ["RedisMonitor"]


class RedisMonitor:
    """Monitor Redis and notify changes."""

    def __init__(self, connection_pool):
        self.connection_pool = connection_pool
        self.connection = None

    def __del__(self):
        try:
            self.reset()
        except:
            pass

    def reset(self):
        if self.connection:
            self.connection_pool.release(self.connection)
            self.connection = None

    def read_response(self):
        return self.connection.read_response()

    def listen(self):
        while True:
            yield self.read_response()

    def monitor(self):
        """Produce an iterable of changes on the Redis database."""
        if self.connection is None:
            self.connection = self.connection_pool.get_connection(
                'monitor', None)
        self.connection.send_command("monitor")
        return self.listen()
