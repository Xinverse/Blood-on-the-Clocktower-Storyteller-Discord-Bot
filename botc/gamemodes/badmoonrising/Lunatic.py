"""Contains the Lunatic Character class"""

import json
from botc import Character, Outsider
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.lunatic.value.lower()]


class Lunatic(Outsider, BadMoonRising, Character):
    """Lunatic: You think you are a Demon, but your abilities malfunction. 
    The Demon knows who you are & who you attack.
    """
    
    def __init__(self):

        Character.__init__(self)
        BadMoonRising.__init__(self)
        Outsider.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/5/56/Lunatic_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Lunatic"

        self._role_enum = BMRRole.lunatic
        