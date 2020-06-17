"""Contains the Pukka Character class"""

import json
from botc import Character, Demon
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.pukka.value.lower()]


class Pukka(Demon, BadMoonRising, Character):
    """Pukka: Each night, choose a player: they are poisoned until tomorrow night, then die. 
    You act on the first night.
    """

    def __init__(self):

        Character.__init__(self)
        BadMoonRising.__init__(self)
        Demon.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/9/90/Pukka_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Pukka"

        self._role_enum = BMRRole.pukka
        