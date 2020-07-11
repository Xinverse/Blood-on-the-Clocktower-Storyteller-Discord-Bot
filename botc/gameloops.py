"""Contains game loop functions"""

import botutils
import asyncio
import math
import json
import discord
import configparser
from discord.ext import tasks

BASE_NIGHT = 10
NIGHT_MULTIPLER = 1

BASE_DAWN = 15
DAWN_MULTIPLIER = 0

VOTE_TIMEOUT = 7
DELETE_VOTE_AFTER = 45

INCREMENT = 1

Config = configparser.ConfigParser()
Config.read("preferences.INI")

CARD_LYNCH = Config["colors"]["CARD_LYNCH"]
CARD_LYNCH = int(CARD_LYNCH, 16)
CARD_NO_LYNCH = Config["colors"]["CARD_NO_LYNCH"]
CARD_NO_LYNCH = int(CARD_NO_LYNCH, 16)

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)
    ghost_vote_url = documentation["images"]["ghost_vote"]
    blank_token_url = documentation["images"]["blank_token"]
    alive_lynch = documentation["images"]["alive_lynch"]
    alive_no_lynch = documentation["images"]["alive_no_lynch"]
    dead_lynch = documentation["images"]["dead_lynch"]
    dead_no_lynch = documentation["images"]["dead_no_lynch"]

global botc_game_obj


async def nomination_loop(game, nominated):
    """One round of nomination. Iterate through all players with available 
    votes and register votes using reactions.
    """
    import globvars

    for player in game.sitting_order:
        if player.has_vote():

            link = ghost_vote_url if player.is_apparently_dead() else blank_token_url
            msg = f"***{player.user.name}#{player.user.discriminator}***, Will you vote for the execution of ---?"
            embed = discord.Embed(description = msg)
            embed.set_thumbnail(url = link)

            message = await botutils.send_lobby(message = player.user.mention, embed = embed)
            await message.add_reaction(botutils.BotEmoji.approved)
            await message.add_reaction(botutils.BotEmoji.denied)

            def check(reaction, user):
                """Reaction must meet these criteria:
                - Must be from the user in question
                - Must be one of the two voting emojis
                - Must be on the same voting call message
                """
                return user.id == player.user.id and \
                    str(reaction.emoji) in (botutils.BotEmoji.approved, botutils.BotEmoji.denied) and \
                    reaction.message.id == message.id
            
            try:
                reaction, user = await globvars.client.wait_for('reaction_add', timeout=VOTE_TIMEOUT, check=check)
                assert user.id == player.user.id, f"{user} reacted instead"
            
            # The player did not vote. It counts as a "No" (hand down)
            except asyncio.TimeoutError:
                new_embed = discord.Embed(
                        description = msg,
                        color = CARD_NO_LYNCH
                    )
                if player.is_apparently_alive():
                    new_embed.set_thumbnail(url = alive_no_lynch)
                else:
                    new_embed.set_thumbnail(url = dead_no_lynch)
                await message.edit(embed = new_embed, delete_after = DELETE_VOTE_AFTER)
                await message.clear_reactions()
                continue

            # The player has voted
            else:

                # Hand up (lynch)
                if str(reaction.emoji) == botutils.BotEmoji.approved:
                    new_embed = discord.Embed(
                        description = msg,
                        color = CARD_LYNCH
                    )
                    if player.is_apparently_alive():
                        new_embed.set_thumbnail(url = alive_lynch)
                    else:
                        new_embed.set_thumbnail(url = dead_lynch)
                
                # Hand down (no lynch)
                elif str(reaction.emoji) == botutils.BotEmoji.denied:
                    new_embed = discord.Embed(
                        description = msg,
                        color = CARD_NO_LYNCH
                    )
                    if player.is_apparently_alive():
                        new_embed.set_thumbnail(url = alive_no_lynch)
                    else:
                        new_embed.set_thumbnail(url = dead_no_lynch)
                
                await message.edit(embed = new_embed, delete_after = DELETE_VOTE_AFTER)
                await message.clear_reactions()


async def night_loop(game):
    """Night loop
    ----- Night : 
        30 seconds min
        90 seconds max
        At intervals of 15 seconds when all actions are submitted (45, 60, 75)
    """
    # Transition to night fall
    await game.make_nightfall()
    # Start night
    if not game._chrono.is_night_1():
        # Night 1 is alraedy handled by the opening dm
        await before_night(game)
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
    # base_day_length = math.sqrt(game.nb_players)
    # base_day_length = math.ceil(base_day_length)
    # base_day_length = base_day_length * 60
    base_day_length = 500
    await asyncio.sleep(base_day_length)


async def before_night(game):
    """Run before a regular (not the first) night starts. Distribute regular night dm."""
    for player in game.sitting_order:
        await player.role.ego_self.send_regular_night_start_dm(player.user)


async def after_night_1(game):
    """Run after night 1 ends. Handle the night 1 end."""
    # Send n1 end messages
    await game.compute_night_ability_interactions()
    for player in game.sitting_order:
        await player.role.ego_self.send_n1_end_message(player.user)


async def after_night(game):
    """Run after a regular (not the first) night ends. Handle the regular night end."""
    await game.compute_night_ability_interactions()
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
