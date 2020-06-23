"""Contains the Phase class"""

import enum

class Phase(enum.Enum):
    """Phase class: 
    day -> daytime
    night -> nighttime
    idle -> out of game
    dawn -> between night and day
    """

    idle = "idle"
    night = "night"
    day = "day"
    dawn = "dawn"
    