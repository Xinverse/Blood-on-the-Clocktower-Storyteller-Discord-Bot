"""Contains the Juggler Character class"""

import json
from botc import Character, Townsfolk
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.juggler.value.lower()]


class Juggler(Townsfolk, SectsAndViolets, Character):
    """Juggler: On your 1st day, publicly guess up to 5 player's characters. That night, you learn how many you got correct.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "https://bloodontheclocktower.com/wiki/images/b/b4/Juggler_Token.png"
        self._wiki_link = "https://bloodontheclocktower.com/wiki/Juggler"

        self._role_enum = SnVRole.juggler
