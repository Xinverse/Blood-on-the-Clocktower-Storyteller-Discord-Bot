"""Contains the Virgin Character class"""

import json 
from botc import Townsfolk, Character
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.virgin.value.lower()]


class Virgin(Townsfolk, TroubleBrewing, Character):
    """Virgin: The 1st time you are nominated, if the nominator is a Townsfolk, 
    they are executed immediately.

    ===== VIRGIN ===== 

    true_self = virgin
    ego_self = virgin
    social_self = virgin

    commands:
    - None

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
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/5/5e/Virgin_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Virgin"

        self._role_enum = TBRole.virgin
        self._emoji = "<:virgin:722687299363667988>"
