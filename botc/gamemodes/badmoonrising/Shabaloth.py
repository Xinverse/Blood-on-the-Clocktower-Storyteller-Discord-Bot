"""Contains the Shabaloth Character class"""

import json
from botc import Character, Demon
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.shabaloth.value.lower()]


class Shabaloth(Demon, BadMoonRising, Character):
    """Shabaloth: Each night*, choose 2 players: they die. A dead player you chose last night 
    might be regurgitated.
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

        self._art_link = "http://bloodontheclocktower.com/wiki/images/7/75/Shabaloth_Token.png"
        self._art_link_cropped = "https://imgur.com/vWrBrvS.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Shabaloth"

        self._role_enum = BMRRole.shabaloth
        self._emoji = "<:shabaloth:722688861788045314>"
        