"""Contains the Mastermind Character class"""

import json
from botc import Character, Minion
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.mastermind.value.lower()]


class Mastermind(Minion, BadMoonRising, Character):
    """Mastermind: If the Demon dies by execution, play for 1 more day. If a player 
    is then executed, their team loses
    """

    def __init__(self):

        Character.__init__(self)
        BadMoonRising.__init__(self)
        Minion.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/d/d5/Mastermind_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Mastermind"

        self._role_enum = BMRRole.mastermind
        