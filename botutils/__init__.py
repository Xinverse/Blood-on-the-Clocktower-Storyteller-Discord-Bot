"""Bot utility functions"""

from .adds import add_alive_role, add_dead_role, remove_alive_role, remove_dead_role, \
    remove_all_alive_roles_pregame, lock_lobby, unlock_lobby, add_admin_role, \
    remove_admin_role, remove_all_alive_dead_roles_after_game
from .BotState import BotState
from .checks import check_if_in_pregame, check_if_not_in_game, check_if_not_in_empty, \
    check_if_lobby_or_dm_or_admin, check_if_lobby_or_spec_or_dm_or_admin, check_if_dm, \
    check_if_admin, check_if_lobby, check_if_not_ignored, return_false, return_true, \
    check_if_is_pregame_player, check_if_spec
from .emoji import BotEmoji
from .GameChooser import GameChooser
from .helpers import make_ping, make_role_ping, strip_ping, get_member_obj, get_user_obj, \
    make_code_block, make_time_string, update_state_machine, find_role_in_all, \
    make_alive_ping, make_dead_ping
from .MasterState import MasterState, StateMachine
from .Pregame import Pregame
from .sends import send_lobby, log, Level, send_pregame_stats
from .tasks import rate_limit_commands, lobby_timeout, after_lobby_timeout, \
    cycling_bot_status, start_votes_timer
