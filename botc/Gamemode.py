"""Contains the BOTC Gamemode class"""

import enum

class Gamemode(enum.Enum):
    """BoTC gamemode enum object: TB, BMR, S&V"""

    trouble_brewing = "Trouble-Brewing"
    bad_moon_rising = "Bad-Moon-Rising"
    sects_and_violets = "Sects-&-Violets"
