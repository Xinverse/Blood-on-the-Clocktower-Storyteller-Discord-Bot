"""Contains the custum game error classes"""

from discord.ext import commands


class GameError(Exception):
    """Game Error class, for general errors"""
    pass


class TooManyPlayers(Exception):
    """Too many players"""
    pass


class TooFewPlayers(Exception):
    """Too few players"""
    pass


class IncorrectNumberOfArguments(Exception):
    """Incorrect number of arguments passed"""
    pass


class AlreadyDead(commands.CommandInvokeError):
    """Error for when an already dead player is killed again"""
    pass
