"""Provide Redis command class.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import typing

__all__ = ["Command", "parse_response", "parse_responses"]


class Command:
    """Real Time Database Command.

    Represents a command issued to the Real Time Database. It conveys
    information about the issuer and the command issued.
    """

    def __init__(self, timestamp=None, database=None, client=None,
                 command=None, key_name=None, arguments=None):
        """Initialize command."""
        self.timestamp = timestamp
        self.database = database
        self.client = client
        self.command = command
        self.key_name = key_name
        self.arguments = arguments


def parse_response(response: bytes) -> Command:
    """Parse a Redis response.

    Produce a dictionary containing the parts that compose the command.
    """
    comm = Command()

    response = response.decode()

    parts = response.split(" ")

    if len(parts) == 1:
        raise Exception("Invalid number of arguments")

    comm.timestamp = float(parts[0].strip())

    comm.database = parts[1][1:]

    comm.client = parts[2][:-1]

    comm.command = parts[3].replace('"', '').upper()

    if len(parts) > 2:
        comm.key_name = parts[4].replace('"', '').strip()

    if len(parts) > 3:
        comm.arguments = parts[3:]

    return comm


def parse_responses(response_iter: typing.Iterable[bytes]) \
        -> typing.Iterable[Command]:
    """Parse Redis response messages.

    Produce an iterable of Redis commands.
    :param response_iter: An iterable of Redis responses.
    """
    for response in response_iter:
        try:
            yield parse_response(response)
        except Exception as e:
            print("An Exception was raised on the parse_responses() generator")
            print(str(e))
