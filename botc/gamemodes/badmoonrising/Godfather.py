"""Contains the Godfather Character class"""

import json
from botc import Character, Minion
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.godfather.value.lower()]


class Godfather(Minion, BadMoonRising, Character):
    """Godfather: You start knowing which Outsiders are in-play. If 1 died today, 
    choose a player tonight: they die. [-1 or +1 Outsider]
    """

    def __init__(self):

        Character.__init__(self)
        BadMoonRising.__init__(self)
        Minion.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        self._brief_string = character_text["brief"]
        self._action = character_text["action"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/e/ef/Godfather_Token.png"
        self._art_link_cropped = "https://imgur.com/7JlfMLc.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Godfather"

        self._role_enum = BMRRole.godfather
        self._emoji = "<:bmrgodfather:781151556204625930>"
