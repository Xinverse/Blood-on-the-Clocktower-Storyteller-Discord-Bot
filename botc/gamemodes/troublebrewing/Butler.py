"""Contains the Butler Character class"""

import json 
from botc import Outsider, Character
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.butler.value.lower()]


class Butler(Outsider, TroubleBrewing, Character):
    """Butler: Each night, choose a player (not yourself): tomorrow, you may only vote if 
    they are voting too.

    ===== BUTLER ===== 

    true_self = butler
    ego_self = butler
    social_self = butler
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Outsider.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/1/1a/Butler_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Butler"

        self._role_enum = TBRole.butler
    