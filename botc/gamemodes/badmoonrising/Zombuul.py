"""Contains the Zombuul Character class"""

import json
from botc import Character, Demon
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.zombuul.value.lower()]


class Zombuul(Demon, BadMoonRising, Character):
    """Zombuul: Each night*, if no-one died today, choose a player: they die. The 1st time you die, 
    you do not, but appear to.
    """

    def __init__(self):

        Character.__init__(self)
        BadMoonRising.__init__(self)
        Demon.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        self._brief_string = character_text["brief"]
        self._action = character_text["action"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/c/c6/Zombuul_Token.png"
        self._art_link_cropped = "https://imgur.com/Z84oOaA.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Zombuul"

        self._role_enum = BMRRole.zombuul
        self._emoji = "<:zombuul:722688861980852265>"
        