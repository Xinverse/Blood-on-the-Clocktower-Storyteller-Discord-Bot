"""Contains the Master State class"""

import time
from .Pregame import Pregame
from .BotState import BotState

class MasterState:
    """Master State class: the bot's global state"""

    def __init__(self):
        self._boottime = time.time()
        self._pregame = Pregame()
        self._game = None
        self._session = BotState.empty
    
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
    
    @property
    def session(self):
        return self._session
    
    def transition_to_pregame(self):
        self._session = BotState.pregame
    
    def transition_to_empty(self):
        self._session = BotState.empty
    
    def transition_to_game(self):
        self._session = BotState.game
        self.pregame.clear()
    
    def __str__(self):
        return f"Master State at pregame: {str(self.pregame)}, and game:{str(self.game)}"

    def __repr__(self):
        return self.__str__()