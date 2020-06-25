"""Contains the Chef Character class"""

import json 
import discord
from botc import Townsfolk, Character
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.chef.value.lower()]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    chef_init = strings["gameplay"]["chef_init"]


class Chef(Townsfolk, TroubleBrewing, Character):
    """Chef: You start knowing how many pairs of evil players there are.

    ===== CHEF ===== 

    true_self = chef
    ego_self = chef
    social_self = chef

    commands:
    - None

    initialize setup? -> NO
    initialize role? -> NO

    ----- First night
    START:
    override first night instruction? -> YES  # default is to send instruction string only
                                      => Send passive initial information

    ----- Regular night
    START:
    override regular night instruction? -> NO  # default is to send nothing
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
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/4c/Chef_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Chef"

        self._role_enum = TBRole.chef
        self._emoji = "<:chef:722686296073699388>"
    
    async def send_first_night_instruction(self, recipient):
        """Send the number of pairs of evils sitting together."""
        import globvars
        # We initialize what their social self is going to be for this round of inspection
        for player in globvars.master_state.game.sitting_order:
            player.role.set_new_social_self()
        # Make a list of all pairs in the sitting order
        total = len(globvars.master_state.game.sitting_order)
        all_pairs = [
            (globvars.master_state.game.sitting_order[i], globvars.master_state.game.sitting_order[(i+1)%total]) 
            for i in range(total)
        ]
        # Count the evil pairs
        evil_pair_count = 0
        for pair in all_pairs:
            if pair[0].role.social_self.is_evil() and pair[1].role.social_self.is_evil():
                evil_pair_count += 1
        # Send the info
        msg = self.emoji + " " + self.instruction
        msg += "\n"
        msg += chef_init.format(evil_pair_count)
        try:
            await recipient.send(msg)
        except discord.Forbidden:
            pass
        log_msg = f">>> Chef [send_first_night_instruction] {evil_pair_count} pairs of evils"
        globvars.logging.info(log_msg)
