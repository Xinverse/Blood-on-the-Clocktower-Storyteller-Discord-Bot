"""Contains the Philosopher Character class"""

import json
from botc import Character, Townsfolk
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.philosopher.value.lower()]


class Philosopher(Townsfolk, SectsAndViolets, Character):
    """Philosopher: Once per game, at night, choose a good character: become them. If you duplicate an in-play character, they are drunk.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "https://bloodontheclocktower.com/wiki/images/e/e6/Philosopher_Token.png"
        self._wiki_link = "https://bloodontheclocktower.com/wiki/Philosopher"

        self._role_enum = SnVRole.philosopher
