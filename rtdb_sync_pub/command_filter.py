"""Provide Redis command filtering facilities.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import typing

from . import command

__all__ = ["filter_commands"]

DEFAULT_ALLOWED_COMMANDS = {
    "SET"
}


def filter_commands(commands_iter: typing.Iterable[command.Command],
                    allowed_commands: set=DEFAULT_ALLOWED_COMMANDS) \
        -> typing.Iterable[command.Command]:
    """Filter Redis commands based on a pre-defined set of allowed ones.

    Produce an iterable of Redis commands filtered with just the allowed ones.
    If no value is provided for the `allowed_commands` parameter then all the
    Redis commands that modify the database are allowed.

    :param commands_iter: Iterable source of commands.
    :param allowed_commands: Set of allowed commands.
    """
    [(yield comm) for comm in commands_iter
        if comm.command in allowed_commands]
