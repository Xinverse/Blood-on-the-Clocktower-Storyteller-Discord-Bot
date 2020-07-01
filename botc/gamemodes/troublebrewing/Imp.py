"""Contains the Imp Character class"""

import json
import discord
import random
from botc import Action, ActionTypes
from botc import Demon, Townsfolk, Outsider, Character
from botc.BOTCUtils import GameLogic, BOTCUtils
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.imp.value.lower()]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    demon_bluff_str = strings["gameplay"]["demonbluffs"]


class Imp(Demon, TroubleBrewing, Character):
    """Imp: Each night*, choose a player: they die. If you kill yourself this way, 
    a Minion becomes the Imp.

    ===== IMP ===== 

    true_self = imp
    ego_self = imp
    social_self = imp

    commands:
    - kill <player>

    initialize setup? -> NO
    initialize role? -> NO

    ----- First night
    START:
    override first night instruction? -> YES  # default is to send instruction string only
                                      => Send 3 demon bluffs
                                      => Send demon and minion identities to this minion if 7 players or more

    ----- Regular night
    START:
    override regular night instruction? -> YES  # default is to send nothing
                                        => Send query for "kill" command
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Demon.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        self._brief_string = character_text["brief"]
        self._action = character_text["action"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/42/Imp_Token.png"
        self._art_link_cropped = "https://imgur.com/ptpr9A1.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Imp"

        self._role_enum = TBRole.imp
        self._emoji = "<:imp2:722687671377330197>"

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

        # Seven or more players, send the evil list and three demon bluffs
        if globvars.master_state.game.nb_players >= 7:
            bluffs = self.get_demon_bluffs()
            msg += f"\n{self.demon_head_emoji} {demon_bluff_str.format(bluffs[0], bluffs[1], bluffs[2])}"

        return msg
    
    def get_demon_bluffs(self):
        """Get the list of 3 demon bluffs"""

        # 3 demon bluffs: 2 townsfolk characters + 1 outsider character
        # Exclusing all characters taken by other players, as well as the drunk's ego_self
        all_townsfolks = BOTCUtils.get_role_list(TroubleBrewing, Townsfolk)
        all_outsiders = BOTCUtils.get_role_list(TroubleBrewing, Outsider)
        taken_townsfolks = [player.role.name for player in globvars.master_state.game.setup.townsfolks]
        taken_outsiders = [player.role.name for player in globvars.master_state.game.setup.outsiders]

        possible_townsfolk_bluffs = [character for character in all_townsfolks 
                                        if character.name not in taken_townsfolks]
        possible_outsider_bluffs = [character for character in all_outsiders 
                                    if character.name not in taken_outsiders]
        random.shuffle(possible_townsfolk_bluffs)
        random.shuffle(possible_outsider_bluffs)

        # For the first two bluffs, we want a townsfolk, definitely
        bluff_1 = possible_townsfolk_bluffs.pop()
        bluff_2 = possible_townsfolk_bluffs.pop()

        # For the third bluff, if the outsider list is not empty, we will take an outsider. Otherwise
        # it's 40% chance outsider, 60% chance townsfolk
        if possible_outsider_bluffs:
            town_or_out = random.choices(
                ["t", "o"],
                weights=[0.6, 0.4]
            )
            if town_or_out[0] == "t":
                bluff_3 = possible_townsfolk_bluffs.pop()
            else:
                bluff_3 = possible_outsider_bluffs.pop()
        else:
            bluff_3 = possible_townsfolk_bluffs.pop()

        globvars.logging.info(f">>> Imp: Received three demon bluffs {bluff_1}, {bluff_2} and {bluff_3}.")
        return (bluff_1, bluff_2, bluff_3)
    
    async def send_regular_night_instruction(self, recipient):
        """Query the player for "kill" command"""
        
        msg = self.emoji + " " + self.instruction
        msg += "\n\n"
        msg += globvars.master_state.game.create_sitting_order_stats_string()
        try: 
            await recipient.send(msg)
        except discord.Forbidden:
            pass
    
    @GameLogic.changes_not_allowed
    @GameLogic.requires_one_target
    async def register_kill(self, player, targets):
        """Kill command"""
        # Must be 1 target
        assert len(targets) == 1, "Received a number of targets different than 1 for imp 'kill'"
        action = Action(player, targets, ActionTypes.kill, globvars.master_state.game._chrono.phase_id)
        player.action_grid.register_an_action(action, globvars.master_state.game._chrono.phase_id)
        await player.user.send("You decided to kill **{}**.".format(targets[0].user.display_name))
