"""Contains the Snake Charmer Character class"""

import json
from botc import Character, Townsfolk
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.snakecharmer.value.lower()]


class SnakeCharmer(Townsfolk, SectsAndViolets, Character):
    """Snake Charmer: Each night, choose an alive player: a chosen Demon swaps characters & alignments with you & is then poisoned.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/6/65/Snake_Charmer_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Snake_Charmer"

        self._role_enum = SnVRole.snakecharmer
