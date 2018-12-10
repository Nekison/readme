"""Module for declare custom exceptions."""


__all__ = ["MqttBrokerIsDown", "MqttBrokerNotFound"]


class MqttBrokerIsDown(Exception):
    """Class to indicate that mqtt broker is down."""


class MqttBrokerNotFound(Exception):
    """Class to indicate that mqtt client can't connect with mqtt broker."""
