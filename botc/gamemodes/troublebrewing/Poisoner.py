"""Contains the Poisoner Character class"""

import json 
import discord
from botc import Minion, Character
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

    send first night instruction? -> TRUE (demon identity)
    send regular night instruction -> TRUE (query for "poison" command)
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
    
    async def send_regular_night_instruction(self, recipient):
        """Query the player for "poison" command"""
        
        msg = self.instruction
        msg += "\n\n"
        msg += globvars.master_state.game.create_sitting_order_stats_string()
        try: 
            await recipient.send(msg)
        except discord.Forbidden:
            pass
