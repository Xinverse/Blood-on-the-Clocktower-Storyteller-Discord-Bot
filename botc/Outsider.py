"""Contains the Outisder class"""

from .Category import Category
from .Team import Team

class Outsider:
    """Outsider class"""

    def __init__(self):
        self._category = Category.outsider
        self._team = Team.good

        