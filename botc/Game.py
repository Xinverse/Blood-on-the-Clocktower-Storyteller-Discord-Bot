"""Contains the BOTC Game class"""

import random
import datetime
import botutils
import globvars
import json
from .BOTCUtils import BOTCUtils
from .Category import Category
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

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    nightfall = strings["gameplay"]["nightfall"]
    daybreak = strings["gameplay"]["daybreak"]
    lobby_game_start = strings["gameplay"]["lobby_game_start"]


class Setup:
   """A class to facilitate role to player access"""

   def __init__(self):

      self.demon = []
      self.minions = []
      self.townsfolks = []
      self.outsiders = []
      self.role_dict = {}  # {"recluse" : player_obj1, "undertaker" : player_obj2}

   def create(self, player_ob_list):

      for player in player_ob_list:
         self.role_dict.update({player.role.name.lower(): player})
         if player.role.category == Category.demon:
            self.demon.append(player)
         elif player.role.category == Category.minion:
            self.minions.append(player)
         elif player.role.category == Category.townsfolk:
            self.townsfolks.append(player)
         elif player.role.category == Category.outsider:
            self.outsiders.append(player)
      assert len(self.demon) == 1, "More than 1 demon found."
   
   def clear(self):
      
      self.__init__()


class Game(GameMeta):
   """BoTC Game class
   
   Order of Action (First Night)
   1. poisoner
   2. washerwoman
   3. librarian
   4. investigator
   5. chef
   6. empath
   7. fortune teller
   8. butler
   9. spy


   Order of Action (All Other Nights)
   1. poisoner
   2. monk
   3. scarlet woman 
   4. imp
   5. ravenkeeper
   6. empath
   7. fortune teller
   8. butler
   9. undertaker
   10. spy
   """

   MIN_PLAYERS = 5
   MAX_PLAYERS = 15

   def __init__(self):
      
      self._gamemode = Gamemode.trouble_brewing  # default gamemode will always be trouble brewing
      self._member_obj_list = []  # list object - list of discord member objects 
      self._player_obj_list = []  # list object - list of player objects
      self._sitting_order = tuple()  # tuple object (for immutability)
      self._current_phase = Phase.idle
      self._setup = Setup()
   
   @property
   def nb_players(self):
      return len(self._player_obj_list)
   
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
   
   @property
   def setup(self):
      return self._setup

   def is_day(self):
      return self.current_phase == Phase.day

   def is_night(self):
      return self.current_phase == Phase.night
   
   def create_sitting_order_stats_string(self):
      """Create a stats board:

      Sitting Order:
      ```css
      Chris (232456937349834784) [DEAD]
      John (233426113285745785) [ALIVE]
      Anna (266015398221479937) [ALIVE]
      Fred (3447492102843678721) [ALIVE]
      ```
      """
      msg = "__*Sitting Order*__ : "
      msg += "```css\n"
      for player in self.sitting_order:
         if player.is_alive():
            line = f"{player.user.display_name} ({player.user.id}) [ALIVE]\n"
         elif player.is_dead():
            line = f"{player.user.display_name} ({player.user.id}) [DEAD]\n"
         else:
            line = f"{player.user.display_name} ({player.user.id}) [QUIT]\n"
         msg += line
      msg += "```"
      return msg

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

   async def start_game(self):
      """Start the game. 
      Must be implemented.
      """
      # Register the players in game
      self.register_players(globvars.master_state.pregame)
      # Generate the setup (role list)
      setup = self.generate_role_set()
      # Give each player a role
      self.distribute_roles(setup, self.member_obj_list)
      # Freeze the sitting
      self.generate_frozen_sitting()
      # Initialize the setup object
      self.setup.clear()
      self.setup.create(self.player_obj_list)
      # Send the lobby welcome message
      await botutils.send_lobby(lobby_game_start)
      # Lock the lobby channel
      await botutils.lock_lobby()
      # Log the game data
      await botutils.log(botutils.Level.info, "Game started, to-do")
      # Send the opening dm to all players
      for player in self._player_obj_list:
         await player.role.ego_self.send_opening_dm_embed(player.user)
      # Send first night info dm to all players
      for player in self._player_obj_list:
         await player.role.ego_self.send_first_night_instruction(player.user)
      # Transition to night fall
      await self.make_nightfall()

   async def end_game(self):
      """End the game, compute winners etc. 
      Must be implemented.
      """
      # Send the lobby welcome message
      await botutils.send_lobby("Game over, todo")
      # Log the game over data
      await botutils.log(botutils.Level.info, "Game finished, to-do")
      # Clear the setup object
      self.setup.clear()
      # Unlock the lobby channel
      await botutils.unlock_lobby()

   async def make_nightfall(self):
      """Transition the game into night phase"""
      self._current_phase = Phase.night
      await botutils.send_lobby(nightfall)

   async def make_daybreak(self):
      """Transition the game into day phase"""
      self._current_phase = Phase.day
      await botutils.send_lobby(daybreak)

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
               
            tb_townsfolk_all = BOTCUtils.get_role_list(TroubleBrewing, Townsfolk)
            tb_outsider_all = BOTCUtils.get_role_list(TroubleBrewing, Outsider)
            tb_minion_all = BOTCUtils.get_role_list(TroubleBrewing, Minion)
            tb_demon_all = BOTCUtils.get_role_list(TroubleBrewing, Demon)

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
