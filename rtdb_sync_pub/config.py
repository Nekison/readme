"""Provide Time Series Database Subscriber configuration utilities.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import configargparse

__all__ = ["setup_parser"]


def setup_parser(parser: configargparse.ArgParser) -> configargparse.ArgParser:
    """Set up ArgParser instance for this application."""
    parser.add("--mqtt-host",
               type=str,
               action="store",
               default="mqtt-broker",
               help="MQTT broker to connect to")

    parser.add("--mqtt-topic",
               type=str,
               action="store",
               default="/",
               help="MQTT topic to listen to messages")

    parser.add("--redis-host",
               type=str,
               action="store",
               default="redis",
               help="Redis host to connect to")

    parser.add("--redis-db",
               type=int,
               action="store",
               default=0,
               help="Redis database to connect to")

    return parser
