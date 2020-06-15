"""Contains the BOTC Game class"""

import random
import datetime
import botutils
from .Phase import Phase
from .Player import Player
from .errors import GameError, TooFewPlayers, TooManyPlayers
from .Townsfolk import Townsfolk
from .Outsider import Outsider
from .Minion import Minion
from .Demon import Demon
from .gamemodes.troublebrewing._utils import TroubleBrewing
from .gamemodes.Gamemode import Gamemode
from .RoleGuide import RoleGuide
from models import GameMeta

random.seed(datetime.datetime.now())


class BOTCUtils:
   """Some utility functions"""

   @staticmethod
   def get_role_list(edition, category):
      """Get the entire list of an edition and a category """
      return [role_class() for role_class in edition.__subclasses__() if issubclass(role_class, category)]


class Game(GameMeta):
   """BoTC Game class"""

   MIN_PLAYERS = 5
   MAX_PLAYERS = 15

   def __init__(self):
      
      self._gamemode = Gamemode.trouble_brewing  # default gamemode will always be trouble brewing
      self._member_obj_list = []  # list object - list of discord member objects 
      self._player_obj_list = []  # list object - list of player objects
      self._sitting_order = tuple()  # tuple object (for immutability)
      self._current_phase = Phase.idle  
   
   @property
   def gamemode(self):
      return self._gamemode
   
   @property
   def member_obj_list(self):
      return self._member_obj_list
   
   @property
   def player_obj_list(self):
      return self._player_obj_list

   @property
   def sitting_order(self):
      return self._sitting_order
   
   @property
   def current_phase(self):
      return self._current_phase

   def register_players(self, id_list):
      """Register the players. 
      Must be implemented.
      """

      for user_id in id_list:
         member_obj = botutils.get_member_obj(user_id)
         if member_obj:
            self._member_obj_list.append(member_obj)
         else:
            raise GameError("Member not found, invalid user ID")

   def start_game(self):
      """Start the game. 
      Must be implemented.
      """

      # Generate the setup (role list)
      setup = self.generate_role_set()
      # Give each player a role
      self.distribute_roles(setup, self.member_obj_list)

   def end_game(self):
      """End the game, compute winners etc. 
      Must be implemented.
      """
      pass

   def make_nightfall(self):
      """Transition the game into night phase"""
      self._current_phase = Phase.night

   def make_daybreak(self):
      """Transition the game into day phase"""
      self._current_phase = Phase.day

   def generate_role_set(self):
      """Generate a list of roles according to the number of players"""

      num_player = len(self._member_obj_list)
      
      # Incorrect number of players
      if num_player > self.MAX_PLAYERS:
         raise TooManyPlayers("Must be 15 players or less.")
      
      elif num_player < self.MIN_PLAYERS:
         raise TooFewPlayers("Must be 5 players or more.")
      
      # Correct number of players
      else:
         role_guide = RoleGuide(num_player)
         nb_townsfolk = role_guide.nb_townsfolks
         nb_outsider = role_guide.nb_outsiders
         nb_minion = role_guide.nb_minions
         nb_demon = role_guide.nb_demons

         # Trouble brewing mode
         if self.gamemode == Gamemode.trouble_brewing:
               
            tb_townsfolk_all = BOTCUtils.get_role_list(Gamemode.trouble_brewing, Townsfolk())
            tb_outsider_all = BOTCUtils.get_role_list(Gamemode.trouble_brewing, Outsider())
            tb_minion_all = BOTCUtils.get_role_list(Gamemode.trouble_brewing, Minion())
            tb_demon_all = BOTCUtils.get_role_list(Gamemode.trouble_brewing, Demon())

            ret_townsfolk = random.sample(tb_townsfolk_all, nb_townsfolk)
            ret_outsider = random.sample(tb_outsider_all, nb_outsider)
            ret_minion = random.sample(tb_minion_all, nb_minion)
            ret_demon = random.sample(tb_demon_all, nb_demon)

            final_townsfolk = ret_townsfolk.copy()
            final_outsider = ret_outsider.copy()
            final_minion = ret_minion.copy()
            final_demon = ret_demon.copy()

            prelim = ret_townsfolk + ret_outsider + ret_minion + ret_demon

            for role in prelim:
               setup_next = role.exec_init_setup(final_townsfolk, final_outsider, final_minion, final_demon)
               final_townsfolk = setup_next[0]
               final_outsider = setup_next[1]
               final_minion = setup_next[2]
               final_demon = setup_next[3]
            
            setup = final_townsfolk + final_outsider + final_minion + final_demon
            random.shuffle(setup)

            return setup

         # Bad moon rising mode
         elif self.gamemode == Gamemode.bad_moon_rising:
            pass

         # Sects and violets mode
         elif self.gamemode == Gamemode.sects_and_violets:
            pass

         else:
            raise GameError("Gamemode is not one of available BoTC editions.")
      
   def distribute_roles(self, role_obj_list, member_obj_list):
      """Distribute the roles to the players"""

      if len(role_obj_list) != len(member_obj_list):
         raise GameError("Number of players not matching number of roles generated")

      else:
         ret = []
         for member in member_obj_list:
               role_obj = role_obj_list.pop()
               player_obj = Player(member, role_obj)
               ret.append(player_obj)

      self._player_obj_list = ret
   
   def generate_frozen_sitting(self):
        """Freeze the sittings of the table around the game table"""

        random.shuffle(self.player_obj_list)
        self._sitting_order = tuple(self._player_obj_list)
    
   def __repr__(self):
      return "BOTC Game Object"
