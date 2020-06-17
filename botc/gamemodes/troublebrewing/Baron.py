"""Contains the Baron Character class"""

import json
import random
import discord
from botc import BOTCUtils
from botc import Minion, Character
from botc.Outsider import Outsider
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.baron.value.lower()]

with open('botc/game_text.json') as json_file:
    strings = json.load(json_file)
    evilteammates = strings["gameplay"]["evilteammates"]


class Baron(Minion, TroubleBrewing, Character):
    """Baron: There are extra Outsiders in play [+2 Outsiders]

    ===== BARON ===== 

    true_self = baron
    ego_self = baron
    social_self = baron

    commands
    - None

    override first night instruction? -> YES  # default is to send instruction string only
                                      => Send demon and minion identities to this minion if 7 players or more
    override regular night instruction -> NO  # default is to send nothing
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Minion.__init__(self)  

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/b/ba/Baron_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Baron"

        self._role_enum = TBRole.baron
        self._emoji = "<:baron:722687671499227167>"
    
    def exec_init_setup(self, townsfolk_obj_list, outsider_obj_list, minion_obj_list, demon_obj_list):
        """Add two outsiders to the setup, remove two townsfolks from the setup"""

        random.shuffle(townsfolk_obj_list)
        townsfolk_obj_list.pop()
        townsfolk_obj_list.pop()
        tb_outsider_all = BOTCUtils.get_role_list(TroubleBrewing, Outsider)
        random.shuffle(tb_outsider_all)

        count = 0

        for outsider in tb_outsider_all:
            if count >= 2:
                break
            else:
                if str(outsider) not in [str(role) for role in outsider_obj_list]:
                    outsider_obj_list.append(outsider)
                    count += 1

        return [townsfolk_obj_list, outsider_obj_list, minion_obj_list, demon_obj_list]
    
    async def send_first_night_instruction(self, recipient):
        """Send demon and minion list if there are 7 or more players. 
        Otherwise, send the default instruction string.
        """
        if globvars.master_state.game.nb_players >= 7:
            msg1 = self._demon_head_emoji + " " + evilteammates
            msg2 = self.emoji + " " + self.instruction
            msg = msg1 + msg2
            try:
                await recipient.send(msg)
            except discord.Forbidden:
                pass
        else:
            msg = self.emoji + " " + self.instruction
            try:
                await recipient.send(msg)
            except discord.Forbidden:
                pass
