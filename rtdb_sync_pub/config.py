"""Provide Time Series Database Publisher configuration utilities.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import configargparse

__all__ = ["setup_parser"]


def setup_parser(parser: configargparse.ArgParser) -> configargparse.ArgParser:
    """Set up ArgParser instance for this application."""
    parser.add("-c",
               "--config",
               required=False,
               is_config_file=True,
               help="Real Time Database Synchronization Publisher "
                    "configuration file path")

    parser.add("--mqtt-host",
               type=str,
               action="store",
               default="mqtt-broker",
               env_var='MQTT_HOST',
               help="MQTT broker to connect to")

    parser.add("--mqtt-port",
               type=int,
               action="store",
               default=1883,
               help="Inet port to connect to")

    parser.add("--mqtt-ca-certs",
               type=str,
               action="store",
               default=None,
               help="MQTT Certificate Authority certificate files")

    parser.add("--mqtt-tls-insecure",
               type=bool,
               action="store",
               default=False,
               help="MQTT TLS is insecure")

    parser.add("--mqtt-topic",
               type=str,
               action="store",
               default="/",
               env_var='MQTT_TOPIC',
               help="MQTT topic to listen to messages")

    parser.add("--redis-host",
               type=str,
               action="store",
               default="redis",
               env_var='REDIS_HOST',
               help="Redis host to connect to")

    parser.add("--redis-db",
               type=int,
               action="store",
               default=0,
               env_var='REDIS_DB',
               help="Redis database to connect to")

    parser.add("--agent-id",
               type=str,
               action="store",
               default="root-rtdb",
               env_var='AGENT_ID',
               help="Process agent used to complement the sync")

    return parser
