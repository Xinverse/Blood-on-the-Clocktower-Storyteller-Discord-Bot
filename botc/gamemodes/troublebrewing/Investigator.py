"""Contains the Investigator Character class"""

import json 
import random
import discord
from botc import Townsfolk, Character, Category
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.investigator.value.lower()]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    investigator_init = strings["gameplay"]["investigator_init"]


class Investigator(Townsfolk, TroubleBrewing, Character):
    """Investigator: You start knowing 1 of 2 players is a particular Minion.

    ===== INVESTIGATOR ===== 

    true_self = investigator
    ego_self = investigator
    social_self = investigator

    commands:
    - None

    initialize setup? -> NO
    initialize role? -> NO

    override first night instruction? -> YES  # default is to send instruction string only
                                      => Send passive initial information
    override regular night instruction -> NO  # default is to send nothing
    """

    def __init__(self):

        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/e/ec/Investigator_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Investigator"

        self._role_enum = TBRole.investigator
        self._emoji = "<:investigator:722685830585384971>"
    
    async def send_first_night_instruction(self, recipient):
        """Send two possible minions"""

        # Choose the player that registers as minion
        minions = []
        for player in globvars.master_state.game.sitting_order:
            if player.role.social_self.category == Category.minion:
                minions.append(player)
        if minions:
            random.shuffle(minions)
            minion = minions.pop()
        else:
            minions = globvars.master_state.game.setup.minions
            minion = minions.pop()

        # Choose the other player
        other_possibilities = [player for player in globvars.master_state.game.sitting_order 
                               if player.user.id != minion.user.id]
        other = random.choice(other_possibilities)
        
        # Construct the message
        two_player_list = [minion, other]
        random.shuffle(two_player_list)
        msg = self.emoji + " " + self.instruction
        msg += "\n"
        msg += investigator_init.format(minion.role.social_self.name)
        msg += "```basic\n"
        msg += f"{two_player_list[0].user.display_name} ({two_player_list[0].user.id})\n"
        msg += f"{two_player_list[1].user.display_name} ({two_player_list[1].user.id})\n"
        msg += "```"

        try:
            await recipient.send(msg)
        except discord.Forbidden:
            pass

        globvars.logging.info(f">>> Investigator [send_first_night_instruction] Sent {minion} and {other}")
