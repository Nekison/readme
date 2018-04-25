"""Provide Real Time Database command transform facilities.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import typing

from . import command

__all__ = ["prefix_key_name"]


def prefix_key_name(commands_iter: typing.Iterable[command.Command],
                    prefix: str) -> typing.Iterable[command.Command]:
    """Prefix Real Time Database command key name.

    :param commands_iter: Iterable source of commands.
    :param prefix: Key name prefix.
    """
    for comm in commands_iter:
        comm.key_name = "{}{}".format(prefix, comm.key_name)
        yield comm
