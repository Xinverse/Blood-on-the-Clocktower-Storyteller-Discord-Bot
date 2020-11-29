"""Contains the Sweetheart Character class"""

import json
from botc import Character, Outsider
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.sweetheart.value.lower()]


class Sweetheart(Outsider, SectsAndViolets, Character):
    """Sweetheart: If you die, 1 player is drunk from now on.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Outsider.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "https://bloodontheclocktower.com/wiki/images/3/34/Sweetheart_Token.png"
        self._wiki_link = "https://bloodontheclocktower.com/wiki/Sweetheart"

        self._role_enum = SnVRole.sweetheart
