"""Contains the custum game error classes"""

class GameError(Exception):
    """Game Error class, for general errors"""
    pass


class TooManyPlayers(Exception):
    """Too many players"""
    pass


class TooFewPlayers(Exception):
    """Too few players"""
    pass
