"""Contains the Player State class"""

import enum

class PlayerState(enum.Enum):
    """Player State class"""

    alive = "alive"
    dead = "dead"
    fleaved = "fleaved"