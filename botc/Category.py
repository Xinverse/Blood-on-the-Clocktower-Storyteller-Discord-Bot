"""Contains the BOTC Category class"""

import enum

class Category(enum.Enum):
    """BoTC role category enum object: Townsfolk, Outsider, Minion, Demon"""

    townsfolk = "Townsfolk"
    outsider = "Outsider"
    minion = "Minion"
    demon = "Demon"