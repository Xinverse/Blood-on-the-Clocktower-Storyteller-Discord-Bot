"""Contains the Poisoner Character class"""

import json 
import discord
from botc import Minion, Character
from botc.BOTCUtils import GameLogic
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.poisoner.value.lower()]


class Poisoner(Minion, TroubleBrewing, Character):
    """Poisoner: Each night, choose a player, their ability malfunctions tonight and tomorrow day.

    ===== POISONER ===== 

    true_self = poisoner
    ego_self = poisoner
    social_self = poisoner

    commands:
    - poison <player>

    initialize setup? -> NO
    initialize role? -> NO

    override first night instruction? -> YES  # default is to send instruction string only
                                      => Send query for "poison" command
                                      => Send demon and minion identities to this minion if 7 players or more
    override regular night instruction -> YES  # default is to send nothing
                                       => Send query for "poison" command
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Minion.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/a/af/Poisoner_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Poisoner"

        self._role_enum = TBRole.poisoner
        self._emoji = "<:poisoner:722687671671193620>"
    
    async def send_first_night_instruction(self, recipient):
        """Send demon and minion list if there are 7 or more players. 
        Otherwise, send the default instruction string.
        """
        # Seven or more players, send the evil list
        if globvars.master_state.game.nb_players >= 7:
            msg1 = globvars.master_state.game.setup.create_evil_team_string()
            msg2 = self.emoji + " " + self.instruction
            msg = msg1 + msg2
            try:
                await recipient.send(msg)
            except discord.Forbidden:
                pass
        # Less than seven players, teensyville rules
        else:
            msg = self.emoji + " " + self.instruction
            try:
                await recipient.send(msg)
            except discord.Forbidden:
                pass
    
    async def send_regular_night_instruction(self, recipient):
        """Query the player for "poison" command"""
        
        msg = self.emoji + " " + self.instruction
        msg += "\n\n"
        msg += globvars.master_state.game.create_sitting_order_stats_string()
        try: 
            await recipient.send(msg)
        except discord.Forbidden:
            pass
    
    @GameLogic.changes_not_allowed
    @GameLogic.requires_one_target
    async def exec_poison(self, targets):
        """Poison command"""
        pass
