"""Contains the Pit-Hag Character class"""

import json
from botc import Character, Minion
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.pithag.value.lower()]


class PitHag(Minion, SectsAndViolets, Character):
    """Pit-Hag: Each night*, choose a player & character they become (if not-in-play). If a Demon is made, deaths tonight are arbitrary.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Minion.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "https://bloodontheclocktower.com/wiki/images/6/63/Pit_Hag_Token.png"
        self._wiki_link = "https://bloodontheclocktower.com/wiki/Pit_Hag"

        self._role_enum = SnVRole.pithag
