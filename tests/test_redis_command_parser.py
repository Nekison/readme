"""Provide test cases for rtdb_sync_pub.redis_command_parser module.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import os
import unittest

from rtdb_sync_pub import redis_command_parser


class TestParseResponse(unittest.TestCase):
    """parse_response function test case."""

    def setUp(self):
        """parse_response method test case setup."""
        script_dir = os.path.dirname(__file__)
        rel_path = "./valid-redis-command.txt"
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path, "rb") as f:
            self.response = f.read()

    def test_raise_exception_inv_number_args(self):
        """Test parse_response() raise exception if body is not command."""
        try:
            redis_command_parser.parse_response(b"OK")
        except Exception as e:
            self.assertEqual(e.args[0], "Invalid number of arguments")

    def test_return_dict(self):
        """Test that parse_response() return a dictionary."""
        command = redis_command_parser.parse_response(self.response)

        self.assertTrue(isinstance(command, dict))


if __name__ == '__main__':
    unittest.main()
