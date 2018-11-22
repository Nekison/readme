"""Module to provide mqtt utilities."""


__all__ = ["on_connect", "on_publish"]


def on_connect(client, userdata, flags, rc):
    """Log MQTT CONNACK response information.

    Used as MQTT client on_connect callback.
    """
    print("MQTT Client Connected with result code {}".format(str(rc)))


def on_publish(client, userdata, result):
    """Log MQTT PUBACK information.

    Used as MQTT client on_publish callback.
    """
    print("MQTT Message Published with result code {}".format(str(result)))
