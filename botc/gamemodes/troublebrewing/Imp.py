"""Contains the Imp Character class"""

import json
import discord
import random
import datetime
import configparser
import botutils
from botc import Action, ActionTypes, Demon, Townsfolk, Outsider, Character, \
    RecurringAction, StatusList, AlreadyDead
from botc.gamemodes.troublebrewing.Soldier import Soldier
from botc.BOTCUtils import GameLogic, BOTCUtils
from ._utils import TroubleBrewing, TBRole
import globvars

Config = configparser.ConfigParser()

Config.read("preferences.INI")

DEMON_COLOR = Config["colors"]["DEMON_COLOR"]
DEMON_COLOR = int(DEMON_COLOR, 16)

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.imp.value.lower()]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    demon_bluff_str = strings["gameplay"]["demonbluffs"]
    action_assign = strings["gameplay"]["action_assign"]
    role_change = strings["gameplay"]["role_change"]
    copyrights_str = strings["misc"]["copyrights"]

with open('botutils/bot_text.json') as json_file:
    bot_text = json.load(json_file)
    butterfly = bot_text["esthetics"]["butterfly"]


class Imp(Demon, TroubleBrewing, Character, RecurringAction):
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
        
        self._art_link = "https://bloodontheclocktower.com/wiki/images/4/42/Imp_Token.png"
        self._art_link_cropped = "https://imgur.com/ptpr9A1.png"
        self._wiki_link = "https://bloodontheclocktower.com/wiki/Imp"

        self._role_enum = TBRole.imp
        self._emoji = "<:tbimp:739317350897025054>"

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
    
    def has_finished_night_action(self, player):
        """Return True if imp has submitted the kill action"""

        if player.is_alive():
            if globvars.master_state.game._chrono.is_night_1():
                return True
            current_phase_id = globvars.master_state.game._chrono.phase_id
            received_action = player.action_grid.retrieve_an_action(current_phase_id)
            return received_action is not None and received_action.action_type == ActionTypes.kill
        return True
    
    @GameLogic.except_first_night
    @GameLogic.requires_one_target
    @GameLogic.changes_not_allowed
    async def register_kill(self, player, targets):
        """Kill command"""
        
        # Must be 1 target
        assert len(targets) == 1, "Received a number of targets different than 1 for imp 'kill'"
        action = Action(player, targets, ActionTypes.kill, globvars.master_state.game._chrono.phase_id)
        player.action_grid.register_an_action(action, globvars.master_state.game._chrono.phase_id)
        # Normal kill
        if player.user.id != targets[0].user.id:
            msg = butterfly + " " + character_text["feedback"][0].format(targets[0].game_nametag)
            await player.user.send(msg)
        # Starpass
        else:
            msg = butterfly + " " + character_text["feedback"][1].format(targets[0].game_nametag)
            await player.user.send(msg)
    
    async def exec_kill(self, demon_player, killed_player):
        """Execute the kill action (night ability interaction)"""

        if demon_player.is_alive() and not demon_player.is_droisoned():
            # Players who have received a status effect granting them safety from the demon 
            # do not die
            if killed_player.has_status_effect(StatusList.safety_from_demon):
                return
            await killed_player.role.true_self.on_being_demon_killed(killed_player)
    
    async def _starpass(self, demon_player):
        """Starpassing ability works when the demon is killed by himself at night"""
        
        # If 5 or more players alive (not counting travelers), scarlet woman has priority 
        # over the promotion to demonhood
        if globvars.master_state.game.nb_alive_players >= 5:

            from botc.gamemodes.troublebrewing import ScarletWoman
            # This list of scarletwomen could contain dead players
            scarletwomen = BOTCUtils.get_players_from_role_name(ScarletWoman()._role_enum)

            if scarletwomen:
                # We only want the alive, and not poisoned scarlet women
                alive_scarletwomen = [player for player in scarletwomen if player.is_alive() and not player.is_droisoned()]
                if alive_scarletwomen:
                    promoted = random.choice(alive_scarletwomen)
                    promoted._old_role_obj = promoted._role_obj
                    await promoted.exec_change_role(Imp())
                    embed = self.__make_demonhood_promo_embed(promoted)
                    try:
                        await promoted.user.send(embed = embed)
                    except discord.Forbidden:
                        pass
                    return
        
        # Otherwise, any random minion is selected
        # This list of minions could contain dead players
        minions = BOTCUtils.get_all_minions()

        if minions:
            # We only want the alive players.
            alive_minions = [player for player in minions if player.is_alive()]
            if alive_minions:
                promoted = random.choice(alive_minions)
                promoted._old_role_obj = promoted._role_obj
                await promoted.exec_change_role(Imp())
                embed = self.__make_demonhood_promo_embed(promoted)
                try:
                    await promoted.user.send(embed = embed)
                except discord.Forbidden:
                    pass

    async def on_being_demon_killed(self, killed_player):
        """Function that runs after the player has been killed by the demon at night.
        Overriding the parent behaviour. 
        This implements the star passing mechanic.
        """
        if killed_player.is_alive():
            await self._starpass(killed_player)
            await killed_player.exec_real_death()
            globvars.master_state.game.night_deaths.append(killed_player)
    
    async def on_being_executed(self, executed_player):
        """Funtion that runs after the player has been executed.
        Overriding the parent behaviour.
        Check for presence of scarlet woman and promote her to demonhood if applicable.
        """
        if executed_player.is_alive():
            # If 5 or more players alive (not counting travelers), scarlet woman gets 
            # promoted to demonhood
            if globvars.master_state.game.nb_alive_players >= 5:

                from botc.gamemodes.troublebrewing import ScarletWoman
                # This list of scarletwomen could contain dead players
                scarletwomen = BOTCUtils.get_players_from_role_name(ScarletWoman()._role_enum)

                if scarletwomen:
                    # We only want the alive, and not poisoned scarlet women
                    alive_scarletwomen = [player for player in scarletwomen if player.is_alive() and not player.is_droisoned()]
                    if alive_scarletwomen:
                        promoted = random.choice(alive_scarletwomen)
                        promoted._old_role_obj = promoted._role_obj
                        await promoted.exec_change_role(Imp())
                        embed = self.__make_demonhood_promo_embed(promoted)
                        try:
                            await promoted.user.send(embed = embed)
                        except discord.Forbidden:
                            pass

            await executed_player.exec_real_death()
            game = globvars.master_state.game
            game.today_executed_player = executed_player
    
    def __make_demonhood_promo_embed(self, promoted):
        """Helper function to create an embed to the player promoted to demonhood."""

        recipient = promoted.user
        msg = f"***{recipient.name}#{recipient.discriminator}***, the **{promoted.role.name}**:"
        msg += "\n"
        msg += role_change.format(self.emoji, self.name)
        msg += "\n"
        msg += self.emoji + " " + self.instruction

        embed = discord.Embed(description = msg, color = DEMON_COLOR)
        embed.set_thumbnail(url = self.botc_logo_link)
        embed.set_image(url = self._art_link_cropped)
        embed.set_footer(text = copyrights_str)
        embed.timestamp = datetime.datetime.utcnow()

        return embed
    
    async def process_night_ability(self, player):
        """Process night actions for the imp character.
        @player : the Imp player (Player object)
        """

        # We only do any of the following if the imp is alive. Otherwise skip everything.
        if player.is_alive():
        
            phase = globvars.master_state.game._chrono.phase_id
            action = player.action_grid.retrieve_an_action(phase)
            # The imp has submitted an action. We call the execution function immediately
            if action:
                assert action.action_type == ActionTypes.kill, f"Wrong action type {action} in imp"
                targets = action.target_player
                killed_player = targets[0]
                await self.exec_kill(player, killed_player)
            # The imp has not submitted an action. We will randomize the action and make 
            # the imp kill one random player that is not the imp. 
            else:
                if player.is_alive():
                    killed_player = BOTCUtils.get_random_player_excluding(player)
                    await self.exec_kill(player, killed_player)
                    msg = botutils.BotEmoji.butterfly
                    msg += " "
                    msg += action_assign.format(killed_player.game_nametag)
                    try:
                        await player.user.send(msg)
                    except discord.Forbidden:
                        pass
                else:
                    pass
