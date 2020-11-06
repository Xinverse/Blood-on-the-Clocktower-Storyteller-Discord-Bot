"""Contains the Butler Character class"""

import json 
import botutils
import discord
from botc.BOTCUtils import GameLogic
from botc import Outsider, Character, Action, ActionTypes, BOTCUtils, RecurringAction, \
    ButlerService
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.butler.value.lower()]

with open('botutils/bot_text.json') as json_file:
    bot_text = json.load(json_file)
    butterfly = bot_text["esthetics"]["butterfly"]

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)
    action_assign = documentation["gameplay"]["action_assign"]


class Butler(Outsider, TroubleBrewing, Character, RecurringAction):
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
        self._emoji = "<:tbbutler:739317349248794685>"

    def create_n1_instr_str(self):
        """Create the instruction field on the opening dm card"""

        # First line is the character instruction string
        msg = f"{self.emoji} {self.instruction}"
        addendum = character_text["n1_addendum"]
        
        # Some characters have a line of addendum
        if addendum:
            scroll_emoji = botutils.BotEmoji.scroll
            msg += f"\n{scroll_emoji} {addendum}"
            
        return msg
    
    def add_action_field_n1(self, embed_obj):
        """Send the stats list n1"""

        msg = self.action
        msg += globvars.master_state.game.create_sitting_order_stats_string()
        embed_obj.add_field(name = butterfly + " **「 Your Action 」**", value = msg, inline = False)
        return embed_obj
    
    def has_finished_night_action(self, player):
        """Return True if butler has submitted the serve action"""
        
        if player.is_alive():
            current_phase_id = globvars.master_state.game._chrono.phase_id
            received_action = player.action_grid.retrieve_an_action(current_phase_id)
            return received_action is not None and received_action.action_type == ActionTypes.serve
        return True
    
    @GameLogic.no_self_targetting
    @GameLogic.requires_one_target
    @GameLogic.changes_not_allowed
    async def register_serve(self, player, targets):
        """Serve command registration"""

        # Must be 1 target
        assert len(targets) == 1, "Received a number of targets different than 1 for butler 'serve'"
        action = Action(player, targets, ActionTypes.serve, globvars.master_state.game._chrono.phase_id)
        player.action_grid.register_an_action(action, globvars.master_state.game._chrono.phase_id)
        msg = butterfly + " " + character_text["feedback"].format(targets[0].game_nametag)
        await player.user.send(msg)
    
    async def exec_serve(self, butler_player, master_player):
        """Execute the serve action (night ability interaction)"""

        if butler_player.is_alive() and not butler_player.is_droisoned():
            butler_player.add_status_effect(ButlerService(butler_player, butler_player, master_player, 2))
    
    async def process_night_ability(self, player):
        """Process night actions for the butler character.
        @player : the Butler player (Player object)
        """

        # We only do any of the following if the butler is alive. Otherwise skip everything.
        if player.is_alive():
        
            phase = globvars.master_state.game._chrono.phase_id
            action = player.action_grid.retrieve_an_action(phase)

            # The butler has submitted an action. We call the execution function immediately
            if action:
                assert action.action_type == ActionTypes.serve, f"Wrong action type {action} in butler"
                targets = action.target_player
                master_player = targets[0]
                await self.exec_serve(player, master_player)
            # The butler has not submitted an action. We randomize the master for him, 
            # DM him the choice of the master, and then call the execution function
            else:
                master_player = BOTCUtils.get_random_player_excluding(player)
                await self.exec_serve(player, master_player)
                msg = botutils.BotEmoji.butterfly
                msg += " "
                msg += action_assign.format(master_player.game_nametag)
                try:
                    await player.user.send(msg)
                except discord.Forbidden:
                    pass
