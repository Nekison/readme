"""Module for declare custom execption."""


__all__ = ["MqttBrokerIsDown", "MqttBrokerNotFound"]


class Error(Exception):
    """Base class for other exceptions."""


class MqttBrokerIsDown(Error):
    """Class to indicate that mqtt broker is down."""


class MqttBrokerNotFound(Error):
    """Class to indicate that mqtt client can't establish connection with mqtt broker."""
