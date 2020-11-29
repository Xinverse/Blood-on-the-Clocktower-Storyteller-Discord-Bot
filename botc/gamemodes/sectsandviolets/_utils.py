"""Contains SnVRole enum class and SectsAndViolets class"""

import enum
from botc.gamemodes import Gamemode


class SnVRole(enum.Enum):
    """Enum object for all Sects & Violets edition roles"""

    artist = "Artist"
    barber = "Barber"
    cerenovus = "Cerenovus"
    clockmaker = "Clockmaker"
    dreamer = "Dreamer"
    eviltwin = "Evil Twin"
    fanggu = "Fang Gu"
    flowergirl = "Flowergirl"
    juggler = "Juggler"
    klutz = "Klutz"
    mathematician = "Mathematician"
    mutant = "Mutant"
    nodashii = "No Dashii"
    oracle = "Oracle"
    philosopher = "Philosopher"
    pithag = "Pit-Hag"
    sage = "Sage"
    savant = "Savant"
    seamstress = "Seamstress"
    sweetheart = "Sweetheart"
    snakecharmer = "Snake Charmer"
    towncrier = "Town Crier"
    vigormortis = "Vigormortis"
    vortox = "Vortox"
    witch = "Witch"

    
class SectsAndViolets:
    """Parent class for all Sects & Violets edition roles"""

    def __init__(self):

        self._gm_of_appearance = Gamemode.sects_and_violets
        self._gm_art_link = "https://bloodontheclocktower.com/wiki/images/8/8f/SV_Logo.png"
        self._gm_main_page = "https://bloodontheclocktower.com/wiki/Sects_%26_Violets"
