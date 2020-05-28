"""Contains the Phase class"""

import enum

class Phase(enum.Enum):
    """Phase class: day, night, idle"""

    day = "day"
    night = "night"
    idle = "idle"