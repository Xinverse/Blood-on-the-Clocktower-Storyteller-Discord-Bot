"""Contains TBRole enum class and TroubleBrewing class"""

import enum
from botc.gamemodes import Gamemode

class TBRole(enum.Enum):
    """Enum object for all Trouble Brewing edition roles"""

    washerwoman = "Washerwoman"
    librarian = "Librarian"
    investigator = "Investigator"
    chef = "Chef"
    empath = "Empath"
    fortuneteller = "Fortune Teller"
    undertaker = "Undertaker"
    monk = "Monk"
    ravenkeeper = "Ravenkeeper"
    virgin = "Virgin"
    slayer = "Slayer"
    soldier = "Soldier"
    mayor = "Mayor"
    butler = "Butler"
    drunk = "Drunk"
    recluse = "Recluse"
    saint = "Saint"
    poisoner = "Poisoner"
    scarletwoman = "Scarlet Woman"
    baron = "Baron"
    imp = "Imp"


class TroubleBrewing:
    """Parent class for all Trouble Brewing edition roles"""

    def __init__(self):

        self._gm_of_appearance = Gamemode.trouble_brewing
        self._gm_art_link = "http://bloodontheclocktower.com/wiki/images/9/92/TB_Logo.png"

