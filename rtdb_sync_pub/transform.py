"""Provide Real Time Database command transform facilities.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import typing

from . import command

__all__ = ["prefix_key_name", "set_agent"]


def prefix_key_name(commands_iter: typing.Iterable[command.Command],
                    prefix: str) -> typing.Iterable[command.Command]:
    """Prefix Real Time Database command key name.

    :param commands_iter: Iterable source of commands.
    :param prefix: Key name prefix.
    """
    for comm in commands_iter:
        comm.key_name = "{}{}".format(prefix, comm.key_name)
        yield comm

def set_agent(commands_iter: typing.Iterable[command.Command], agent: str) -> typing.Iterable[command.Command]: 
    """Set Real Time Database command agent.

    :param commands_iter: Iterable source of commands.
    :param agent: Agent Unique Identifier.
    """
    for comm in commands_iter:
        comm.agent = agent
        yield comm