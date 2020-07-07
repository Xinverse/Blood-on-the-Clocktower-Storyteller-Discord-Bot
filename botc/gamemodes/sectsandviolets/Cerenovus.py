"""Contains the Cerenovus Character class"""

import json
from botc import Character, Minion
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.cerenovus.value.lower()]


class Cerenovus(Minion, SectsAndViolets, Character):
    """Cerenovus: Each night, choose a player & a good character: they are mad about being this character tomorrow, or might be executed.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Minion.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/9/9d/Cerenovus_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Cerenovus"

        self._role_enum = SnVRole.cerenovus
