"""Contains the Po Character class"""

import json
from botc import Character, Demon
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.po.value.lower()]


class Po(Demon, BadMoonRising, Character):
    """Po: Each night*, you may choose a player: they die. If you chose no-one last night, 
    choose 3 players tonight.
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

        self._art_link = "http://bloodontheclocktower.com/wiki/images/7/7b/Po_Token.png"
        self._art_link_cropped = "https://imgur.com/aBHkr6t.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Po"

        self._role_enum = BMRRole.po
        self._emoji = "<:po:722688861343318046>"
