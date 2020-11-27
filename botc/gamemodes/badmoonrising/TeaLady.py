"""Contains the Tea Lady Character class"""

import json
from botc import Character, Townsfolk
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.tealady.value.lower()]


class TeaLady(Townsfolk, BadMoonRising, Character):
    """Tea Lady: If both your alive neighbors are good, they can not die.
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

        self._art_link = "http://bloodontheclocktower.com/wiki/images/e/e7/Tea_Lady_Token.png"
        self._art_link_cropped = "https://imgur.com/oEHE6oQ.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Tea_Lady"

        self._role_enum = BMRRole.tealady
        self._emoji = "<:bmrtealady:781152054986539040>"
        
