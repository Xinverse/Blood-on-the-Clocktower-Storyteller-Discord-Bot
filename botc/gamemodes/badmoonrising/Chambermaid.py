"""Contains the Chambermaid Character class"""

import json
from botc import Character, Townsfolk
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.chambermaid.value.lower()]


class Chambermaid(Townsfolk, BadMoonRising, Character):
    """Chambermaid Each night, choose 2 alive players (not yourself): you learn how many woke 
    tonight due to their ability.
    """

    def __init__(self):

        Character.__init__(self)
        BadMoonRising.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        self._brief_string = character_text["brief"]
        self._action = character_text["action"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/8/87/Chambermaid_Token.png"
        self._art_link_cropped = "https://imgur.com/eNn6hQa.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Chambermaid"

        self._role_enum = BMRRole.chambermaid
        self._emoji = "<:bmrchambermaid:781151556053499925>"
