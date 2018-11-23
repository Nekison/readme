"""Module to provide mqtt utilities."""

# Standard library imports
import sys
import time

# Third party imports
import paho.mqtt.client as mqtt

# Local application imports
from . import callbacks as cb
from . import events
from ..exceptions import MqttBrokerIsDown


__all__ = ["create"]


def _check_connection(args, exec_queue):
    start_time = time.time()
    timeout = args.limit_time

    while True:
        if exec_queue.qsize() == 0:
            elapse_time = time.time() - start_time
            if elapse_time > timeout:
                exec_queue.put(events.MQTT_BROKER_NOT_FOUND)
                break
            else:
                continue
        else:
            event = exec_queue.get()
            if event == events.CLIENT_CONNECTED:
                break

        time.sleep(1)


def create(args, exec_queue):
    client = mqtt.Client()

    # setup client settings
    client.on_connect = cb.on_connect(exec_queue)
    client.on_publish = cb.on_publish
    client.on_disconnect = cb.on_disconnect(args, exec_queue)

    client.enable_logger()

    if args.mqtt_port != 1883:
        client.tls_set(ca_certs=args.mqtt_ca_certs)
        client.tls_insecure_set(args.mqtt_tls_insecure)

    client.loop_start()
    client.connect_async(args.mqtt_host, args.mqtt_port,
                         keepalive=args.limit_time)

    print("Connecting to mqtt broker")
    _check_connection(args, exec_queue)

    return client
