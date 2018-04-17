"""Provide Redis command parsing facilities.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""


__all__ = ["parse_response", "parse_responses"]


def parse_response(response):
    """Parse a Redis response.

    Produce a dictionary containing the parts that compose the command.
    """
    command = {
        "timestamp": None,
        "database": None,
        "client": None,
        "command": None,
        "key_name": None,
        "arguments": None
    }

    response = response.decode()

    parts = response.split(" ")

    if len(parts) == 1:
        raise Exception("Invalid number of arguments")

    command["timestamp"] = float(parts[0].strip())

    command["database"] = parts[1][1:]

    command["client"] = parts[2][:-1]

    command["command"] = parts[3].replace('"', '').upper()

    if len(parts) > 2:
        command["key_name"] = parts[4].replace('"', '').strip()

    if len(parts) > 3:
        command["arguments"] = parts[3:]

    return command


def parse_responses(response_iter):
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
