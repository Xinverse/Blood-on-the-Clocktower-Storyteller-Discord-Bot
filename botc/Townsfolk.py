"""Contains the Townsfolk class"""

from .Category import Category
from .Team import Team

class Townsfolk:
    """Townsfolk class"""

    def __init__(self):
        self._category = Category.townsfolk
        self._team = Team.good
