"""Contains the Scarlet Woman Character class"""

import json 
import discord
from botc import Minion, Character, NonRecurringAction
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.scarletwoman.value.lower()]

class ScarletWoman(Minion, TroubleBrewing, Character, NonRecurringAction):
    """Scarlet Woman: If there are 5 or more players alive & the Demon dies, you become the Demon.

    ===== SCARLET WASHERWOMAN ===== 

    true_self = washerwoman
    ego_self = washerwoman
    social_self = washerwoman

    commands:
    - None

    initialize setup? -> NO
    initialize role? -> NO

    ----- First night
    START:
    override first night instruction? -> YES  # default is to send instruction string only
                                      => Send demon and minion identities to this minion 
                                         if 7 players or more

    ----- Regular night
    START:
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
        self._brief_string = character_text["brief"]
        self._action = character_text["action"]
        
        self._art_link = "https://bloodontheclocktower.com/wiki/images/7/7c/Scarlet_Woman_Token.png"
        self._art_link_cropped = "https://imgur.com/qgvpSOJ.png"
        self._wiki_link = "https://bloodontheclocktower.com/wiki/Scarlet_Woman"

        self._role_enum = TBRole.scarletwoman
        self._emoji = "<:tbscarletwoman:739317351110934558>"
    
    def exec_init_setup(self, townsfolk_obj_list, outsider_obj_list, minion_obj_list, demon_obj_list):
        """The scarlet woman has a lower chance of appearing at 6p or less"""

        random.shuffle(townsfolk_obj_list)

        # Remove two townsfolks
        townsfolk_obj_list.pop()
        townsfolk_obj_list.pop()

        # If the single remaining townsfolk is a washerwoman, then remove it
        if len(townsfolk_obj_list) == 1:
            if townsfolk_obj_list[0].name == TBRole.washerwoman.value:
                tb_townsfolk_all = BOTCUtils.get_role_list(TroubleBrewing, Townsfolk)
                all_not_washer = [character for character in tb_townsfolk_all if character.name != TBRole.washerwoman.value]
                townsfolk_obj_list = [random.choice(all_not_washer)]

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

    def create_n1_instr_str(self):
        """Create the instruction field on the opening dm card"""

        # First line is the character instruction string
        msg = f"{self.emoji} {self.instruction}"
        addendum = character_text["n1_addendum"]
        
        # Some characters have a line of addendum
        if addendum:
            with open("botutils/bot_text.json") as json_file:
                bot_text = json.load(json_file)
                scroll_emoji = bot_text["esthetics"]["scroll"]
            msg += f"\n{scroll_emoji} {addendum}"
            
        return msg
    
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
