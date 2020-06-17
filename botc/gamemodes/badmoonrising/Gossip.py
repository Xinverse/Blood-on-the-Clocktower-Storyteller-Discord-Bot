"""Contains the Gossip Character class"""

import json
from botc import Character, Townsfolk
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.gossip.value.lower()]


class Gossip(Townsfolk, BadMoonRising, Character):
    """Gossip: Each day, you may make a public statement. Tonight, if it was true, a player dies.
    """

    def __init__(self):

        Character.__init__(self)
        BadMoonRising.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/b/b8/Gossip_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Gossip"

        self._role_enum = BMRRole.gossip
        