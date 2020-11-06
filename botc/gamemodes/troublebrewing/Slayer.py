"""Contains the Slayer Character class"""

import json
from botc import Action, ActionTypes, Inventory, Flags, Townsfolk, Character, \
    NonRecurringAction, Category, LorePicker, AlreadyDead
from botc.BOTCUtils import GameLogic
from ._utils import TroubleBrewing, TBRole
import botutils
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.slayer.value.lower()] 


class Slayer(Townsfolk, TroubleBrewing, Character, NonRecurringAction):
    """Slayer: Once per game, during the day, publicly choose a player: if they are the Demon, they die.

    ===== SLAYER ===== 

    true_self = slayer
    ego_self = slayer
    social_self = slayer

    commands:
    - slay <player>

    initialize setup? -> NO
    initialize role? -> NO

    ----- First night
    START:
    override first night instruction? -> NO  # default is to send instruction string only

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
        self._action = character_text["action"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/2/2f/Slayer_Token.png"
        self._art_link_cropped = "https://imgur.com/MtSElpk.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Slayer"

        self._role_enum = TBRole.slayer
        self._emoji = "<:tbslayer:739317350704218274>"

        self.inventory = Inventory(
            Flags.slayer_unique_attempt
        )

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
    
    @GameLogic.unique_ability(ActionTypes.slay)
    @GameLogic.requires_one_target
    async def register_slay(self, player, targets):
        """Slay command
        @player : Player object
        @targets : Target object
        """

        # Must be 1 target
        assert len(targets) == 1, "Received a number of targets different than 1 for slayer 'slay'"
        action = Action(player, targets, ActionTypes.slay, globvars.master_state.game._chrono.phase_id)
        player.action_grid.register_an_action(action, globvars.master_state.game._chrono.phase_id)
        await self.exec_slay(player, targets[0])
    
    async def exec_slay(self, slayer_player, slain_player):
        """Execute the slay action (immediate effect)"""
        
        # Remove the unique use ability from the player's inventory
        slayer_player.role.ego_self.inventory.remove_item_from_inventory(Flags.slayer_unique_attempt)
        
        # The ability succeeds when the slayer is not droisoned and the slain player is registering
        # as a demon with their social self
        if not slayer_player.is_droisoned():
            if slain_player.role.social_self.category == Category.demon:
                string = LorePicker().pick(LorePicker().SLAY_SUCCESS)
                string = string.format(
                    slayer = slayer_player.game_nametag, 
                    slain = slain_player.game_nametag
                )
                try:
                    await slain_player.exec_real_death()
                except AlreadyDead:
                    pass
                await botutils.send_lobby(string)
                return

        # The ability fails no matter what for a droisoned slayer, or if the slain player 
        # is not a demon
        string = LorePicker().pick(LorePicker().SLAY_FAIL)
        string = string.format(
            slayer = slayer_player.game_nametag, 
            slain = slain_player.game_nametag
        )
        await botutils.send_lobby(string)
