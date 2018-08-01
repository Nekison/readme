"""Provide Real Time Database command filtering facilities.

Copyright (c) 2018, Sorbotics LLC.
All rights reserved.
"""

import json
import typing

from . import command

__all__ = ["filter_allowed_commands", "filter_target_database",
           "CommandFilterQueue"]

ALLOWED_COMMANDS = {
    "SET", "LPUSH", "RPUSH", "BRPOP"
}

TARGET_DATABASE = 0


def filter_allowed_commands(commands_iter: typing.Iterable[command.Command],
                            allowed_commands: set = ALLOWED_COMMANDS) \
        -> typing.Iterable[command.Command]:
    """Filter Real Time Database commands based on pre-defined set of allowed.

    Produce an iterable of Real Time Database commands filtered with just the
    allowed ones. If no value is provided for the `allowed_commands` parameter
    then all the Real Time Database commands that modify the database are
    allowed.

    :param commands_iter: Iterable source of commands.
    :param allowed_commands: Set of allowed commands.
    """
    return [(yield comm) for comm in commands_iter
            if comm.command in allowed_commands]


def filter_target_database(commands_iter: typing.Iterable[command.Command],
                           target_database: int = TARGET_DATABASE) \
        -> typing.Iterable[command.Command]:
    """Filter Real Time Database commands based on the target database.

    :param commands_iter: Iterable source of commands.
    :param target_database: Target Real Time Database.
    """
    return [(yield comm) for comm in commands_iter
            if comm.database == target_database]


class CommandFilterQueue:
    """Queue based Command filter."""

    def __init__(self, key_name: str = "command_queue"):
        """Initialize the CommandFilterQueue instance.

        :param key_name: Name of the Real Time Database key holding the queue.
        """
        self.key_name = key_name
        self.commands = list()

    def _is_queue_command(self, comm: command.Command) -> bool:
        return comm.key_name == self.key_name and comm.command == "RPUSH"

    def _register_command(self, comm: command.Command):
        el = json.loads(''.join(comm.arguments).replace('\\\\"', '\\"'))

        self.commands.append(command.Command(el["timestamp"], el["database"], None,
                                             el["command"], el["key_name"],
                                             el["arguments"]))

    def _find_command(self, comm: command.Command) -> bool:
        # skip checking if command queue is empty
        if len(self.commands) < 1:
            return False

        el = self.commands[0]



        # TODO: need to compare all arguments
        return el.database == comm.database \
            and el.command == comm.command \
            and el.key_name == comm.key_name

    def _unregister_command(self, comm: command.Command):
        self.commands.pop()

    def filter(self, commands_iter: typing.Iterable[command.Command]) \
            -> typing.Iterable[command.Command]:
        """Filter all commands produced by the iterable using the queue."""
        for comm in commands_iter:
            # if command is directed to the queue store it for latter use
            if self._is_queue_command(comm):
                print("Adding queue command {} {}".format(comm.__dict__, len(comm.arguments)))
                self._register_command(comm)
            elif self._find_command(comm):
                print("Unregister queue command {}".format(comm.__dict__))
                self._unregister_command(comm)
            else:
                yield comm
