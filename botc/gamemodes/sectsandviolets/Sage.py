"""Contains the Sage Character class"""

import json
from botc import Character, Townsfolk
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.sage.value.lower()]


class Sage(Townsfolk, SectsAndViolets, Character):
    """Sage: If the Demon kills you, you learn that it is 1 of 2 players.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/a/a7/Sage_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Sage"

        self._role_enum = SnVRole.sage
