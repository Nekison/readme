"""Module for declare custom execption."""


__all__ = ["MqttBrokerIsDown"]


class Error(Exception):
    """Base class for other exceptions."""


class MqttBrokerIsDown(Error):
    """Class to indicate that mqtt broker is down."""
