"""Contains the Investigator Character class"""

import json 
import random
import datetime
import discord
from botc import Townsfolk, Character, Category
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.investigator.value.lower()]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    investigator_init = strings["gameplay"]["investigator_init"]
    copyrights_str = strings["misc"]["copyrights"]


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
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/e/ec/Investigator_Token.png"
        self._art_link_cropped = "https://imgur.com/9B2WNCc.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Investigator"

        self._role_enum = TBRole.investigator
        self._emoji = "<:investigator:722685830585384971>"

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
    
    async def send_n1_end_message(self, recipient):
        """Send the number of pairs of evils sitting together."""

        # We have a list of two players
        two_player_list = self.get_two_possible_minions()
        registered_minion_type = two_player_list[2]
        link = registered_minion_type.art_link
        assert registered_minion_type.category == Category.minion, "Investigator did not receive a minion character"

        # Get rid of the last element (the minion type)
        two_player_list.pop()

        # Construct the message to send
        msg = f"***{recipient.name}{recipient.discriminator}***, the **{self.name}**:"
        msg += "\n"
        msg += self.emoji + " " + self.instruction
        msg += "\n"
        msg += investigator_init.format(registered_minion_type.name)
        msg += "```basic\n"
        msg += f"{two_player_list[0].user.display_name} ({two_player_list[0].user.id})\n"
        msg += f"{two_player_list[1].user.display_name} ({two_player_list[1].user.id})\n"
        msg += "```"

        embed = discord.Embed(description = msg)
        embed.set_thumbnail(url = link)
        embed.set_footer(text = copyrights_str)
        embed.timestamp = datetime.datetime.utcnow()

        try:
            await recipient.send(embed = embed)
        except discord.Forbidden:
            pass
    
    def get_two_possible_minions(self):
        """Send two possible minions"""

        # First set the social self
        for player in globvars.master_state.game.sitting_order:
            player.role.set_new_social_self()

        # Choose the player that registers as minion
        minions = []
        registered_minion_type = None
        for player in globvars.master_state.game.sitting_order:
            if player.role.social_self.category == Category.minion:
                minions.append(player)

        # If we found a minion
        if minions:
            random.shuffle(minions)
            minion = minions.pop()
            registered_minion_type = minion.role.social_self

        # No minion found through social self: meaning that some registered as townsfolks.
        else:
            minions = globvars.master_state.game.setup.minions
            minion = minions.pop()
            registered_minion_type = minion.role.true_self

        # Choose the other player
        other_possibilities = [player for player in globvars.master_state.game.sitting_order 
                               if player.user.id != minion.user.id]
        other = random.choice(other_possibilities)
        
        # Construct the message
        two_player_list = [minion, other]
        random.shuffle(two_player_list)
        two_player_list.append(registered_minion_type)

        globvars.logging.info(f">>> Investigator: Sent {minion} and {other} as {registered_minion_type}")

        return two_player_list
