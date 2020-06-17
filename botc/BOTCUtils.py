"""Contains the BOTCUtils class"""

import globvars

class BOTCUtils:
   """Some utility functions"""

   @staticmethod
   def get_role_list(edition, category):
      """Get the entire list of an edition and a category """
      return [role_class() for role_class in edition.__subclasses__() if issubclass(role_class, category)]
   
   @staticmethod
   def get_player_from_id(userid):
      """Find a player object from a user ID"""
      userid = int(userid)
      for player in globvars.master_state.game.sitting_order:
         if player.user.id == userid:
            return player
         