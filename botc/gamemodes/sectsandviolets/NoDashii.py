"""Contains the No Dashii Character class"""

import json
from botc import Character, Demon
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.nodashii.value.lower()]


class NoDashii(Demon, SectsAndViolets, Character):
    """No Dashii: Each night*, choose a player: they die. Your 2 Townsfolk neighbors are poisoned.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Demon.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/f/f4/No_Dashii_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/No_Dashii"

        self._role_enum = SnVRole.nodashii
