"""Contains the Ravenkeeper Character class"""

import json
from botc import Action, ActionTypes
from botc import Townsfolk, Character
from botc.BOTCUtils import GameLogic
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.ravenkeeper.value.lower()]


class Ravenkeeper(Townsfolk, TroubleBrewing, Character):
    """Ravenkeeper: If you die at night, you are woken to choose a player: you learn their character.

    ===== RAVENKEEPER ===== 

    true_self = ravenkeeper
    ego_self = ravenkeeper
    social_self = ravenkeeper

    commands:
    - learn <player>

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
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/45/Ravenkeeper_Token.png"
        self._art_link_cropped = "https://imgur.com/5sReG9x.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Ravenkeeper"
        
        self._role_enum = TBRole.ravenkeeper
        self._emoji = "<:ravenkeeper:722686977295646731>"

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
    
    @GameLogic.changes_not_allowed
    @GameLogic.requires_one_target
    async def register_learn(self, player, targets):
        """Learn command"""
        # Must be 1 target
        assert len(targets) == 1, "Received a number of targets different than 1 for ravenkeeper 'learn'"
        action = Action(player, targets, ActionTypes.learn, globvars.master_state.game._chrono.phase_id)
        player.action_grid.register_an_action(action, globvars.master_state.game._chrono.phase_id)
        await player.user.send("You decided to learn **{}**'s character.".format(targets[0].user.display_name))
        