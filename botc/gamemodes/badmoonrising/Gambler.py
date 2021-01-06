"""Contains the Gambler Character class"""

import json
from botc import Character, Townsfolk
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.gambler.value.lower()]


class Gambler(Townsfolk, BadMoonRising, Character):
    """Gambler: Each night*, choose a player & guess their character: if you guess wrong, you die.
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

        self._art_link = "https://bloodontheclocktower.com/wiki/images/f/f5/Gambler_Token.png"
        self._art_link_cropped = "https://imgur.com/vkiURKP.png"
        self._wiki_link = "https://bloodontheclocktower.com/wiki/Gambler"

        self._role_enum = BMRRole.gambler
        self._emoji = "<:bmrgambler:781151556426792960>"
