"""Contains the Oracle Character class"""

import json
from botc import Character, Townsfolk
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.oracle.value.lower()]


class Oracle(Townsfolk, SectsAndViolets, Character):
    """Oracle: Each night*, you learn how many dead players are evil.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/2/26/Oracle_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Oracle"

        self._role_enum = SnVRole.oracle
