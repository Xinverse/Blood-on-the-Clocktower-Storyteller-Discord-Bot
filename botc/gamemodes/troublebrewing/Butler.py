"""Contains the Butler Character class"""

import json 
import botutils
import discord
from botc.BOTCUtils import GameLogic
from botc import Outsider, Character
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.butler.value.lower()]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    target_nb = strings["cmd_warnings"]["target_nb"]
    x_emoji = strings["cmd_warnings"]["x_emoji"]


class Butler(Outsider, TroubleBrewing, Character):
    """Butler: Each night, choose a player (not yourself): tomorrow, you may only vote if 
    they are voting too.

    ===== BUTLER ===== 

    true_self = butler
    ego_self = butler
    social_self = butler

    commands
    - serve <player>

    initialize setup? -> NO
    initialize role? -> NO

    ----- First night
    START:
    override first night instruction? -> YES  # default is to send instruction string only
                                      => Send query for "serve" command

    ----- Regular night
    START:
    override regular night instruction? -> YES  # default is to send nothing
                                        => Send query for "serve" command
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
        self._emoji = "<:butler:722687426421719050>"

    async def send_first_night_instruction(self, recipient):
        """Query the player for "serve" command"""
        
        msg = self.emoji + " " + self.instruction
        msg += "\n\n"
        msg += globvars.master_state.game.create_sitting_order_stats_string()
        try: 
            await recipient.send(msg)
        except discord.Forbidden:
            pass
    
    async def send_regular_night_instruction(self, recipient):
        """Query the player for "serve" command"""
        
        msg = self.emoji + " " + self.instruction
        msg += "\n\n"
        msg += globvars.master_state.game.create_sitting_order_stats_string()
        try: 
            await recipient.send(msg)
        except discord.Forbidden:
            pass
    
    @GameLogic.changes_not_allowed
    @GameLogic.requires_one_target
    async def register_serve(self, player, targets):
        """Serve command registration"""
        pass
