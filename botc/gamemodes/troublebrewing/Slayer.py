"""Contains the Slayer Character class"""

import json 
from botc import Townsfolk, Character
from botc.BOTCUtils import GameLogic
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.slayer.value.lower()]   


class Slayer(Townsfolk, TroubleBrewing, Character):
    """Slayer: Once per game, during the day, publicly choose a player: if they are the Demon, they die.

    ===== SLAYER ===== 

    true_self = slayer
    ego_self = slayer
    social_self = slayer

    commands:
    - slay <player>

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
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/2/2f/Slayer_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Slayer"

        self._role_enum = TBRole.slayer
        self._emoji = "<:slayer:722687329050820648>"
    
    @GameLogic.changes_not_allowed
    @GameLogic.unique_ability
    @GameLogic.requires_one_target
    async def exec_slay(self, targets):
        """Slay command"""
        pass

