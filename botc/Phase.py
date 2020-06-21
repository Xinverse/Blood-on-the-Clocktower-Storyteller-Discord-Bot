"""Contains the Phase class"""

import enum

class Phase(enum.Enum):
    """Phase class: day, night, idle"""

    idle = "idle"
    night = "night"
    day = "day"
   
    