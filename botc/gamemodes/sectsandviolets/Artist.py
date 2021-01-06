"""Contains the Artist Character class"""

import json
from botc import Character, Townsfolk
from ._utils import SectsAndViolets, SnVRole

with open('botc/gamemodes/sectsandviolets/character_text.json') as json_file:
    character_text = json.load(json_file)[SnVRole.artist.value.lower()]


class Artist(Townsfolk, SectsAndViolets, Character):
    """Artist: Once per game, during the day, privately ask the Storyteller any yes/no question.
    """

    def __init__(self):

        Character.__init__(self)
        SectsAndViolets.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "https://bloodontheclocktower.com/wiki/images/9/9f/Artist_Token.png"
        self._wiki_link = "https://bloodontheclocktower.com/wiki/Artist"

        self._role_enum = SnVRole.artist
