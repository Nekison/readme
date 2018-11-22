"""Module to provide mqtt utilities."""

# Third party modules
import paho.mqtt.client as mqtt

__all__ = ["create_client"]


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


def create_client(args):
    client = mqtt.Client()

    # setup client settings
    client.on_connect = _on_connect
    client.on_publish = _on_publish
    client.enable_logger()

    if args.mqtt_port != 1883:
        client.tls_set(ca_certs=args.mqtt_ca_certs)

        client.tls_insecure_set(args.mqtt_tls_insecure)

    client.loop_start()

    client.connect_async(args.mqtt_host, args.mqtt_port)

    return client
