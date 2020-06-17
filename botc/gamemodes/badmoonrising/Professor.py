"""Contains the Professor Character class"""

import json
from botc import Character, Townsfolk
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.professor.value.lower()]


class Professor(Townsfolk, BadMoonRising, Character):
    """Professor: Once per game, at night, choose a dead player: if they are a Townsfolk, 
    they are resurrected.
    """

    def __init__(self):

        Character.__init__(self)
        BadMoonRising.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/a/ac/Professor_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Professor"

        self._role_enum = BMRRole.professor
