"""Contains the Dreamer Character class"""

import json
from botc import Character, Townsfolk
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.dreamer.value.lower()]


class Dreamer(Townsfolk, SectsAndViolets, Character):
    """Dreamer: Each night, choose a player (not yourself): you learn 1 good character and 1 evil character, 1 of which is correct.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/2/2c/Dreamer_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Dreamer"

        self._role_enum = SnVRole.dreamer
