"""Contains the Mutant Character class"""

import json
from botc import Character, Outsider
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.mutant.value.lower()]


class Mutant(Outsider, SectsAndViolets, Character):
    """Mutant: If you are "mad" about being an Outsider, you might be executed.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Outsider.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/3/30/Mutant_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Mutant"

        self._role_enum = SnVRole.mutant
