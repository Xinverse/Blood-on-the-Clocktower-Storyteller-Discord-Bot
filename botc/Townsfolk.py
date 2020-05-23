from .Category import Category
from .Team import Team

class Townsfolk:
    """Townsfolk object"""

    def __init__(self):
        self._category = Category.townsfolk
        self._team = Team.good
    
    @property
    def category(self):
        return self._category
    
    @property
    def team(self):
        return self._team
        