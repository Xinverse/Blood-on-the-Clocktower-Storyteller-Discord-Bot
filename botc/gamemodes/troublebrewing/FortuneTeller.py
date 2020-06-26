"""Contains the Fortune Teller Character class"""

import json
import random
import discord 
from botc import Townsfolk, Character, Storyteller, RedHerring
from botc.BOTCUtils import GameLogic
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.fortuneteller.value.lower()]


class FortuneTeller(Townsfolk, TroubleBrewing, Character):
    """Fortune Teller: Each night, choose 2 players: you learn if either is a Demon. 
    There is 1 good player that registers falsely to you.

    ===== FORTUNE TELLER ===== 

    true_self = fortune teller
    ego_self = fortune teller
    social_self = fortune teller

    commands:
    - read <player> and <player>

    initialize setup? -> NO
    initialize role? -> YES

    ----- First night
    START:
    override first night instruction? -> YES  # default is to send instruction string only
                                      => Send query for "read" command

    ----- Regular night
    START:
    override regular night instruction? -> YES  # default is to send nothing
                                        => Send query for "read" command
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
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/3/3a/Fortune_Teller_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Fortune_Teller"

        self._role_enum = TBRole.fortuneteller
        self._emoji = "<:fortuneteller:722687043666313218>"

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
        """Send query for "read" command."""

        msg = self.emoji + " " + self.instruction
        msg += "\n\n"
        msg += globvars.master_state.game.create_sitting_order_stats_string()
        try: 
            await recipient.send(msg)
        except discord.Forbidden:
            pass
    
    async def send_regular_night_instruction(self, recipient):
        """Send query for "read" command."""

        msg = self.emoji + " " + self.instruction
        msg += "\n\n"
        msg += globvars.master_state.game.create_sitting_order_stats_string()
        try: 
            await recipient.send(msg)
        except discord.Forbidden:
            pass
    
    def exec_init_role(self, setup):
        """Assign one of the townsfolks or outsiders as a red herring"""
        possibilities = setup.townsfolks + setup.outsiders
        chosen = random.choice(possibilities)
        chosen.add_status_effect(RedHerring(Storyteller(), chosen))
        globvars.logging.info(f">>> Fortune Teller [exec_init_role] Set red herring to {str(chosen)}")

    @GameLogic.changes_not_allowed
    @GameLogic.requires_two_targets
    async def register_read(self, player, targets):
        """Read command"""
        pass
