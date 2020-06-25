"""Contains the Monk Character class"""

import json 
import discord
from botc import Townsfolk, Character
from botc.BOTCUtils import GameLogic
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.monk.value.lower()]


class Monk(Townsfolk, TroubleBrewing, Character):
    """Monk: Each night*, choose a player (not yourself): they are safe from the Demon tonight.

    ===== MONK ===== 

    true_self = monk
    ego_self = monk
    social_self = monk

    commands:
    - protect <player>

    initialize setup? -> NO
    initialize role? -> NO

    ----- First night
    START:
    override first night instruction? -> NO  # default is to send instruction string only

    ----- Regular night
    START:
    override regular night instruction -> YES  # default is to send nothing
                                       => Send query for "protect" command                              
    """
    
    def __init__(self):

        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        self._brief_string = character_text["brief"]
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/1/1b/Monk_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Monk"

        self._role_enum = TBRole.monk
        self._emoji = "<:monk:722687015560151050>"

    async def send_regular_night_instruction(self, recipient):
        """Query the player for "protect" command"""
        
        msg = self.instruction
        msg += "\n\n"
        msg += globvars.master_state.game.create_sitting_order_stats_string()
        try: 
            await recipient.send(msg)
        except discord.Forbidden:
            pass
    
    @GameLogic.changes_not_allowed
    @GameLogic.requires_one_target
    @GameLogic.except_first_night
    @GameLogic.no_self_targetting
    async def register_protect(self, player, targets):
        """Protect command"""
        pass
