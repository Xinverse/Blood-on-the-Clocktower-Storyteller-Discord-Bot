"""Contains the Monk Character class"""

import json 
import discord
from botc import Action, ActionTypes, Townsfolk, Character, SafetyFromDemon, RecurringAction
from botc.BOTCUtils import GameLogic
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.monk.value.lower()]

with open('botutils/bot_text.json') as json_file:
    bot_text = json.load(json_file)
    butterfly = bot_text["esthetics"]["butterfly"]


class Monk(Townsfolk, TroubleBrewing, Character, RecurringAction):
    """Monk: Each night*, choose a player (not yourself): they are safe from the Demon tonight.

    ===== MONK ===== 

    true_self = monk
    ego_self = monk
    social_self = monk

    commands:
    - protect <player>

    initialize setup? -> NO
    initialize role? -> NO

    ----- First night
    START:
    override first night instruction? -> NO  # default is to send instruction string only

    ----- Regular night
    START:
    override regular night instruction -> YES  # default is to send nothing
                                       => Send query for "protect" command                              
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
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/1/1b/Monk_Token.png"
        self._art_link_cropped = "https://imgur.com/Hiv2lIw.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Monk"

        self._role_enum = TBRole.monk
        self._emoji = "<:monk:722687015560151050>"
    
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
    
    def has_finished_night_action(self, player):
        """Return True if monk has submitted the protect action"""
        
        if player.is_alive():
            # First night, monk ability does not act
            if globvars.master_state.game._chrono.is_night_1():
                return True
            current_phase_id = globvars.master_state.game._chrono.phase_id
            received_action = player.action_grid.retrieve_an_action(current_phase_id)
            return received_action is not None and received_action.action_type == ActionTypes.protect
        return True
    
    @GameLogic.except_first_night
    @GameLogic.no_self_targetting
    @GameLogic.requires_one_target
    @GameLogic.changes_not_allowed
    async def register_protect(self, player, targets):
        """Protect command"""

        # Must be 1 target
        assert len(targets) == 1, "Received a number of targets different than 1 for monk 'protect'"
        action = Action(player, targets, ActionTypes.protect, globvars.master_state.game._chrono.phase_id)
        player.action_grid.register_an_action(action, globvars.master_state.game._chrono.phase_id)
        msg = butterfly + " " + character_text["feedback"].format(targets[0].game_nametag)
        await player.user.send(msg)
    
    async def exec_protect(self, monk_player, protected_player):
        """Execute the protection action (night ability interaction)"""

        if not monk_player.is_droisoned() and monk_player.is_alive():
            protected_player.add_status_effect(SafetyFromDemon(monk_player, protected_player, 2))
    
    async def process_night_ability(self, player):
        """Process night actions for the monk character.
        @player : the Monk player (Player object)
        """
        
        phase = globvars.master_state.game._chrono.phase_id
        action = player.action_grid.retrieve_an_action(phase)
        # The monk has submitted an action. We call the execution function immediately
        if action:
            assert action.action_type == ActionTypes.protect, f"Wrong action type {action} in monk"
            targets = action.target_player
            protected_player = targets[0]
            await self.exec_protect(player, protected_player)
        # The imp has not submitted an action. We will not randomize the action because this 
        # is a priviledged ability
        else:
            pass

