"""Provide Redis monitoring facilities.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""
import time

from redis import exceptions as redis_exceptions

__all__ = ["RedisMonitor"]


class RedisMonitor:
    """Monitor Redis and notify changes."""

    def __init__(self, connection_pool):
        """Initialize the Redis monitor.

        Takes as argument a Redis connection pool as produced by
        `redis.ConnectionPool`.
        """
        self._connection_pool = connection_pool
        self._connection = None

    def __del__(self):
        """Release resources on delete."""
        try:
            self._reset()
        except Exception:
            pass

    def _reset(self):
        if self._connection:
            self._connection_pool.release(self._connection)
            self._connection = None

    def _read_response(self):
        return self._connection.read_response()

    def _listen(self):
        while True:
            try:
                yield self._read_response()
            except redis_exceptions.TimeoutError as e:
                raise redis_exceptions.TimeoutError(
                    "{} While listening to the response".format(str(e)))
            except redis_exceptions.ConnectionError as e:
                raise redis_exceptions.ConnectionError(
                    "{} While sending the monitor command".format(str(e)))
            except Exception as e:
                raise Exception("{} while sending the monitor command"
                                .format(str(e)))

    def monitor(self):
        """Produce an iterable of changes on the Redis database."""
        if self._connection is None:
            self._connection = self._connection_pool.get_connection(
                'monitor', None)
        self._send_command_monitor()
        return self._listen()

    def _send_command_monitor(self):
        try:
            self._connection.send_command("monitor")
        except TimeoutError as e:
            raise TimeoutError("{} While sending the monitor command"
                               .format(str(e)))
        except ConnectionError as e:
            raise ConnectionError("{} While sending the monitor command"
                                  .format(str(e)))
        except Exception as e:
            raise Exception("{} while sending the monitor command"
                            .format(str(e)))
