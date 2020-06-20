"""Contains the Soldier Character class"""

import json 
from botc import Townsfolk, Character
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.soldier.value.lower()]


class Soldier(Townsfolk, TroubleBrewing, Character):
    """Soldier: You are safe from the Demon.

    ===== SOLDIER ===== 

    true_self = soldier
    ego_self = soldier
    social_self = soldier

    commands:
    - None

    initialize setup? -> NO
    initialize role? -> NO

    override first night instruction? -> NO  # default is to send instruction string only
    override regular night instruction -> NO  # default is to send nothing
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/9/9e/Soldier_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Soldier"

        self._role_enum = TBRole.soldier
        self._emoji = "<:soldier:722687220841971753>"
