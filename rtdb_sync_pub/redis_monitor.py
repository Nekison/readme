"""Provide Redis monitoring facilities.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

__all__ = ["RedisMonitor"]


class RedisMonitor:
    """Monitor Redis and notify changes."""

    def monitor(self):
        """Produce an iterable of changes on the Redis database."""
        return iter([])
