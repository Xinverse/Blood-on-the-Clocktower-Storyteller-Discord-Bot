"""Contains the Assassin Character class"""

import json
from botc import Character, Minion
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.assassin.value.lower()]


class Assassin(Minion, BadMoonRising, Character):
    """Assassin: Once per game, at night*, choose a player: they die, even if for some reason they could not.
    """

    def __init__(self):

        Character.__init__(self)
        BadMoonRising.__init__(self)
        Minion.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/e/e0/Assassin_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Assassin"

        self._role_enum = BMRRole.assassin