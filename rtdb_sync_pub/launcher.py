#!/usr/bin/python3
"""Application launcher.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import json
import time
import redis
import sys
import configargparse
import paho.mqtt.client as mqtt
from redis.exceptions import ConnectionError, TimeoutError

from . import __version__, monitor, command, filter, transform, config


def mqtt_on_connect(client, userdata, flags, rc):
    """Log MQTT CONNACK response information.

    Used as MQTT client on_connect callback.
    """
    print("MQTT Client Connected with result code {}".format(str(rc)))


def mqtt_on_publish(client, userdata, result):
    """Log MQTT PUBACK information.

    Used as MQTT client on_publish callback.
    """
    print("MQTT Message Published with result code {}".format(str(result)))


if __name__ == '__main__':
    print("Starting Real Time Database Synchronization Publisher Ver.",
          __version__)

    arg_parser = config.setup_parser(configargparse.ArgParser())

    args = arg_parser.parse_args()

    # print application configuration
    print(arg_parser.format_values())

    # pool = redis.ConnectionPool(host='192.168.1.141', port=6379, db=0)
    pool = redis.ConnectionPool(host=args.redis_host, port=6379,
                                db=args.redis_db)
    r = redis.Redis(connection_pool=pool)

    client = mqtt.Client()

    # setup client settings
    client.on_connect = mqtt_on_connect
    client.on_publish = mqtt_on_publish
    client.enable_logger()

    if args.mqtt_port != 1883:
        client.tls_set(ca_certs=args.mqtt_ca_certs)

        client.tls_insecure_set(args.mqtt_tls_insecure)

    client.loop_start()

    client.connect_async(args.mqtt_host, args.mqtt_port)

    monitor = monitor.RedisMonitor(pool)
    filter_queue = filter.CommandFilterQueue()

    print("Starting Real Time Database monitoring")

    limit_time = args.limit_time
    previous_error_time = None
    start_time = None

    while True:
        try:
            for comm in transform.set_agent(
                    transform.prefix_key_name(
                    filter.filter_allowed_commands(
                    filter_queue.filter(
                    filter.filter_target_database(
                    command.parse_responses(monitor.monitor()),
                        args.redis_db))),
                    args.mqtt_topic), args.agent_id):

                result = client.publish(comm.key_name,
                                        json.dumps(comm.__dict__), 1)
                print("MQTT Message Publish called for topic {} with result {}"
                      .format(comm.key_name, str(result)))
        except ConnectionError as e:
            print("{}".format(str(e)))
        except TimeoutError as e:
            print("{}".format(str(e)))
        except Exception as e:
            print(str(e))
        finally:
            if start_time is None:
                start_time = time.time()
            else:
                error_time = time.time() - previous_error_time
                if error_time >= 2:
                    start_time = time.time()
                else:
                    elapsed_time = time.time() - start_time
                    elapsed_time_int = int(elapsed_time)
                    if elapsed_time_int >= int(limit_time):
                        print("Error during synchronization, "
                              "try to recover for {} seconds".
                              format(limit_time))
                        sys.exit(1)

            previous_error_time = time.time()
