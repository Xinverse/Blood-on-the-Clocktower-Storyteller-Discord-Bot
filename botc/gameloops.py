"""Contains game loop functions"""

import botutils
import asyncio
import math
import traceback
import json
import discord
import datetime
import configparser
from botc import ChoppingBlock
from discord.ext import tasks

Config = configparser.ConfigParser()
Config.read("preferences.INI")

# Lengths
BASE_NIGHT = int(Config["botc"]["BASE_NIGHT"])
NIGHT_MULTIPLER = int(Config["botc"]["NIGHT_MULTIPLER"])
BASE_DAWN = int(Config["botc"]["BASE_DAWN"])
DAWN_MULTIPLIER = int(Config["botc"]["DAWN_MULTIPLIER"])
VOTE_TIMEOUT = int(Config["botc"]["VOTE_TIMEOUT"])
DELETE_VOTE_AFTER = int(Config["botc"]["DELETE_VOTE_AFTER"])
DEBATE_TIME = int(Config["botc"]["DEBATE_TIME"])
INCREMENT = int(Config["botc"]["INCREMENT"])

# Colors
CARD_LYNCH = Config["colors"]["CARD_LYNCH"]
CARD_LYNCH = int(CARD_LYNCH, 16)
CARD_NO_LYNCH = Config["colors"]["CARD_NO_LYNCH"]
CARD_NO_LYNCH = int(CARD_NO_LYNCH, 16)

# Config
Config.read("config.INI")

PREFIX = Config["settings"]["PREFIX"]

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)
    clockface = documentation["images"]["clockface"]
    approved_seal = documentation["images"]["approved_seal"]
    denied_seal = documentation["images"]["denied_seal"]
    ghost_vote_url = documentation["images"]["ghost_vote"]
    blank_token_url = documentation["images"]["blank_token"]
    alive_lynch = documentation["images"]["alive_lynch"]
    alive_no_lynch = documentation["images"]["alive_no_lynch"]
    dead_lynch = documentation["images"]["dead_lynch"]
    dead_no_lynch = documentation["images"]["dead_no_lynch"]
    call_for_vote = documentation["gameplay"]["call_for_vote"]
    votes_stats = documentation["gameplay"]["votes_stats"]
    votes_to_exe = documentation["gameplay"]["votes_to_exe"]
    votes_to_tie = documentation["gameplay"]["votes_to_tie"]
    votes_current = documentation["gameplay"]["votes_current"]
    voted_yes = documentation["gameplay"]["voted_yes"]
    voted_no = documentation["gameplay"]["voted_no"]
    verdict_chopping = documentation["gameplay"]["verdict_chopping"]
    verdict_safe = documentation["gameplay"]["verdict_safe"]
    nomination_intro = documentation["gameplay"]["nomination_intro"]
    vote_summary = documentation["gameplay"]["vote_summary"]
    nomination_short = documentation["gameplay"]["nomination_short"]
    nominations_open = documentation["gameplay"]["nominations_open"]
    nomination_countdown = documentation["gameplay"]["nomination_countdown"]
    day_over_soon = documentation["gameplay"]["day_over_soon"]
    no_execution = documentation["gameplay"]["no_execution"]
    execution = documentation["gameplay"]["execution"]
    copyrights_str = documentation["misc"]["copyrights"]

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)
    error_str = language["system"]["error"]

global botc_game_obj


@tasks.loop(count = 1)
async def nomination_loop(game, nominator, nominated):
    """One round of nomination. Iterate through all players with available 
    votes and register votes using reactions.

    A vote results in an execution if the number of votes equals or exceeds 
    half the number of alive players.
    """

    intro_msg = nomination_intro.format(
        botutils.BotEmoji.demonhead,
        botutils.make_alive_ping(),
        nominator.user.mention, 
        nominated.user.mention,
        DEBATE_TIME
    )
    await botutils.send_lobby(intro_msg)

    import globvars

    # Debate time
    await asyncio.sleep(DEBATE_TIME)

    # Counts
    nb_total_players = len(game.sitting_order)
    nb_alive_players = len([player for player in game.sitting_order if player.is_apparently_alive()])
    nb_available_votes = len([player for player in game.sitting_order if player.has_vote()])
    nb_required_votes = math.ceil(nb_alive_players / 2)
    nb_current_votes = 0

    # The starting index is one after the nominated player
    find_nominated = lambda p: p.user.id == nominated.user.id
    nominated_idx = next(i for i, v in enumerate(game.sitting_order) if find_nominated(v))
    start_idx = nominated_idx + 1
    end_idx = start_idx + len(game.sitting_order)

    for i in range(start_idx, end_idx):

        idx = i % len(game.sitting_order)
        player = game.sitting_order[idx]
 
        if player.has_vote():

            link = ghost_vote_url if player.is_apparently_dead() else blank_token_url

            # Construct the message
            author_str = f"{player.user.name}#{player.user.discriminator}, "
            msg = call_for_vote.format(nominated.game_nametag)
            msg += "\n\n"

            # General vote stats
            # 10 players total. 10 players alive. 10 available voters.
            msg += votes_stats.format(
                total = nb_total_players,
                emoji_total = botutils.BotEmoji.people,
                alive = nb_alive_players,
                emoji_alive = botutils.BotEmoji.alive,
                votes = nb_available_votes,
                emoji_votes = botutils.BotEmoji.votes
            )
            msg += "\n"

            # Goal vote stats
            # 【 5 :approved: votes to execute. 】 or 【 5 :approved: votes to tie. 】
            # Someone is already on the chopping block.
            if game.chopping_block:
                msg += votes_to_tie.format(
                    votes = game.chopping_block.nb_votes,
                    emoji = botutils.BotEmoji.approved
                )

            # No one is on the chopping block yet
            else:
                msg += votes_to_exe.format(
                    votes = nb_required_votes,
                    emoji = botutils.BotEmoji.approved
                )
            
            msg += "\n"

            # Current vote stats
            # 【 0 :approved: votes currently. 】
            msg += votes_current.format(
                votes = nb_current_votes,
                emoji = botutils.BotEmoji.approved
            )

            # Create the embed and associated assets
            embed = discord.Embed(description = msg)
            embed.set_author(name = author_str, icon_url=player.user.avatar_url)
            embed.set_thumbnail(url = link)

            # Send the message and add reactions
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
                author_str = f"{player.user.name}#{player.user.discriminator}, "
                msg = voted_no.format(
                    botutils.BotEmoji.denied,
                    nominated.game_nametag
                )
                new_embed = discord.Embed(
                    description = msg,
                    color = CARD_NO_LYNCH
                )
                new_embed.set_author(name = author_str, icon_url=player.user.avatar_url)
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
                    author_str = f"{player.user.name}#{player.user.discriminator}, "
                    msg = voted_yes.format(
                        botutils.BotEmoji.approved,
                        nominated.game_nametag
                    )
                    nb_current_votes += 1
                    player.spend_vote()
                    new_embed = discord.Embed(
                        description = msg,
                        color = CARD_LYNCH
                    )
                    new_embed.set_author(name = author_str, icon_url=player.user.avatar_url)
                    if player.is_apparently_alive():
                        new_embed.set_thumbnail(url = alive_lynch)
                    else:
                        new_embed.set_thumbnail(url = dead_lynch)
                
                # Hand down (no lynch)
                elif str(reaction.emoji) == botutils.BotEmoji.denied:
                    author_str = f"{player.user.name}#{player.user.discriminator}, "
                    msg = voted_no.format(
                        botutils.BotEmoji.denied,
                        nominated.game_nametag
                    )
                    new_embed = discord.Embed(
                        description = msg,
                        color = CARD_NO_LYNCH
                    )
                    new_embed.set_author(name = author_str, icon_url=player.user.avatar_url)
                    if player.is_apparently_alive():
                        new_embed.set_thumbnail(url = alive_no_lynch)
                    else:
                        new_embed.set_thumbnail(url = dead_no_lynch)
                
                await message.edit(embed = new_embed, delete_after = DELETE_VOTE_AFTER)
                await message.clear_reactions()
    
    # ----- The summmary embed message -----

    msg = nomination_short.format(
        nominated.game_nametag,
        nominator.game_nametag
    )
    msg += "\n"

    # General vote stats
    msg += votes_stats.format(
            total = nb_total_players,
            emoji_total = botutils.BotEmoji.people,
            alive = nb_alive_players,
            emoji_alive = botutils.BotEmoji.alive,
            votes = nb_available_votes,
            emoji_votes = botutils.BotEmoji.votes
    )
    msg += "\n"

    # Goal vote stats
    if game.chopping_block:
        msg += votes_to_tie.format(
            votes = game.chopping_block.nb_votes,
            emoji = botutils.BotEmoji.approved
        )
    else:
        msg += votes_to_exe.format(
            votes = nb_required_votes,
            emoji = botutils.BotEmoji.approved
        )
    msg += "\n"

    # Current vote stats
    msg += votes_current.format(
        votes = nb_current_votes,
        emoji = botutils.BotEmoji.approved
    )
    msg += "\n"
    msg += "\n"

    # The vote count has reached execution threshold. 
    if nb_current_votes >= nb_required_votes:
        # Someone is on the chopping block
        if game.chopping_block:
            # Tie: no one is lynched
            if nb_current_votes == game.chopping_block.nb_votes:
                globvars.master_state.game.chopping_block = ChoppingBlock(None, nb_current_votes)
                msg += verdict_safe.format(nominated.game_nametag)
                thumbnail_url = denied_seal
            # This player will replace the person on the chopping block.
            elif nb_current_votes > game.chopping_block.nb_votes:
                globvars.master_state.game.chopping_block = ChoppingBlock(nominated, nb_current_votes)
                msg += verdict_chopping.format(nominated.game_nametag)
                thumbnail_url = approved_seal
            # The player on the chopping block remains there.
            else:
                msg += verdict_safe.format(nominated.game_nametag)
                thumbnail_url = denied_seal
        # No one is on the chopping block currently. 
        # The player is now on the chopping block awaiting death.
        else:
            globvars.master_state.game.chopping_block = ChoppingBlock(nominated, nb_current_votes)
            msg += verdict_chopping.format(nominated.game_nametag)
            thumbnail_url = approved_seal

    # The execution did not pass. The player is safe.
    else:
        msg += verdict_safe.format(nominated.game_nametag)
        thumbnail_url = denied_seal
        
    summary_embed = discord.Embed(description = msg)
    summary_embed.set_author(
        name = vote_summary,
        icon_url = clockface
    )
    summary_embed.set_thumbnail(url = thumbnail_url)
    summary_embed.set_footer(text = copyrights_str)
    summary_embed.timestamp = datetime.datetime.utcnow()
    await botutils.send_lobby(message = None, embed = summary_embed)


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


@tasks.loop(count = 1)
async def base_day_loop(duration):
    """The base day length during which it's not possible to nominate"""
    await asyncio.sleep(duration)


async def day_loop(game):
    """Day loop"""

    import botc.switches

    # Start day
    await game.make_daybreak()
    # Base day length
    base_day_length = math.sqrt(2 * game.nb_players)
    base_day_length = math.ceil(base_day_length)
    base_day_length = base_day_length * 60
    base_day_loop.start(base_day_length)

    for _ in range(base_day_length):
        # The master switch has been turned on. Proceed to the next phase.
        if botc.switches.master_proceed_to_night:
            base_day_loop.cancel()
            return
        await asyncio.sleep(1)

    # Nominations are open
    msg = botutils.BotEmoji.grimoire + " " + nominations_open.format(PREFIX)
    await botutils.send_lobby(msg)

    timers = [90, 60, 45, 30, 20, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]

    for timer in timers:

        msg = botutils.BotEmoji.grimoire + " " + nomination_countdown.format(timer)
        await botutils.send_lobby(msg)

        countdown = timer
        count = 0

        while not nomination_loop.is_running():
            
            # The master switch has been turned on. Proceed to the next phase.
            if botc.switches.master_proceed_to_night:
                return

            count += 1
            await asyncio.sleep(1)

            # Give a time remaining reminder
            remaining_time = countdown - count
            if remaining_time == 10:
                msg = botutils.BotEmoji.hourglass + " " + day_over_soon
                await botutils.send_lobby(msg)

            # Time has run out
            if count >= countdown:
                if game.chopping_block:
                    if game.chopping_block.player_about_to_die:
                        await game.chopping_block.player_about_to_die.exec_real_death()
                        game.today_executed_player = game.chopping_block.player_about_to_die
                        msg = botutils.BotEmoji.grimoire + " " + execution.format(
                            game.chopping_block.player_about_to_die.game_nametag, 
                            game.chopping_block.nb_votes
                        )
                    else:
                        msg = botutils.BotEmoji.grimoire + " " + no_execution
                    await botutils.send_lobby(msg)
                else:
                    msg = botutils.BotEmoji.grimoire + " " + no_execution
                    await botutils.send_lobby(msg)
                return

        while nomination_loop.is_running():

            # The master switch has been turned on. Proceed to the next phase.
            if botc.switches.master_proceed_to_night:
                return

            await asyncio.sleep(1)


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
    while True:
        # Night
        await night_loop(game_obj)
        # Dawn
        await dawn_loop(game_obj)
        # Day
        await day_loop(game_obj)
    

@master_game_loop.after_loop
async def after_master_game_loop():
    global botc_game_obj
    await botc_game_obj.end_game()


@master_game_loop.error
async def master_loop_error(error):
    """Handler of exceptions in master game loop"""

    try:
        raise error
    except Exception:
        await botutils.send_lobby(error_str)
        await botutils.log(botutils.Level.error, traceback.format_exc())
    finally:
        master_game_loop.cancel()
