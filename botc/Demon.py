"""Contains the Demon class"""

from .Category import Category
from .Team import Team

class Demon:
    """Demon class"""
    
    def __init__(self):
        self._category = Category.demon
        self._team = Team.evil
