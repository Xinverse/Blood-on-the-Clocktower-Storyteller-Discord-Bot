"""Contains the Chrono object to keep track of in game time"""

import math
from .Phase import Phase


class GameChrono:
    """Game Chrono class to represent game chronology
    0 = idle phase (pregame)
    1 = night 1
    2 = dawn 1
    3 = day 1
    4 = night 2
    5 = dawn 2
    6 = day 2
    etc.
    """

    def __init__(self):
        self.current = 0
    
    def next(self):
        self.current += 1
    
    def is_night_1(self):
        return self.current == 1
    
    @property
    def phase_id(self):
        return self.current

    @property
    def cycle(self):
        """The nth cycle"""
        return math.ceil(self.current/3)
    
    @property
    def phase(self):
        """Whether night or day"""
        if self.current == 0:
            return Phase.idle
        else:
            if self.current % 3 == 0:
                return Phase.day
            elif self.current % 3 == 1:
                return Phase.night
            else:
                return Phase.dawn
