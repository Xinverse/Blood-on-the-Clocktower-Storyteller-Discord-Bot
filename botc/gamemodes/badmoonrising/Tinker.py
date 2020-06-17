"""Contains the Tinker Character class"""

import json
from botc import Character, Outsider
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.tinker.value.lower()]


class Tinker(Outsider, BadMoonRising, Character):
    """Tinker: You might die at any time.
    """

    def __init__(self):

        Character.__init__(self)
        BadMoonRising.__init__(self)
        Outsider.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/e/e8/Tinker_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Tinker"

        self._role_enum = BMRRole.tinker
        