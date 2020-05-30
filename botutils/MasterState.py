"""Contains the Master State class"""

import time

class MasterState:
    """Master State class: the bot's global state"""

    def __init__(self):
        self._boottime = time.time()
        self._pregame = None
        self._game = None
    
    @property
    def boottime(self):
        return self._boottime

    @property
    def pregame(self):
        return self._pregame
    
    @pregame.setter
    def pregame(self, new):
        self._pregame = new
    
    @property
    def game(self):
        return self._game
    
    @game.setter
    def game(self, new):
        self._game = new
    
    def __str__(self):
        return f"Master State at pregame: {str(self.pregame)}, and game:{str(self.game)}"

    def __repr__(self):
        return self.__str__()