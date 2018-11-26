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
from .utils.mqtt import events, client as client_mqtt
from . import __version__, monitor, command, filter, transform, config


def check_mqtt_events(mqtt_events_queue):
    """Check if ocurred some event in thread for mqtt client."""
    if mqtt_events_queue.qsize() != 0:
        event = mqtt_events_queue.get()
        if event == events.MQTT_BROKER_DOWN:
            raise MqttBrokerIsDown
        elif event == events.MQTT_BROKER_NOT_FOUND:
            raise MqttBrokerNotFound
        else:
            print(event)


def main():
    """Create main function this is entry point for service."""
    print("Starting Real Time Database Synchronization Publisher Ver.",
          __version__)

    arg_parser = config.setup_parser(configargparse.ArgParser())

    args = arg_parser.parse_args()

    # print application configuration
    print(arg_parser.format_values())

    pool = redis.ConnectionPool(host=args.redis_host, port=6379,
                                db=args.redis_db)

    redis.Redis(connection_pool=pool)

    mqtt_events_queue = queue.Queue()
    mqtt_client = client_mqtt.create(args, mqtt_events_queue)

    redis_monitor = monitor.RedisMonitor(pool)
    filter_queue = filter.CommandFilterQueue()

    print("Starting Real Time Database monitoring - Publisher")

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
                    command.parse_responses(redis_monitor.monitor()),
                        args.redis_db))),
                    args.mqtt_topic), args.agent_id):

                result = mqtt_client.publish(comm.key_name,
                                             json.dumps(comm.__dict__), 1)
                print("MQTT Message Publish called for topic {} with result {}"
                      .format(comm.key_name, str(result)))

            time.sleep(2)
            check_mqtt_events(mqtt_events_queue)

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


if __name__ == '__main__':
    try:
        main()
    except MqttBrokerIsDown as error:
        print("Mqtt broker is down application will end")
        sys.exit(1)
    except MqttBrokerNotFound as error:
        print("Connection to mqtt broker can't be established")
        sys.exit(1)
