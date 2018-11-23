"""Module to provide mqtt utilities."""

# Standard library imports
import sys
import time

# Third party imports
import paho.mqtt.client as mqtt

# Local application imports
from .exceptions import MqttBrokerIsDown


__all__ = ["create_client"]


def _on_disconnect(args, exec_queue):
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
                    exec_queue.put("BROKER_DOWN")
                    sys.exit(1)
                else:
                    time.sleep(1)
                    continue

    return inner_on_disconnect


def _on_connect(client, userdata, flags, rc):
    """Log MQTT CONNACK response information.

    Used as MQTT client on_connect callback.
    """
    print("MQTT Client Connected with result code {}".format(str(rc)))


def _on_publish(client, userdata, result):
    """Log MQTT PUBACK information.

    Used as MQTT client on_publish callback.
    """
    print("MQTT Message Published with result code {}".format(str(result)))


def create_client(args, exec_queue):
    client = mqtt.Client()

    # setup client settings
    client.on_connect = _on_connect
    client.on_publish = _on_publish
    client.on_disconnect = _on_disconnect(args, exec_queue)

    client.enable_logger()

    if args.mqtt_port != 1883:
        client.tls_set(ca_certs=args.mqtt_ca_certs)

        client.tls_insecure_set(args.mqtt_tls_insecure)

    client.loop_start()

    client.connect_async(args.mqtt_host, args.mqtt_port)

    return client
