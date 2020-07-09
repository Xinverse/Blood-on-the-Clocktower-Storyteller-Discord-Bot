"""Contains the Poisoner Character class"""

import json 
import discord
from botc import Action, ActionTypes, Minion, Character, Poison, RecurringAction
from botc.BOTCUtils import GameLogic
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.poisoner.value.lower()]

with open('botutils/bot_text.json') as json_file:
    bot_text = json.load(json_file)
    butterfly = bot_text["esthetics"]["butterfly"]


class Poisoner(Minion, TroubleBrewing, Character, RecurringAction):
    """Poisoner: Each night, choose a player, their ability malfunctions tonight and tomorrow day.

    ===== POISONER ===== 

    true_self = poisoner
    ego_self = poisoner
    social_self = poisoner

    commands:
    - poison <player>

    initialize setup? -> NO
    initialize role? -> NO

    ----- First night
    START:
    override first night instruction? -> YES  # default is to send instruction string only
                                      => Send query for "poison" command
                                      => Send demon and minion identities to this minion 
                                         if 7 players or more

    ----- Regular night
    START:
    override regular night instruction -> YES  # default is to send nothing
                                       => Send query for "poison" command
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Minion.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        self._brief_string = character_text["brief"]
        self._action = character_text["action"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/a/af/Poisoner_Token.png"
        self._art_link_cropped = "https://imgur.com/JaLRhNO.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Poisoner"

        self._role_enum = TBRole.poisoner
        self._emoji = "<:poisoner:722687671671193620>"

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
    
    def has_finished_night_action(self, player):
        """Return True if poisoner has submitted the protect action"""

        if player.is_alive():
            current_phase_id = globvars.master_state.game._chrono.phase_id
            received_action = player.action_grid.retrieve_an_action(current_phase_id)
            return received_action is not None and received_action.action_type == ActionTypes.poison
        return True
    
    @GameLogic.changes_not_allowed
    @GameLogic.requires_one_target
    async def register_poison(self, player, targets):
        """Poison command"""
        # Must be 1 target
        assert len(targets) == 1, "Received a number of targets different than 1 for poisoner 'poison'"
        action = Action(player, targets, ActionTypes.poison, globvars.master_state.game._chrono.phase_id)
        player.action_grid.register_an_action(action, globvars.master_state.game._chrono.phase_id)
        msg = butterfly + " " + character_text["feedback"].format(targets[0].game_nametag)
        await player.user.send(msg)

    async def exec_poison(self, poisoner_player, poisoned_player):
        """Execute the poison actions (night interaction)"""
        if not poisoner_player.is_droisoned() and poisoner_player.is_alive():
            poisoned_player.add_status_effect(Poison(poisoner_player, poisoned_player))
    
    async def process_night_ability(self, player):
        """Process night actions for the poisoner character.
        @player : the Butler player (Player object)
        """
        
        phase = globvars.master_state.game._chrono.phase_id
        action = player.action_grid.retrieve_an_action(phase)
        # The poisoner has submitted an action. We call the execution function immediately
        if action:
            assert action.action_type == ActionTypes.poison, f"Wrong action type {action} in poisoner"
            targets = action.target_player
            poisoned_player = targets[0]
            await self.exec_poison(player, poisoned_player)
        # The poisoner has not submitted an action. We will not randomize the action since 
        # the poison ability is a "priviledged" ability
        else:
            pass
        