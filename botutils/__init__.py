"""Bot utility functions"""

from .adds import add_alive_role, add_dead_role, remove_alive_role, remove_dead_role, remove_all_alive_roles_pregame
from .BotState import BotState
from .checks import check_if_in_pregame, check_if_not_in_game, check_if_not_in_empty, check_if_lobby_or_dm_or_admin, check_if_lobby_or_spec_or_dm_or_admin, check_if_dm, check_if_admin, check_if_lobby, check_if_not_ignored, return_false
from .GameMeta import GameMeta
from .helpers import make_ping, make_role_ping, strip_ping, get_member_obj, get_user_obj, make_code_block, make_time_string
from .MasterState import MasterState
from .Pregame import Pregame
from .sends import send_lobby, log, Level, send_pregame_stats
from .testing import TestGame
