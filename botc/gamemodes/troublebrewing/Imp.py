"""Contains the Imp Character class"""

import json
import discord
import random
from botc import Demon, Townsfolk, Outsider, Character
from botc.BOTCUtils import GameLogic, BOTCUtils
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.imp.value.lower()]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    demon_bluff_str = strings["gameplay"]["demonbluffs"]


class Imp(Demon, TroubleBrewing, Character):
    """Imp: Each night*, choose a player: they die. If you kill yourself this way, 
    a Minion becomes the Imp.

    ===== IMP ===== 

    true_self = imp
    ego_self = imp
    social_self = imp

    commands:
    - kill <player>

    initialize setup? -> NO
    initialize role? -> NO

    override first night instruction? -> YES  # default is to send instruction string only
                                      => Send 3 demon bluffs
                                      => Send demon and minion identities to this minion if 7 players or more
    override regular night instruction -> YES  # default is to send nothing
                                      => Send query for "kill" command
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
    
    async def send_first_night_instruction(self, recipient):
        """Send demon and minion list if there are 7 or more players, as well as 3 bluffs.
        Otherwise, send the default instruction string.
        """
        # Seven or more players, send the evil list and three demon bluffs
        if globvars.master_state.game.nb_players >= 7:
            
            # 3 demon bluffs: 2 townsfolk characters + 1 outsider character
            # Exclusing all characters taken by other players, as well as the drunk's ego_self
            all_townsfolks = BOTCUtils.get_role_list(TroubleBrewing, Townsfolk)
            all_outsiders = BOTCUtils.get_role_list(TroubleBrewing, Outsider)
            taken_townsfolks = [player.role.name for player in globvars.master_state.game.setup.townsfolks]
            taken_outsiders = [player.role.name for player in globvars.master_state.game.setup.outsiders]

            possible_townsfolk_bluffs = [character for character in all_townsfolks 
                                         if character.name not in taken_townsfolks]
            possible_outsider_bluffs = [character for character in all_outsiders 
                                        if character.name not in taken_outsiders]
            random.shuffle(possible_townsfolk_bluffs)
            random.shuffle(possible_outsider_bluffs)

            bluff_1 = possible_townsfolk_bluffs.pop()
            bluff_2 = possible_townsfolk_bluffs.pop()
            bluff_3 = possible_outsider_bluffs.pop()

            msg1 = demon_bluff_str.format(bluff_1.name, bluff_2.name, bluff_3.name) + "\n"
            msg2 = globvars.master_state.game.setup.create_evil_team_string()
            msg3 = self.emoji + " " + self.instruction
            msg = msg1 + msg2 + msg3
            
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
        """Query the player for "kill" command"""
        
        msg = self.emoji + " " + self.instruction
        msg += "\n\n"
        msg += globvars.master_state.game.create_sitting_order_stats_string()
        try: 
            await recipient.send(msg)
        except discord.Forbidden:
            pass
    
    @GameLogic.changes_not_allowed
    @GameLogic.requires_two_targets
    async def exec_kill(self, targets):
        """Kill command"""
        pass
