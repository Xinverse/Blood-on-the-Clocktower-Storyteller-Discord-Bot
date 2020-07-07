"""Contains the Klutz Character class"""

import json
from botc import Character, Outsider
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.klutz.value.lower()]


class Klutz(Outsider, SectsAndViolets, Character):
    """Klutz: When you learn that you died, publicly choose 1 alive player: if they are evil, your team loses.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Outsider.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/2/2a/Klutz_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Klutz"

        self._role_enum = SnVRole.klutz
