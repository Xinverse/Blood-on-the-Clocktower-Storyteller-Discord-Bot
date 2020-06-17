"""Contains the Imp Character class"""

import json 
from botc import Demon, Character
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.imp.value.lower()]


class Imp(Demon, TroubleBrewing, Character):
    """Imp: Each night*, choose a player: they die. If you kill yourself this way, 
    a Minion becomes the Imp.

    ===== IMP ===== 

    true_self = imp
    ego_self = imp
    social_self = imp

    commands:
    - kill <player>

    send first night instruction? -> FALSE
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Demon.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/42/Imp_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Imp"

        self._role_enum = TBRole.imp
        self._emoji = "<:imp2:722687671377330197>"
