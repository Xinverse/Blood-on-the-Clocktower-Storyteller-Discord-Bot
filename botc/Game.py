"""Contains the BOTC Game class"""

import random
import datetime
import botutils
import globvars
import json
import pytz
import configparser
import discord
import asyncio
import math
from .chrono import GameChrono
from .BOTCUtils import BOTCUtils
from .Category import Category
from .Phase import Phase
from .Player import Player
from .errors import GameError, TooFewPlayers, TooManyPlayers
from .Townsfolk import Townsfolk
from .Outsider import Outsider
from .Minion import Minion
from .Demon import Demon
from botc.gamemodes.troublebrewing.Saint import Saint
from .gamemodes.troublebrewing._utils import TroubleBrewing
from .gamemodes.Gamemode import Gamemode
from .RoleGuide import RoleGuide
from models import GameMeta

Config = configparser.ConfigParser()
Config.read("preferences.INI")

IN_GAME_NORMAL = Config["colors"]["IN_GAME_NORMAL"]
IN_GAME_NORMAL = int(IN_GAME_NORMAL, 16)

BASE_NIGHT = 30
BASE_DAWN = 15
INCREMENT = 15

random.seed(datetime.datetime.now())

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    nightfall = strings["gameplay"]["nightfall"]
    daybreak = strings["gameplay"]["daybreak"]
    dawn = strings["gameplay"]["dawn"]
    lobby_game_start = strings["gameplay"]["lobby_game_start"]
    evilteammates = strings["gameplay"]["evilteammates"]
    copyrights_str = strings["misc"]["copyrights"]
    tb_lore = strings["gameplay"]["tb_lore"]

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)
    skull_unicode = language["esthetics"]["skull"]
    fquit_unicode = language["esthetics"]["fquit"]


class Setup:
   """A class to facilitate role to player access"""

   DEMON_HEAD_EMOJI = "<:demonhead:722894653438820432>"

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
   
   def create_evil_team_string(self):
      """
      :demonhead: Your Evil team consists of:
      ```basic
      Oliver (460105234748801024) (demon)
      Johnny (159985870458322944) (minion)
      Michel (614109280508968980) (minion)
      ```
      """
      msg = Setup.DEMON_HEAD_EMOJI + " " + evilteammates + "```basic\n"
      for demon in self.demon:
         msg += f"{demon.user.display_name} ({demon.user.id}) (demon)"
         msg += "\n"
      for minion in self.minions:
         msg += f"{minion.user.display_name} ({minion.user.id}) (minion)"
         msg += "\n"
      msg += "```"
      return msg
   
   def clear(self):
      
      self.__init__()


class GameLog:
   """Game log class"""

   def __init__(self, game_obj):
      self.setup = game_obj.setup
      self.sitting_order = game_obj.sitting_order
      self.gamemode = game_obj.gamemode.value

   def create_game_obj_log_str(self):
      """Create the game log string. The string looks like this:

      Game Start:
      ```asciidoc
      BoTC game started at 2020-06-19T19:50:04.657050-04:00, with 10 players, using the Trouble-Brewing edition.
      --------------------
      DEMON :: [Tester 1 (614109280508968980) is Imp]
      MINION :: [Tester 5 (235088799074484224) is Baron, Tester 3 (159985870458322944) is Spy]
      TOWNSFOLK :: [Tester 6 (172002275412279296) is Chef, Tester 4 (184405311681986560) is Monk, Xinverse 
      (346426113285753875) is Slayer, Tester 7 (460105234748801024) is Librarian, Tester 2 (270904126974590976) 
      is Investigator]
      OUTSIDER :: [Penguin (606332710911156778) is Saint, Temporary Bot (609674334247771236) is Butler]
      ```
      """

      Config = configparser.ConfigParser()
      Config.read("preferences.INI")

      TIMEZONE = Config["location"]["TIME_ZONE"]

      d = datetime.datetime.now()
      timezone = pytz.timezone(TIMEZONE)
      d_aware = timezone.localize(d)

      msg = "Game Start:```asciidoc\n"
      msg += f"BoTC game started at {d_aware.isoformat()}, with {len(self.sitting_order)} players, using the {self.gamemode} edition.\n"
      msg += "--------------------\n"

      msg += f"DEMON :: {str(self.setup.demon)}\n"
      msg += f"MINION :: {str(self.setup.minions)}\n"
      msg += f"TOWNSFOLK :: {str(self.setup.townsfolks)}\n"
      msg += f"OUTSIDER :: {str(self.setup.outsiders)}\n"

      msg += "```"

      return msg

   async def send_game_obj_log_str(self):
      """Log the game object"""
      msg = self.create_game_obj_log_str()
      await botutils.log(botutils.Level.info, msg)


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

   Our equivalent:
   night start: poisoner, fortune teller, butler
   night end: washerwoman, librarian, investigator, chef, empath, spy


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

   Our equivalent:
   night start: poisoner, monk, imp, fortune teller, butler
   night end: empath, spy, ravenkeeper, undertaker
   """

   MIN_PLAYERS = 5
   MAX_PLAYERS = 15

   def __init__(self):
      
      self._gamemode = Gamemode.trouble_brewing  # default gamemode will always be trouble brewing
      self._member_obj_list = []  # list object - list of discord member objects 
      self._player_obj_list = []  # list object - list of player objects
      self._sitting_order = tuple()  # tuple object (for immutability)
      self._chrono = GameChrono()
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
      return self._chrono.phase
   
   @property
   def current_cycle(self):
      return self._chrono.cycle
   
   @property
   def setup(self):
      return self._setup

   def is_idle(self):
      return self.current_phase == Phase.idle

   def is_day(self):
      return self.current_phase == Phase.day
   
   def is_dawn(self):
      return self.current_phase == Phase.dawn

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

      msg = "```css\n"
      for player in self.sitting_order:
         if player.is_alive():
            line = f"{player.user.display_name} ({player.user.id}) [alive]\n"
         elif player.is_dead():
            line = f"{player.user.display_name} ({player.user.id}) [dead] {skull_unicode}\n"
         else:
            line = f"{player.user.display_name} ({player.user.id}) [quit] {fquit_unicode}\n"
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
   
   async def send_lobby_welcome_message(self):
      """Send the welcome message in lobby"""

      # Trouble Brewing Edition
      if self.gamemode == Gamemode.trouble_brewing:
         embed = discord.Embed(
            title = "WELCOME TO RAVENSWOOD BLUFF", 
            url = TroubleBrewing()._gm_main_page, 
            description = tb_lore,
            color = IN_GAME_NORMAL
            )
         # Using the Saint() object to access some URL's
         embed.set_thumbnail(url = Saint()._botc_logo_link)
         embed.set_author(name = "Trouble Brewing Edition - Blood on the Clocktower (BoTC)",
                          icon_url = Saint()._botc_demon_link)
         embed.set_image(url = TroubleBrewing()._gm_art_link)
         embed.timestamp = datetime.datetime.utcnow()
         embed.set_footer(text = copyrights_str)
         
         pings = " ".join([player.user.mention for player in self.sitting_order])
         msg = lobby_game_start.format(pings, "𝕿𝖗𝖔𝖚𝖇𝖑𝖊 𝕭𝖗𝖊𝖜𝖎𝖓𝖌", self.nb_players)

         await botutils.send_lobby(msg, embed=embed)

      # Bad Moon Rising Edition
      elif self.gamemode == Gamemode.bad_moon_rising:
         pass

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
      # Initialize each role to set flags as needed, etc.
      for player in self._player_obj_list:
         player.role.exec_init_role(self.setup)
      # Send the lobby welcome message
      await self.send_lobby_welcome_message()
      # Lock the lobby channel
      await botutils.lock_lobby()
      # Log the game data
      await GameLog(self).send_game_obj_log_str()
      # Send the opening dm to all players
      for player in self._player_obj_list:
         await player.role.ego_self.send_opening_dm_embed(player.user)
      # Transition to night fall
      await self.make_nightfall()
      # Load game related commands
      globvars.client.load_extension("botc.botc_commands")
      globvars.client.load_extension("botc.botc_debug_commands")
      # Start the game loop
      await self.master_game_loop()
   
   async def master_game_loop(self):
      """Master game loop

      Cycling works like this:
      Night start
      Night end
      Dawn start
      Dawn end
      Day start
      Day end
      etc.

      ----- Night : 
         30 seconds min
         90 seconds max
         Or at intervals of 15 seconds when all actions are submitted (45, 60, 75)
      ----- Dawn : 
         15 seconds min
         30 seconds max
         At intervals of 15 seconds (15, 30)
      ----- Day: 
         2 * sqrt(total_players) minutes until nomination
         Time until each nomination: 30, 20, 15, and 10 for all subsequent nominations.
      ----- Nomination:
         30 seconds for accusations & defence
         7 seconds for each vote (fastforwording)
      """

      # ----- First Night -----
      # Base night length
      await asyncio.sleep(BASE_NIGHT)

      # Increment (night)
      for _ in range(0):
         if self.has_received_all_expected_night_actions():
            break
         await asyncio.sleep(INCREMENT)
      
      # End night
      for player in self.sitting_order:
         await player.role.ego_self.send_n1_end_message(player.user)

      # ----- First Dawn -----
      # Start dawn
      await self.make_dawn()

      # Base dawn length
      await asyncio.sleep(INCREMENT)

      # Increment (dawn)
      for _ in range(2):
         if self.has_received_all_expected_dawn_actions():
            break
         await asyncio.sleep(INCREMENT)

      # ----- First Day -----
      # Start day
      await self.make_daybreak()

      # Base day length
      base_day_length = math.sqrt(self.nb_players)
      base_day_length = math.ceil(base_day_length)
      base_day_length = base_day_length * 60
      await asyncio.sleep(base_day_length)

      # Nominations start
      for nomination_countdown in [30, 20, 15, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]:
         await botutils.send_lobby("You have **{}** seconds to nominate.".format(nomination_countdown))
      
      # ----- All other cycles -----

      await self.end_game()
   
   def has_received_all_expected_dawn_actions(self):
      return False
   
   def has_received_all_expected_night_actions(self):
      return False
   
   def has_reached_wincon(self):
      """Check if the game has reached win con. Return True if yes, else no."""
      return False

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
      self._chrono.next()
      await botutils.send_lobby(nightfall + " https://imgur.com/QPLPKKw")
   
   async def make_dawn(self):
      """Transition the game into dawn/interlude phase"""
      self._chrono.next()
      await botutils.send_lobby(dawn + " https://imgur.com/vkd747Q")

   async def make_daybreak(self):
      """Transition the game into day phase"""
      self._chrono.next()
      await botutils.send_lobby(daybreak + " https://imgur.com/ic6402z")

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
        globvars.logging.info(f"Sitting Order {str(self._sitting_order)}")
    
   def __repr__(self):
      return "BOTC Game Object"
