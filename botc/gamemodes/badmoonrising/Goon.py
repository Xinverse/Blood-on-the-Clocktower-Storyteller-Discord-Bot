"""Contains the Goon Character class"""

import json
from botc import Character, Outsider
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.goon.value.lower()]


class Goon(Outsider, BadMoonRising, Character):
    """Goon: Each night, the 1st player to choose you with their ability is drunk until dusk. 
    You become their alignment.
    """

    def __init__(self):

        Character.__init__(self)
        BadMoonRising.__init__(self)
        Outsider.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/a/a4/Goon_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Goon"

        self._role_enum = BMRRole.goon
