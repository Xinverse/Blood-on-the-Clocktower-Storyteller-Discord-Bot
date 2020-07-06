"""Contains game loop functions"""

import botutils
import asyncio
import math
from discord.ext import tasks

BASE_NIGHT = 10
NIGHT_MULTIPLER = 1

BASE_DAWN = 15
DAWN_MULTIPLIER = 1

INCREMENT = 5

global botc_game_obj


async def night_loop(game):
    """Night loop
    ----- Night : 
        30 seconds min
        90 seconds max
        At intervals of 15 seconds when all actions are submitted (45, 60, 75)
    """
    # Transition to night fall
    await game.make_nightfall()
    # Base night length
    await asyncio.sleep(BASE_NIGHT)
    # Increment night by small blocks of time if not all players have finished actions
    for _ in range(NIGHT_MULTIPLER):
        if game.has_received_all_expected_night_actions():
            break
        await asyncio.sleep(INCREMENT)
    # End night 1
    if game._chrono.is_night_1():
        await after_night_1(game)
    # End a regular night
    else:
        await after_night(game)


async def dawn_loop(game):
    """Dawn loop
    ----- Dawn : 
        15 seconds min
        30 seconds max
        At intervals of 15 seconds (15, 30)
    """
    # Start dawn
    await game.make_dawn()
    # Base dawn length
    await asyncio.sleep(INCREMENT)
    # Increment (dawn)
    for _ in range(DAWN_MULTIPLIER):
        if game.has_received_all_expected_dawn_actions():
            break
        await asyncio.sleep(INCREMENT)


async def day_loop(game):
    """Day loop"""
    # Start day
    await game.make_daybreak()
    # Base day length
    base_day_length = math.sqrt(game.nb_players)
    base_day_length = math.ceil(base_day_length)
    base_day_length = base_day_length * 60
    await asyncio.sleep(base_day_length)


async def after_night_1(game):
    """Run after night 1 ends. Handle the night 1 end."""
    # Send n1 end messages
    for player in game.sitting_order:
        await player.role.ego_self.send_n1_end_message(player.user)


async def after_night(game):
    """Run after a regular (not the first) night ends. Handle the regular night end."""
    for player in game.sitting_order:
        await player.role.ego_self.send_regular_night_end_dm(player.user)


@tasks.loop(count = 1)
async def master_game_loop(game_obj):
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
        At intervals of 15 seconds when all actions are submitted (45, 60, 75)

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
    global botc_game_obj
    botc_game_obj = game_obj
    while not game_obj.has_reached_wincon():
        # Night
        await night_loop(game_obj)
        # Check win con
        if game_obj.has_reached_wincon():
            break
        # Dawn
        await dawn_loop(game_obj)
        # Check win con
        if game_obj.has_reached_wincon():
            break
        # Day
        await day_loop(game_obj)
        # Check win con
        if game_obj.has_reached_wincon():
            break
    

@master_game_loop.after_loop
async def after_master_game_loop():
    global botc_game_obj
    await botc_game_obj.end_game()
