"""Contains the Courtier Character class"""

import json
from botc import Character, Townsfolk
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.courtier.value.lower()]


class Courtier(Townsfolk, BadMoonRising, Character):
    """Courtier: Once per game, at night, choose a character: they are drunk for 3 nights & 3 days.
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

        self._art_link = "http://bloodontheclocktower.com/wiki/images/7/7d/Courtier_Token.png"
        self._art_link_cropped = "https://imgur.com/c1wt8jB.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Courtier"

        self._role_enum = BMRRole.courtier
        self._emoji = "<:courtier:722688860076769311>"
