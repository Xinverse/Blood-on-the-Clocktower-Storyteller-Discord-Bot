"""Contains the Chef Character class"""

import json 
import discord
import datetime
import random
from botc import Townsfolk, Character, BOTCUtils
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.chef.value.lower()]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    chef_init = strings["gameplay"]["chef_init"]
    copyrights_str = strings["misc"]["copyrights"]


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
        self._action = character_text["action"]
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/4c/Chef_Token.png"
        self._art_link_cropped = "https://imgur.com/m2Wjejh.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Chef"

        self._role_enum = TBRole.chef
        self._emoji = "<:chef:722686296073699388>"

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
    
    def __create_droisoned_info(self):
        """Create drunk/poisoned information for the n1 chef info"""

        import globvars
        total_nb_evils = len(globvars.master_state.game.setup.minions) + \
            len(globvars.master_state.game.setup.demon)
        possibilities = range(total_nb_evils)
        ret = random.choice(possibilities)
        return ret
    
    async def send_n1_end_message(self, recipient):
        """Send the number of pairs of evils sitting together."""

        from botc.BOTCUtils import get_number_image

        player = BOTCUtils.get_player_from_id(recipient.id)
        if player.is_droisoned():
            evil_pair_count = self.__create_droisoned_info()
        else:
            evil_pair_count = self.get_nb_pairs_of_evils()
        link = get_number_image(evil_pair_count)

        msg = f"***{recipient.name}#{recipient.discriminator}***, the **{self.name}**:"
        msg += "\n"
        msg += self.emoji + " " + self.instruction
        msg += "\n"
        msg += chef_init.format(evil_pair_count)

        embed = discord.Embed(description = msg)
        embed.set_thumbnail(url = link)
        embed.set_footer(text = copyrights_str)
        embed.timestamp = datetime.datetime.utcnow()

        try:
            await recipient.send(embed = embed)
        except discord.Forbidden:
            pass
    
    def get_nb_pairs_of_evils(self):
        """Get the number of pairs of evils sitting together."""

        import globvars

        # We initialize what their social self is going to be for this round of inspection
        for player in globvars.master_state.game.sitting_order:
            player.role.set_new_social_self(player)

        # Make a list of all pairs in the sitting order
        total = len(globvars.master_state.game.sitting_order)
        all_pairs = [
            (
                globvars.master_state.game.sitting_order[i], 
                globvars.master_state.game.sitting_order[(i+1)%total]
            ) 
            for i in range(total)
        ]

        # Count the evil pairs
        evil_pair_count = 0
        for pair in all_pairs:
            if pair[0].role.social_self.is_evil() and pair[1].role.social_self.is_evil():
                evil_pair_count += 1
        
        log_msg = f">>> Chef: {evil_pair_count} pairs of evils"
        globvars.logging.info(log_msg)

        return evil_pair_count
