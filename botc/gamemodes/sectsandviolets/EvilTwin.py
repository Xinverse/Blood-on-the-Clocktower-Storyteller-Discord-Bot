"""Contains the Evil Twin Character class"""

import json
from botc import Character, Minion
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.eviltwin.value.lower()]


class EvilTwin(Minion, SectsAndViolets, Character):
    """Evil Twin: You & an opposing player know each other. If the good player is executed, evil wins. Good can't win if you both live.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Minion.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/2/24/Evil_Twin_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Evil_Twin"

        self._role_enum = SnVRole.eviltwin
