"""Provide test cases for rtdb_sync_pub.command module.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import os
import unittest

from rtdb_sync_pub import command


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
            command.parse_response(b"OK")
        except Exception as e:
            self.assertEqual(e.args[0], "Invalid number of arguments")

    def test_return_Command(self):
        """Test that parse_response() return a dictionary."""
        comm = command.parse_response(self.response)

        self.assertTrue(isinstance(comm, command.Command))

    def test_return_command_has_timestamp(self):
        """Test that return dictionary has timestamp attr."""
        comm = command.parse_response(self.response)

        self.assertTrue(hasattr(comm, "timestamp"))

    def test_return_command_has_database(self):
        """Test that return dictionary has database attr."""
        comm = command.parse_response(self.response)

        self.assertTrue(hasattr(comm, "database"))

    def test_return_command_has_client(self):
        """Test that return dictionary has client attr."""
        comm = command.parse_response(self.response)

        self.assertTrue(hasattr(comm, "client"))

    def test_return_command_has_command(self):
        """Test that return dictionary has command attr."""
        comm = command.parse_response(self.response)

        self.assertTrue(hasattr(comm, "command"))

    def test_return_command_has_key_name(self):
        """Test that return dictionary has key_name attr."""
        comm = command.parse_response(self.response)

        self.assertTrue(hasattr(comm, "key_name"))

    def test_return_command_has_arguments(self):
        """Test that return dictionary has arguments attr."""
        comm = command.parse_response(self.response)

        self.assertTrue(hasattr(comm, "arguments"))


class TestParseResponses(unittest.TestCase):
    """parse_responses function test case."""

    def setUp(self):
        """parse_response method test case setup."""
        script_dir = os.path.dirname(__file__)
        rel_path = "./valid-redis-command.txt"
        abs_file_path = os.path.join(script_dir, rel_path)

        with open(abs_file_path, "rb") as f:
            self.responses = [f.read()]

    def test_return_iterable(self):
        """Test that function produce an iterable."""
        result = command.parse_responses(self.responses)

        try:
            iter(result)
        except TypeError:
            self.fail("monitor() return value is not iterable")


if __name__ == '__main__':
    unittest.main()
