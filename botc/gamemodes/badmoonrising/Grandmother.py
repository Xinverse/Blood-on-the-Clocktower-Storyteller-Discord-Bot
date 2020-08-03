"""Contains the Grandmother Character class"""

import json
from botc import Character, Townsfolk
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.grandmother.value.lower()]


class Grandmother(Townsfolk, BadMoonRising, Character):
    """Grandmother: You start knowing a good player & character. If the Demon kills them, you die too.
    """

    def __init__(self):

        Character.__init__(self)
        BadMoonRising.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        self._brief_string = character_text["brief"]
        self._action = character_text["action"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/3/3a/Grandmother_Token.png"
        self._art_link_cropped = "https://imgur.com/goIkjnU.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Grandmother"

        self._role_enum = BMRRole.grandmother
        self._emoji = "<:grandmother:722688860450062347>"
        