"""Provide test cases for rtdb_sync_sub.config module.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import unittest

import configargparse

from rtdb_sync_pub import config


class TestSetupParser(unittest.TestCase):
    """setup_parser function test case."""

    def test_return_same_parser(self):
        """Test that it return the same parser given as argument."""
        arg_parser = configargparse.ArgParser()
        self.assertEqual(config.setup_parser(arg_parser), arg_parser)

    def test_it_set_mqtt_host_attr(self):
        """Test that mqtt_host attribute is set in product."""
        arg_parser = configargparse.ArgParser()
        args = config.setup_parser(arg_parser).parse_args(args=[])
        self.assertIn("mqtt_host", args)

    def test_it_set_mqtt_port_attr(self):
        """Test that mqtt_port attribute is set in product."""
        arg_parser = configargparse.ArgParser()
        args = config.setup_parser(arg_parser).parse_args(args=[])
        self.assertIn("mqtt_port", args)

    def test_it_set_mqtt_ca_certs_attr(self):
        """Test that mqtt_ca_certs attribute is set in product."""
        arg_parser = configargparse.ArgParser()
        args = config.setup_parser(arg_parser).parse_args(args=[])
        self.assertIn("mqtt_ca_certs", args)

    def test_it_set_mqtt_tls_insecure_attr(self):
        """Test that mqtt_tls_insecure attribute is set in product."""
        arg_parser = configargparse.ArgParser()
        args = config.setup_parser(arg_parser).parse_args(args=[])
        self.assertIn("mqtt_tls_insecure", args)

    def test_it_set_mqtt_topic_attr(self):
        """Test that mqtt_topic attribute is set in product."""
        arg_parser = configargparse.ArgParser()
        args = config.setup_parser(arg_parser).parse_args(args=[])
        self.assertIn("mqtt_topic", args)

    def test_it_set_redis_host_attr(self):
        """Test that redis_host attribute is set in product."""
        arg_parser = configargparse.ArgParser()
        args = config.setup_parser(arg_parser).parse_args(args=[])
        self.assertIn("redis_host", args)

    def test_it_set_redis_db_attr(self):
        """Test that redis_db attribute is set in product."""
        arg_parser = configargparse.ArgParser()
        args = config.setup_parser(arg_parser).parse_args(args=[])
        self.assertIn("redis_db", args)

    def test_it_set_agent_id_attr(self):
        """Test that agent_id attribute is set in product."""
        arg_parser = configargparse.ArgParser()
        args = config.setup_parser(arg_parser).parse_args(args=[])
        self.assertIn("agent_id", args)


if __name__ == '__main__':
    unittest.main()
