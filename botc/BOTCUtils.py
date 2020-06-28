"""Contains some BoTC game related utility functions"""

import json
import random
from discord.ext import commands

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)
    x_emoji = documentation["cmd_warnings"]["x_emoji"]
    player_not_found = documentation["cmd_warnings"]["player_not_found"]
   

def get_number_image(nb):
   """Get a random bloodied number image corresponding to the input integer"""
   assert nb in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0], "Number received is not a digit"
   numbers = documentation["numbers"]
   possibilities = numbers[str(nb)]
   chosen = random.choice(possibilities)
   return chosen


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


class BOTCUtils:
   """Some utility functions"""

   @staticmethod
   def get_role_list(edition, category):
      """Get the entire list of an edition and a category """
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


class Targets:
   """Targets class for storing BoTC characters' targets"""

   def __init__(self, target_list):
      self.target_list = target_list
      self.target_nb = len(self.target_list)
   
   def __len__(self):
      return len(self.target_list)
   
   def __iter__(self):
      yield from self.target_list


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
            msg = player_not_found.format(ctx.author.mention, x_emoji, raw if len(raw) <= 1000 else raw[:1000])
            await ctx.author.send(msg)
            raise commands.BadArgument(f"Player {raw} not found.")
      return Targets(actual_targets)


class UniqueAbilityError(Exception):
   """Attempt to use unique ability twice"""
   pass


class FirstNightNotAllowed(Exception):
   """Attempt to use action on first night when not allowed"""
   pass


class ChangesNotAllowed(Exception):
   """Attempt to resubmit an action after it's been used"""
   pass


class MustBeOneTarget(Exception):
   """Must be exactly one target"""
   pass


class MustBeTwoTargets(Exception):
   """Must be exactly two targets"""
   pass


class NoSelfTargetting(Exception):
   """Does not allow self targetting in command input"""
   pass


class GameLogic:
   """Game logic decorators to be used on ability methods in character classes"""

   @staticmethod
   def no_self_targetting(func):
      """Decorator for abilities that disallow the player to target themself"""
      def inner(self, player, targets):
         for target in targets:
            if target.user.id == player.user.id:
               raise NoSelfTargetting("You may not target yourself")
         return func(self, player, targets)
      return inner 

   @staticmethod
   def unique_ability(func):
      """Decorator for unique abilities to be used once per game"""
      def inner(self, player, targets):
         return func(self, player, targets)
      return inner

   @staticmethod
   def except_first_night(func):
      """Decorator for abilities that cannot be used on the first night"""
      def inner(self, player, targets):
         import globvars
         if globvars.master_state.game.is_night() and globvars.master_state.game.current_cycle == 1:
            raise FirstNightNotAllowed("You may not use this command during the first night.")
         return func(self, player, targets)
      return inner

   @staticmethod
   def changes_not_allowed(func):
      """Decorator for abilities that cannot modify targets after inputting them"""
      def inner(self, player, targets):
         return func(self, player, targets)
      return inner
   
   @staticmethod
   def requires_one_target(func):
      """Decorator for abilities that require one target"""
      def inner(self, player, targets):
         if len(targets) != 1:
            raise MustBeOneTarget("Command must take exactly one input")
         return func(self, player, targets)
      return inner
   
   @staticmethod
   def requires_two_targets(func):
      """Decorator for abilities that require two targets"""
      def inner(self, player, targets):
         if len(targets) != 2:
            raise MustBeTwoTargets("Command must take exactly two inputs")
         return func(self, player, targets)
      return inner
