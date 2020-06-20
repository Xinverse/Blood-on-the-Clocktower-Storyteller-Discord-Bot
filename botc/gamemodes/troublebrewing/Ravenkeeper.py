"""Contains the Ravenkeeper Character class"""

import json 
from botc import Townsfolk, Character
from botc.BOTCUtils import GameLogic
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.ravenkeeper.value.lower()]


class Ravenkeeper(Townsfolk, TroubleBrewing, Character):
    """Ravenkeeper: If you die at night, you are woken to choose a player: you learn their character.

    ===== RAVENKEEPER ===== 

    true_self = ravenkeeper
    ego_self = ravenkeeper
    social_self = ravenkeeper

    commands:
    - learn <player>

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
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/45/Ravenkeeper_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Ravenkeeper"
        
        self._role_enum = TBRole.ravenkeeper
        self._emoji = "<:ravenkeeper:722686977295646731>"
    
    @GameLogic.changes_not_allowed
    @GameLogic.requires_one_target
    async def exec_learn(self, targets):
        """Learn command"""
        pass
        