"""Contains the Scarlet Woman Character class"""

import json 
import discord
from botc import Minion, Character
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.scarletwoman.value.lower()]

class ScarletWoman(Minion, TroubleBrewing, Character):
    """Scarlet Woman: If there are 5 or more players alive & the Demon dies, you become the Demon.

    ===== SCARLET WASHERWOMAN ===== 

    true_self = washerwoman
    ego_self = washerwoman
    social_self = washerwoman

    commands:
    - None

    initialize setup? -> NO
    initialize role? -> NO

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
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/7/7c/Scarlet_Woman_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Scarlet_Woman"

        self._role_enum = TBRole.scarletwoman
        self._emoji = "<:scarletwoman:722687671847092225>"
    
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
