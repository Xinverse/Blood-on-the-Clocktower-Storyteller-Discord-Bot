"""Contains some BoTC game related utility functions"""

import enum
from discord.ext import commands


class StatusList(enum.Enum):
   """List of status effects in game"""
   safe_from_demon = "safe_from_demon"
   drunk = "drunk"
   poisoned = "poisoned"
   red_herring = "red_herring"


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
   """Raised when a command user used the command during the day when not supposed to"""
   pass


class NotNight(commands.CheckFailure):
   """Raised when a command user used the command during the night when not supposed to"""
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
            raise commands.BadArgument(f"Player {raw} not found.")
      return Targets(actual_targets)


class GameLogic:
   """Game logic decorators to be used on ability methods in character classes"""

   @staticmethod
   def unique_ability(func):
      """Decorator for unique abilities to be used once per game"""
      def inner(self, targets):
         return func(self, targets)
      return inner

   @staticmethod
   def except_first_night(func):
      """Decorator for abilities that cannot be used on the first night"""
      def inner(self, targets):
         return func(self, targets)
      return inner

   @staticmethod
   def changes_not_allowed(func):
      """Decorator for abilities that cannot modify targets after inputting them"""
      def inner(self, targets):
         return func(self, targets)
      return inner
   
   @staticmethod
   def requires_one_target(func):
      """Decorator for abilities that require one target"""
      def inner(self, targets):
         return func(self, targets)
      return inner
   
   @staticmethod
   def requires_two_targets(func):
      """Decorator for abilities that require two targets"""
      def inner(self, targets):
         return func(self, targets)
      return inner
