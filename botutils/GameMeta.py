"""Contains the Game Meta class"""

from abc import ABCMeta, abstractmethod, abstractproperty

class GameMeta(metaclass=ABCMeta):
    """A framework for how game classes should be designed.
    All game packs for this bot must inherit from this class, and implement these methods.
    """

    @abstractmethod
    def register_players(self, id_list):
        """Register the players"""
        pass

    @abstractmethod
    def start_game(self):
        """Start the game"""
        pass

    @abstractmethod
    def end_game(self):
        """End the game, compute winners etc."""
        pass

    @abstractproperty
    def phase(self):
        """Return the current phase the game is in (day, night, etc.)"""
        pass
