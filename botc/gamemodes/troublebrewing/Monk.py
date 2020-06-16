"""Contains the Monk Character class"""

import json 
from botc import Townsfolk, Character
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.monk.value.lower()]


class Monk(Townsfolk, TroubleBrewing, Character):
    """Monk: Each night*, choose a player (not yourself): they are safe from the Demon tonight.

    ===== MONK ===== 

    true_self = monk
    ego_self = monk
    social_self = monk

    commands:
    - protect

    send first night instruction? -> FALSE
    """
    
    def __init__(self):

        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/1/1b/Monk_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Monk"

        self._role_enum = TBRole.monk
