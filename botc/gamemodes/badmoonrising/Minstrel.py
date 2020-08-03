"""Contains the Minstrel Character class"""

import json
from botc import Character, Townsfolk
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.minstrel.value.lower()]


class Minstrel(Townsfolk, BadMoonRising, Character):
    """Minstrel: If a Minion died today, all other players (except Travelers) are drunk that 
    night until dusk.
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

        self._art_link = "http://bloodontheclocktower.com/wiki/images/0/03/Minstrel_Token.png"
        self._art_link_cropped = "https://imgur.com/3lmSmQp.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Minstrel"

        self._role_enum = BMRRole.minstrel
        self._emoji = "<:minstrel:722688861213556807>"
        