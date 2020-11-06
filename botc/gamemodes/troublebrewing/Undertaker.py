"""Contains the Undertaker Character class"""

import discord
import datetime
import json 
import random
from botc import Townsfolk, Character, NonRecurringAction, BOTCUtils, Townsfolk, \
    Outsider, Minion, Demon
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.undertaker.value.lower()]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    undertaker_nightly = strings["gameplay"]["undertaker_nightly"]
    undertaker_none = strings["gameplay"]["undertaker_none"]
    copyrights_str = strings["misc"]["copyrights"]


class Undertaker(Townsfolk, TroubleBrewing, Character, NonRecurringAction):
    """Undertaker: Each night, you learn which character died by execution today.

    ===== UNDERTAKER ===== 

    true_self = undertaker
    ego_self = undertaker
    social_self = undertaker

    commands:
    - None

    initialize setup? -> NO
    initialize role? -> NO

    ----- First night
    START:
    override first night instruction? -> NO  # default is to send instruction string only

    ----- Regular night
    START:
    override regular night instruction -> YES  # default is to send nothing
                                       => Send passive nightly information
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
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/f/fe/Undertaker_Token.png"
        self._art_link_cropped = "https://imgur.com/3CpqHsL.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Undertaker"

        self._role_enum = TBRole.undertaker
        self._emoji = "<:tbundertaker:739317350553092136>"

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
        """Create drunk/poisoned information for the undertaker info"""

        import globvars
        executed_player = globvars.master_state.game.today_executed_player

        # If someone has been executed
        if executed_player:

            tb_townsfolk_all = BOTCUtils.get_role_list(TroubleBrewing, Townsfolk)
            tb_outsider_all = BOTCUtils.get_role_list(TroubleBrewing, Outsider)
            tb_minion_all = BOTCUtils.get_role_list(TroubleBrewing, Minion)
            tb_demon_all = BOTCUtils.get_role_list(TroubleBrewing, Demon)

            executed_player.role.set_new_social_self(executed_player)

            # The executed player has a good role. The droisoned undertaker will see a 
            # bad role.
            if executed_player.role.social_self.is_good():
                pool = tb_minion_all + tb_demon_all
                ret = random.choice(pool)
                return ret
                
            # The executed player has a bad role. The droisoned undertaker will see 
            # a good role.
            else:
                pool = tb_townsfolk_all + tb_outsider_all
                pool = [character for character in pool if character.name != Undertaker().name]
                ret = random.choice(pool)
                return ret

        # If no one is executed, then send none
        else:
            return None
    
    async def send_n1_end_message(self, recipient):
        """Send the character of the executed player today."""
        await self.send_regular_night_end_dm(recipient)
    
    async def send_regular_night_end_dm(self, recipient):
        """Send the character of the executed player today."""

        player = BOTCUtils.get_player_from_id(recipient.id)

        # Dead players do not receive anything
        if not player.is_alive():
            return 

        # Poisoned info
        if player.is_droisoned():
            character_of_executed = self.__create_droisoned_info()
        else:
            import globvars
            executed_player = globvars.master_state.game.today_executed_player
            if executed_player:
                executed_player.role.set_new_social_self(executed_player)
                character_of_executed = executed_player.role.social_self
            else:
                character_of_executed = None
        
        msg = f"***{recipient.name}#{recipient.discriminator}***, the **{self.name}**:"
        msg += "\n"
        msg += self.emoji + " " + self.instruction
        msg += "\n"

        if character_of_executed:
            msg += undertaker_nightly.format(character_of_executed.name)
        else:
            msg += undertaker_none

        embed = discord.Embed(description = msg)

        if character_of_executed:
            embed.set_thumbnail(url = character_of_executed._art_link_cropped)     
            
        embed.set_footer(text = copyrights_str)
        embed.timestamp = datetime.datetime.utcnow()

        try:
            await recipient.send(embed = embed)
        except discord.Forbidden:
            pass
