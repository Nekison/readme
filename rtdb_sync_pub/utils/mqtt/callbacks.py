"""Module to declare mqtt callbacks used in the application."""

# Standard library imports
import sys
import time


# Local application imports
from . import events

__all__ = ["on_disconnect", "on_connect", "on_publish"]


def on_disconnect(args, events_queue):
    """Manage disconnect event from mqtt broker."""
    timeout_time = args.limit_time

    def inner_on_disconnect(client, userdata, result):
        start_time = time.time()

        while True:
            try:
                print("Trying to reconnect mqtt client to {} broker"
                      .format(args.mqtt_host))

                client.reconnect()
                break
            except ConnectionRefusedError as error:
                elapsed_time = time.time() - start_time

                if elapsed_time > timeout_time:
                    client.loop_stop()
                    events_queue.put(events.MQTT_BROKER_DOWN)

                    # Finishing mqtt client thread
                    sys.exit(1)
                else:
                    time.sleep(1)
                    continue

    return inner_on_disconnect


def on_connect(events_queue):
    """High order function to create on_connect callback use by mqtt client."""
    def inner_on_connect(client, userdata, flags, rc):
        """Log MQTT CONNACK response information.

        Used as MQTT client on_connect callback.
        """
        events_queue.put(events.CLIENT_CONNECTED)
        print("MQTT Client Connected with result code {}".format(str(rc)))

    return inner_on_connect


def on_publish(client, userdata, result):
    """Log MQTT PUBACK information.

    Used as MQTT client on_publish callback.
    """
    print("MQTT Message Published with result code {}".format(str(result)))
