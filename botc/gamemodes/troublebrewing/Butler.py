"""Contains the Butler Character class"""

import json 
import botutils
import discord
from botc.BOTCUtils import GameLogic
from botc import Outsider, Character
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.butler.value.lower()]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    target_nb = strings["cmd_warnings"]["target_nb"]
    x_emoji = strings["cmd_warnings"]["x_emoji"]

with open('botutils/bot_text.json') as json_file:
    bot_text = json.load(json_file)
    butterfly = bot_text["esthetics"]["butterfly"]


class Butler(Outsider, TroubleBrewing, Character):
    """Butler: Each night, choose a player (not yourself): tomorrow, you may only vote if 
    they are voting too.

    ===== BUTLER ===== 

    true_self = butler
    ego_self = butler
    social_self = butler

    commands
    - serve <player>

    initialize setup? -> NO
    initialize role? -> NO

    ----- First night
    START:
    override first night instruction? -> YES  # default is to send instruction string only
                                      => Send query for "serve" command

    ----- Regular night
    START:
    override regular night instruction? -> YES  # default is to send nothing
                                        => Send query for "serve" command
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Outsider.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        self._brief_string = character_text["brief"]
        self._action = character_text["action"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/1/1a/Butler_Token.png"
        self._art_link_cropped = "https://imgur.com/UrELsAS.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Butler"

        self._role_enum = TBRole.butler
        self._emoji = "<:butler:722687426421719050>"

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
    
    def add_action_field_n1(self, embed_obj):
        """Send the stats list n1"""

        msg = self.action
        msg += globvars.master_state.game.create_sitting_order_stats_string()
        embed_obj.add_field(name = butterfly + " **「 Your Action 」**", value = msg, inline = False)
        return embed_obj
    
    @GameLogic.changes_not_allowed
    @GameLogic.requires_one_target
    async def register_serve(self, player, targets):
        """Serve command registration"""
        pass
