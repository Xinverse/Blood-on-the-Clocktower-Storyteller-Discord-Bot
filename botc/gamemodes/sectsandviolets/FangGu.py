"""Contains the Fang Gu Character class"""

import json
from botc import Character, Demon
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.fanggu.value.lower()]


class FangGu(Demon, SectsAndViolets, Character):
    """Fang Gu: Each night*, choose a player: they die. The 1st Outsider chosen becomes an evil Fang Gu & you die instead. [+1 Outsider]
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Demon.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/e/e6/Fang_Gu_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Fang_Gu"

        self._role_enum = SnVRole.fanggu
