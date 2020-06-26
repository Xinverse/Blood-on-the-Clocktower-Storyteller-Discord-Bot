"""Contains the Librarian Character class"""

import json
import discord
import random
from botc import Townsfolk, Character, Category
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.librarian.value.lower()]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    librarian_init = strings["gameplay"]["librarian_init"]
    librarian_init_zero = strings["gameplay"]["librarian_init_zero"]


class Librarian(Townsfolk, TroubleBrewing, Character):
    """Librarian: You start knowing that 1 of 2 players is a particular Outsider.
    (Or that zero are in play)

    ===== LIBRARIAN ===== 

    true_self = librarian
    ego_self = librarian
    social_self = librarian

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
        self._brief_string = character_text["brief"]
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/8/86/Librarian_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Librarian"

        self._role_enum = TBRole.librarian
        self._emoji = "<:librarian:722685072205152267>"

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
        """Send two possible outsiders"""

        # First set the social self
        for player in globvars.master_state.game.sitting_order:
            player.role.set_new_social_self()

        # Choose the player that registers as outsider
        outsiders = []
        for player in globvars.master_state.game.sitting_order:
            if player.role.social_self.category == Category.outsider:
                outsiders.append(player)
        if outsiders:
            random.shuffle(outsiders)
            outsider = outsiders.pop()
        else:
            msg = self.emoji + " " + self.instruction
            msg += "\n"
            msg += librarian_init_zero

            try:
                await recipient.send(msg)
            except discord.Forbidden:
                pass
            globvars.logging.info(f">>> Librarian [send_first_night_instruction] Sent 0 outsider")

        # Choose the other player
        other_possibilities = [player for player in globvars.master_state.game.sitting_order 
                               if player.user.id != outsider.user.id]
        other = random.choice(other_possibilities)
        
        # Construct the message
        two_player_list = [outsider, other]
        random.shuffle(two_player_list)
        msg = self.emoji + " " + self.instruction
        msg += "\n"
        msg += librarian_init.format(outsider.role.social_self.name)
        msg += "```basic\n"
        msg += f"{two_player_list[0].user.display_name} ({two_player_list[0].user.id})\n"
        msg += f"{two_player_list[1].user.display_name} ({two_player_list[1].user.id})\n"
        msg += "```"

        try:
            await recipient.send(msg)
        except discord.Forbidden:
            pass

        globvars.logging.info(f">>> Librarian [send_first_night_instruction] Sent {outsider} and {other}")
