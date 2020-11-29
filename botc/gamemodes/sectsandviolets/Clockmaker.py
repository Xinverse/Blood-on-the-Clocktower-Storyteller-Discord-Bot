"""Contains the Clockmaker Character class"""

import json
from botc import Character, Townsfolk
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.clockmaker.value.lower()]


class Clockmaker(Townsfolk, SectsAndViolets, Character):
    """Clockmaker: You start knowing how many steps from the Demon to nearest Minion.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "https://bloodontheclocktower.com/wiki/images/4/4b/Clockmaker_Token.png"
        self._wiki_link = "https://bloodontheclocktower.com/wiki/Clockmaker"

        self._role_enum = SnVRole.clockmaker
