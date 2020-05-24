"""Contains the Minion class"""

from .Category import Category
from .Team import Team

class Minion:
    """Minion class"""

    def __init__(self):
        self._category = Category.minion
        self._team = Team.evil

