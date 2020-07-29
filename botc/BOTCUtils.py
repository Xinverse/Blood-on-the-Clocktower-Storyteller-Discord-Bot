"""Contains some BoTC game related utility functions"""

import asyncio
import json
import configparser
import random
from .Category import Category
from discord.ext import commands, tasks

Config = configparser.ConfigParser()
Config.read("config.INI")

MAX_MESSAGE_LEN = Config["misc"]["MAX_MESSAGE_LEN"]
MAX_MESSAGE_LEN = int(MAX_MESSAGE_LEN)

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)
    x_emoji = documentation["cmd_warnings"]["x_emoji"]
    player_not_found = documentation["cmd_warnings"]["player_not_found"]
    no_self_targetting_str = documentation["cmd_warnings"]["no_self_targetting_str"]
    except_first_night_str = documentation["cmd_warnings"]["except_first_night_str"]
    requires_one_target_str = documentation["cmd_warnings"]["requires_one_target_str"]
    requires_two_targets_str = documentation["cmd_warnings"]["requires_two_targets_str"]
    requires_different_targets_str = documentation["cmd_warnings"]["requires_different_targets_str"]
    changes_not_allowed = documentation["cmd_warnings"]["changes_not_allowed"]
    unique_ability_used = documentation["cmd_warnings"]["unique_ability_used"]
    lore = documentation["lore"]


# ========== TARGETS ===============================================================
# ----------------------------------------------------------------------------------

class Targets(list):
   """Targets class for storing BoTC characters' targets"""

   def __init__(self, target_list):
      self.target_list = target_list
      self.target_nb = len(self.target_list)
   
   def __len__(self):
      return len(self.target_list)
   
   def __iter__(self):
      yield from self.target_list
   
   def __getitem__(self, index):
      return list.__getitem__(self.target_list, index)


def get_number_image(nb):
   """Get a random bloodied number image corresponding to the input integer"""
   assert nb in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0], "Number received is not a digit"
   numbers = documentation["numbers"]
   possibilities = numbers[str(nb)]
   chosen = random.choice(possibilities)
   return chosen


class BOTCUtils:
   """Some utility functions"""

   @staticmethod
   def has_alive_demons():
      """Return true if the game still has alive demons. Using real life state."""
      import globvars
      game = globvars.master_state.game
      for player in game.sitting_order:
         if player.is_alive():
            if player.role.true_self.category == Category.demon:
               return True
      return False

   @staticmethod
   def get_players_from_role_name(character_name_enum):
      """Return the list of players holding a certain character, using ego_self"""
      import globvars
      game = globvars.master_state.game
      ret = []
      for player in game.sitting_order:
         if player.role.ego_self.name == character_name_enum.value:
            ret.append(player)
      return ret
   
   @staticmethod
   def get_all_minions():
      """Return the list of players that are minions, using true_self"""
      import globvars
      game = globvars.master_state.game
      ret = []
      for player in game.sitting_order:
         if player.role.true_self.category == Category.minion:
            ret.append(player)
      return ret

   @staticmethod
   def get_random_player():
      """Get any random player from the game"""
      import globvars
      game = globvars.master_state.game
      return random.choice(game.sitting_order)

   @staticmethod
   def get_random_player_excluding(player):
      """Get any random player that is not the player passed in the argument"""
      import globvars
      game = globvars.master_state.game
      possibilities = [p for p in game.sitting_order if p.user.id != player.user.id]
      return random.choice(possibilities)

   @staticmethod
   def get_role_list(edition, category):
      """Get the entire list of an edition and a category"""
      return [role_class() for role_class in edition.__subclasses__() if issubclass(role_class, category)]
   
   @staticmethod
   def get_player_from_id(userid):
      """Find a player object from a user ID"""
      import globvars
      game = globvars.master_state.game
      userid = int(userid)
      for player in game.sitting_order:
         if player.user.id == userid:
            return player
   
   @staticmethod
   def get_player_from_string(string):
      """Find a player object from user input string.
      Code inspired from belungawhale's discord werewolf project. 
      """
      import globvars
      game = globvars.master_state.game
      string = string.lower()
      usernames = []
      discriminators = []
      nicknames = []
      ids_contains = []
      usernames_contains = []
      nicknames_contains = []
      for player in game.sitting_order:
         if string == str(player.user.id) or string.strip('<@!>') == str(player.user.id):
            return player
         if str(player.user).lower().startswith(string):
            usernames.append(player)
         if string.strip('#') == player.user.discriminator:
            discriminators.append(player)
         if player.user.display_name.lower().startswith(string):
            nicknames.append(player)
         if string in player.user.name.lower():
            usernames_contains.append(player)
         if string in player.user.display_name.lower():
            nicknames_contains.append(player)
         if string in str(player.user.id):
            ids_contains.append(player)
      if len(usernames) == 1:
         return usernames[0]
      if len(discriminators) == 1:
         return discriminators[0]
      if len(nicknames) == 1:
         return nicknames[0]
      if len(usernames_contains) == 1:
         return usernames_contains[0]
      if len(nicknames_contains) == 1:
         return nicknames_contains[0]
      if len(ids_contains) == 1:
         return ids_contains[0]
      return None


# ========== CHECK ERRORS ==========================================================
# ----------------------------------------------------------------------------------

class WhisperTooLong(commands.CommandInvokeError):
   """Raised when a command user tries to whisper a message that is too long"""
   pass

class NotAPlayer(commands.CheckFailure):
   """Raised when a command user is not a registered player"""
   pass


class RoleCannotUseCommand(commands.CheckFailure):
   """Raised when a command user doesn't have a character that allows for a command to be used """
   pass


class NotDMChannel(commands.CheckFailure):
   """Raised when a command user used the command in a channel that is not the bot dm"""
   pass


class NotLobbyChannel(commands.CheckFailure):
   """Raised when a command user used the command in a channel that is not the lobby"""
   pass


class NotDay(commands.CheckFailure):
   """Raised when a command user used the command during another phase than
   day when not supposed to
   """
   pass


class NotDawn(commands.CheckFailure):
   """Raised when a command user used the command during another phase than 
   dawn when not supposed to
   """
   pass


class NotNight(commands.CheckFailure):
   """Raised when a command user used the command during another phase than
   night when not supposed to
   """
   pass


class DeadOnlyCommand(commands.CheckFailure):
   """Raised when a command user used a command reserved for dead players only."""
   pass


class AliveOnlyCommand(commands.CheckFailure):
   """Raised when a command user used a command reserved for alive players only."""
   pass


# ========== GAME LOGIC ============================================================
# ----------------------------------------------------------------------------------

class AbilityForbidden(commands.errors.CommandInvokeError):
   """Custom parent classes for all the following exceptions"""
   pass


class UniqueAbilityError(AbilityForbidden):
   """Attempt to use unique ability twice in game"""
   pass


class FirstNightNotAllowed(AbilityForbidden):
   """Attempt to use action on first night when not allowed"""
   pass


class ChangesNotAllowed(AbilityForbidden):
   """Attempt to resubmit an action after it's been submitted once during the night"""
   pass


class MustBeOneTarget(AbilityForbidden):
   """Must be exactly one target"""
   pass


class MustBeTwoTargets(AbilityForbidden):
   """Must be exactly two targets"""
   pass


class NoSelfTargetting(AbilityForbidden):
   """Does not allow self targetting in command input"""
   pass


class NoRepeatTargets(AbilityForbidden):
   """Does not allow repeat targets. Ex. kill player1 and player1"""
   pass


class GameLogic:
   """Game logic decorators to be used on ability methods in character classes"""

   @staticmethod
   def no_self_targetting(func):
      """Decorator for abilities that disallow the player to target themself"""
      def inner(self, player, targets):
         for target in targets:
            if target.user.id == player.user.id:
               raise NoSelfTargetting(no_self_targetting_str.format(player.user.mention, x_emoji))
         return func(self, player, targets)
      return inner 

   @staticmethod
   def unique_ability(ability_type):
      """Decorator for unique abilities to be used once per game. Decorator factory that 
      creates decorators based on the ability type.

      @ability_type: ActionTypes() enum object
      """
      def decorator(func):
         def inner(self, player, targets):
            from botc import Flags, ActionTypes
            # Slayer's unique "slay" ability. Everyone may use it publicy once.
            if ability_type == ActionTypes.slay:
               if not player.role.ego_self.inventory.has_item_in_inventory(Flags.slayer_unique_attempt):
                  raise UniqueAbilityError(unique_ability_used.format(player.user.mention, x_emoji))
            # Future roles that have a unique ability must go into elif blocks, or else the uncaught 
            # ones will automatically trigger an assertion error.
            else:
               assert 0, "Unique ability check went wrong."
            return func(self, player, targets)
         return inner
      return decorator

   @staticmethod
   def except_first_night(func):
      """Decorator for abilities that cannot be used on the first night"""
      def inner(self, player, targets):
         import globvars
         if globvars.master_state.game.is_night() and globvars.master_state.game.current_cycle == 1:
            raise FirstNightNotAllowed(except_first_night_str.format(player.user.mention, x_emoji))
         return func(self, player, targets)
      return inner

   @staticmethod
   def changes_not_allowed(func):
      """Decorator for abilities that cannot modify targets after inputting them"""
      def inner(self, player, targets):
         import globvars
         if player.role.ego_self.has_finished_night_action(player):
            raise ChangesNotAllowed(changes_not_allowed.format(player.user.mention, x_emoji))
         return func(self, player, targets)
      return inner
   
   @staticmethod
   def requires_one_target(func):
      """Decorator for abilities that require one target"""
      def inner(self, player, targets):
         if len(targets) != 1:
            raise MustBeOneTarget(requires_one_target_str.format(player.user.mention, x_emoji))
         return func(self, player, targets)
      return inner
   
   @staticmethod
   def requires_two_targets(func):
      """Decorator for abilities that require two targets"""
      def inner(self, player, targets):
         if len(targets) != 2:
            raise MustBeTwoTargets(requires_two_targets_str.format(player.user.mention, x_emoji))
         return func(self, player, targets)
      return inner
   
   @staticmethod
   def requires_different_targets(func):
      """Decorator for abilities that do not allow repeat players in the targets"""
      def inner(self, player, targets):
         id_list = [target.user.id for target in targets]
         if len(id_list) != len(set(id_list)):
            raise NoRepeatTargets(requires_different_targets_str.format(player.user.mention, x_emoji))
         return func(self, player, targets)
      return inner


# ========== CONVERTERS ============================================================
# ----------------------------------------------------------------------------------

class PlayerNotFound(commands.BadArgument):
   """Error for when a player argument passed is not found"""
   pass


class RoleNotFound(commands.BadArgument):
   """Error for when a role argument passed is not found"""
   pass


class PlayerConverter(commands.Converter):
   """Parse the player name input arguments from commands"""

   async def convert(self, ctx, argument):
      """Convert to player objects"""
      player = BOTCUtils.get_player_from_string(argument)
      if player:
         return player
      raise PlayerNotFound(f"Player {argument} not found.")


class WhisperConverter(commands.Converter):
   """Parse the whisper content"""

   async def convert(self, ctx, argument):
      """Convert to a string while also checking for the maximum length"""
      if len(argument) > max(MAX_MESSAGE_LEN - 120, 0):
         raise WhisperTooLong("Whisper is too long")
      return argument


class RoleConverter(commands.Converter):
    """Convert a role name to a botc character class"""

    async def convert(self, ctx, argument):
        """
        Find a role name amongst the botc pack. 
        Return the role class if it is found, else return None

        The game_packs variable is coded in the following way:

        {'botc': {'game_obj': <botc.Game.Game object at 0x1187bffd0>, 'gamemodes': {'trouble-brewing': 
        [Baron Obj, Butler Obj, Chef Obj, Drunk Obj, Empath Obj, Fortune Teller Obj, Imp Obj, 
        Investigator Obj, Librarian Obj, Mayor Obj, Monk Obj, Poisoner Obj, Ravenkeeper Obj, 
        Recluse Obj, Saint Obj, Scarlet Woman Obj, Slayer Obj, Soldier Obj, Undertaker Obj, 
        Virgin Obj, Washerwoman Obj]}}}
        """
        import globvars
        editions = globvars.master_state.game_packs["botc"]["gamemodes"]
        for edition in editions:
            role_pool = editions[edition]
            for role in role_pool:
                if argument.lower() in role.name.lower():
                    return role
        raise RoleNotFound(f"Role {argument} not found.")


class PlayerParser(commands.Converter):
   """Parse the player name input arguments from game commands"""

   async def convert(self, ctx, argument):
      """Convert to player objects, and split at "and" keyword"""
      raw_targets = argument.split(" and ")
      actual_targets = []
      for raw in raw_targets:
         player = BOTCUtils.get_player_from_string(raw)
         if player:
            actual_targets.append(player)
         else:
            msg = player_not_found.format(ctx.author.mention, x_emoji)
            await ctx.author.send(msg)
            raise commands.BadArgument(f"Player {raw} not found.")
      return Targets(actual_targets)


# ========== MISCELLANEOUS =========================================================
# ----------------------------------------------------------------------------------

class LorePicker:
   """Helps to pick lore strings from the json file"""

   SLAY_SUCCESS = "slay_success"
   SLAY_FAIL = "slay_fail"

   def pick(self, category):
      """Pick the lore string based on the weighted random function"""
      chosen = random.choices(
         lore[category]["outputs"],
         weights = lore[category]["weights"]
      )
      return chosen[0]
   