"""Contains the Ravenkeeper Character class"""

import json
import discord
import random
import datetime
from botc import Action, ActionTypes, Townsfolk, Character, NonRecurringAction, \
    RavenkeeperActivated, StatusList, BOTCUtils, Minion, Demon, Outsider
from botc.BOTCUtils import GameLogic
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.ravenkeeper.value.lower()]

with open('botutils/bot_text.json') as json_file:
    bot_text = json.load(json_file)
    butterfly = bot_text["esthetics"]["butterfly"]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    copyrights_str = strings["misc"]["copyrights"]
    ravenkeeper_reply = strings["gameplay"]["ravenkeeper_reply"]


class Ravenkeeper(Townsfolk, TroubleBrewing, Character, NonRecurringAction):
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
                            
        self._art_link = "https://bloodontheclocktower.com/wiki/images/4/45/Ravenkeeper_Token.png"
        self._art_link_cropped = "https://imgur.com/5sReG9x.png"
        self._wiki_link = "https://bloodontheclocktower.com/wiki/Ravenkeeper"
        
        self._role_enum = TBRole.ravenkeeper
        self._emoji = "<:tbravenkeeper:739317350913802360>"

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
    
    def has_finished_dawn_action(self, player):
        """Return True if ravenkeeper has submitted the learn action"""

        if player.has_status_effect(StatusList.ravenkeeper_activated):
            current_phase_id = globvars.master_state.game._chrono.phase_id
            received_action = player.action_grid.retrieve_an_action(current_phase_id)
            return received_action is not None and received_action.action_type == ActionTypes.learn
        return True
    
    async def send_regular_dawn_start_dm(self, player):
        """Send the query message at dawn for the learn ability, if the ravenkeeper 
        ability is activated. Otherwise send nothing.
        """

        if player.has_status_effect(StatusList.ravenkeeper_activated):

            recipient = player.user
            
            # Construct the message to send
            msg = f"***{recipient.name}#{recipient.discriminator}***, the **{self.name}**:"
            msg += "\n"
            msg += self.emoji + " " + self.instruction
            msg += "\n"

            embed = discord.Embed(description = msg)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text = copyrights_str)

            msg2 = self.action
            msg2 += globvars.master_state.game.create_sitting_order_stats_string()
            embed.add_field(name = butterfly + " **「 Your Action 」**", value = msg2, inline = False)
            
            try:
                await recipient.send(embed = embed)
            except discord.Forbidden:
                pass
        
    async def exec_learn(self, ravenkeeper_player, learn_player):
        """Execute the learn command (dawn ability interaction)"""

        # Correct info
        if not ravenkeeper_player.is_droisoned():
            learned_character_type = learn_player.role.social_self

        # Droisoned info
        else:
            real_character_type = learn_player.role.true_self
            # If the real character type is good
            if real_character_type.is_good():
                tb_minion_all = BOTCUtils.get_role_list(TroubleBrewing, Minion)
                tb_demon_all = BOTCUtils.get_role_list(TroubleBrewing, Demon)
                pool = tb_minion_all + tb_demon_all
                learned_character_type = random.choice(pool)
            # If the real character type is bad
            else:
                tb_townsfolk_all = BOTCUtils.get_role_list(TroubleBrewing, Townsfolk)
                tb_outsider_all = BOTCUtils.get_role_list(TroubleBrewing, Outsider)
                pool = tb_townsfolk_all + tb_outsider_all
                learned_character_type = random.choice(pool)
        
        link = learned_character_type._art_link_cropped
        recipient = ravenkeeper_player.user
        
        msg = f"***{recipient.name}#{recipient.discriminator}***, the **{self.name}**:"
        msg += "\n"
        msg += self.emoji + " " + self.instruction
        msg += "\n"
        msg += ravenkeeper_reply.format(learned_character_type.name)

        embed = discord.Embed(description = msg)
        embed.set_thumbnail(url = link)
        embed.set_footer(text = copyrights_str)
        embed.timestamp = datetime.datetime.utcnow()

        try:
            await recipient.send(embed = embed)
        except discord.Forbidden:
            pass
    
    @GameLogic.requires_one_target
    @GameLogic.changes_not_allowed_dawn
    @GameLogic.requires_status(StatusList.ravenkeeper_activated)
    async def register_learn(self, player, targets):
        """Learn command"""
        
        # Must be 1 target
        assert len(targets) == 1, "Received a number of targets different than 1 for ravenkeeper 'learn'"
        action = Action(player, targets, ActionTypes.learn, globvars.master_state.game._chrono.phase_id)
        player.action_grid.register_an_action(action, globvars.master_state.game._chrono.phase_id)
        msg = butterfly + " " + character_text["feedback"].format(targets[0].game_nametag)
        await player.user.send(msg)
    
    async def on_being_demon_killed(self, killed_player):
        """Function that runs after the player has been killed by the demon at night.
        """
        if killed_player.is_alive():
            await killed_player.exec_real_death()
            globvars.master_state.game.night_deaths.append(killed_player)
            killed_player.add_status_effect(RavenkeeperActivated(killed_player, killed_player))
    
    async def process_dawn_ability(self, player):
        """Process dawn actions for the ravenkeeper character.
        @player : the Ravenkeeper player (Player object)
        """
        
        phase = globvars.master_state.game._chrono.phase_id
        action = player.action_grid.retrieve_an_action(phase)
        # The Ravenkeeper has submitted an action. We call the execution function immediately
        if action:
            assert action.action_type == ActionTypes.learn, f"Wrong action type {action} in ravenkeeper"
            targets = action.target_player
            learn_player = targets[0]
            await self.exec_learn(player, learn_player)
        # The ravenkeeper has not submitted an action. We will not randomize the action since 
        # the reading ability is a "priviledged" ability
        else:
            pass
    