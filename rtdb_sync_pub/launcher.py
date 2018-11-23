#!/usr/bin/python3
"""Application launcher.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

# Standard library imports
import json
import sys
import time
import queue

# Third party imports
import configargparse
import redis
from redis.exceptions import ConnectionError, TimeoutError

# Local application imports
from .utils.exceptions import MqttBrokerIsDown, MqttBrokerNotFound
from .utils.mqtt import client as mqtt_client
from . import __version__, monitor, command, filter, transform, config

if __name__ == '__main__':
    try:
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

        exec_queue = queue.Queue()
        mqtt_client = mqtt_client.create(args, exec_queue)

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

                    result = mqtt_client.publish(comm.key_name,
                                                 json.dumps(comm.__dict__), 1)
                    print("MQTT Message Publish called for topic {} with result {}"
                          .format(comm.key_name, str(result)))

                time.sleep(2)

                # Check exec queue from mqtt client thread
                if exec_queue.empty():
                    continue
                else:
                    q_info = exec_queue.get()
                    if q_info == "BROKER_DOWN":
                        raise MqttBrokerIsDown
                    elif q_info == "BROKER_NOT_CONNECTED":
                        raise MqttBrokerNotFound
                    else:
                        print(q_info)

            except ConnectionError as e:
                print("{}".format(str(e)))
            except TimeoutError as e:
                print("{}".format(str(e)))
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
    except MqttBrokerIsDown as error:
        print("Mqtt broker is down application will end")
        sys.exit(1)
    except MqttBrokerNotFound as error:
        print("Connection to mqtt broker can't be established")
        sys.exit(1)
