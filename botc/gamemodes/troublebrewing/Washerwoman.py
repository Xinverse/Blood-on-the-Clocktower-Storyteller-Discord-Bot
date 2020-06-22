"""Contains the Washerwoman Character class"""

import json 
import discord
import random
from botc import Townsfolk, Character, Category
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.washerwoman.value.lower()]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    washerwoman_init = strings["gameplay"]["washerwoman_init"]


class Washerwoman(Townsfolk, TroubleBrewing, Character):
    """Washerwoman: You start knowing 1 of 2 players is a particular Townsfolk.

    ===== WASHERWOMAN ===== 

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
                                      => Send passive initial information

    ----- Regular night
    START:
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
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/4d/Washerwoman_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Washerwoman"

        self._role_enum = TBRole.washerwoman
        self._emoji = "<:washerwoman:722684124820668447>"
    
    async def send_first_night_instruction(self, recipient):
        """Send two possible townsfolks"""

        # First set the social self
        for player in globvars.master_state.game.sitting_order:
            player.role.set_new_social_self()

        # Choose the player that registers as minion
        townsfolks = []
        for player in globvars.master_state.game.sitting_order:
            if player.role.social_self.category == Category.townsfolk:
                townsfolks.append(player)
        random.shuffle(townsfolks)
        townsfolk = townsfolks.pop()

        # Choose the other player
        other_possibilities = [player for player in globvars.master_state.game.sitting_order 
                               if player.user.id != townsfolk.user.id]
        other = random.choice(other_possibilities)
        
        # Construct the message
        two_player_list = [townsfolk, other]
        random.shuffle(two_player_list)
        msg = self.emoji + " " + self.instruction
        msg += "\n"
        msg += washerwoman_init.format(townsfolk.role.social_self.name)
        msg += "```basic\n"
        msg += f"{two_player_list[0].user.display_name} ({two_player_list[0].user.id})\n"
        msg += f"{two_player_list[1].user.display_name} ({two_player_list[1].user.id})\n"
        msg += "```"

        try:
            await recipient.send(msg)
        except discord.Forbidden:
            pass

        globvars.logging.info(f">>> Washerwoman [send_first_night_instruction] Sent {townsfolk} and {other}")
