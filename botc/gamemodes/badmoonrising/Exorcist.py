"""Contains the Exorcist Character class"""

import json
from botc import Character, Townsfolk
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.exorcist.value.lower()]


class Exorcist(Townsfolk, BadMoonRising, Character):
    """Exorcist: Each night*, choose a player (not the same as last night): the Demon, if chosen, 
    learns who you are & does not act tonight.
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

        self._art_link = "http://bloodontheclocktower.com/wiki/images/9/9a/Exorcist_Token.png"
        self._art_link_cropped = "https://imgur.com/4Df7WYp.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Exorcist"

        self._role_enum = BMRRole.exorcist
        self._emoji = "<:bmrexorcist:781151556442521620>"
        
