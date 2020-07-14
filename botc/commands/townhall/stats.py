"""Stats command"""

import traceback
import json
import math
import botutils
from library import fancy
from botc import Phase
from discord.ext import commands

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

error_str = language["system"]["error"]

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)
    current_phase = documentation["gameplay"]["current_phase"]
    stats_tied = documentation["gameplay"]["stats_tied"]
    stats_no_one = documentation["gameplay"]["stats_no_one"]
    stats_chopping = documentation["gameplay"]["stats_chopping"]
    stats_header = documentation["gameplay"]["stats_header"]
    votes_stats = documentation["gameplay"]["votes_stats"]
    stats_1 = documentation["gameplay"]["stats_1"]
    stats_2 = documentation["gameplay"]["stats_2"]
    stats_3 = documentation["gameplay"]["stats_3"]


class Stats(commands.Cog, name = "༺ 𝕭𝖑𝖔𝖔𝖉 𝖔𝖓 𝖙𝖍𝖊 𝕮𝖑𝖔𝖈𝖐𝖙𝖔𝖜𝖊𝖗 ༻ 𝔱𝔬𝔴𝔫𝔥𝔞𝔩𝔩"):
    """BoTC in-game commands cog
    Townsquare command - used for viewing the townsquare image
    """
    
    def __init__(self, client):
        self.client = client
    
    def cog_check(self, ctx):
        """Check the channel of the context, return True if it is sent in either 
        lobby, or in spec chat.
        Admins can bypass.
        """
        return botutils.check_if_admin(ctx) or \
               botutils.check_if_lobby(ctx) or \
               botutils.check_if_spec(ctx)
    
    # ---------- STATS COMMAND (Stats) ----------------------------------------
    @commands.command(
        pass_context = True, 
        name = "stats", 
        hidden = False, 
        brief = documentation["doc"]["stats"]["brief"],
        help = documentation["doc"]["stats"]["help"],
        description = documentation["doc"]["stats"]["description"]
    )
    async def stats(self, ctx):
        """Stats command
        usage: stats
        can be used by all players, spectators in spec-chat or in DM
        """
        import globvars
        game = globvars.master_state.game
        msg = ctx.author.mention
        msg += " "
        msg += stats_header.format(game.nb_players, fancy.bold(game.gamemode.value))
        msg += "\n"
        msg += current_phase.format(fancy.bold(game.current_phase.value))
        msg += "\n"

        if globvars.master_state.game.current_phase == Phase.day:

            chopping_block = globvars.master_state.game.chopping_block
            nb_total_players = len(game.sitting_order)
            nb_alive_players = len([player for player in game.sitting_order if player.is_apparently_alive()])
            nb_available_votes = len([player for player in game.sitting_order if player.has_vote()])

            # Vote stats
            msg += votes_stats.format(
                total = nb_total_players,
                emoji_total = botutils.BotEmoji.people,
                alive = nb_alive_players,
                emoji_alive = botutils.BotEmoji.alive,
                votes = nb_available_votes,
                emoji_votes = botutils.BotEmoji.votes
            )
            msg += "\n"

            if chopping_block:
                player_about_to_die = chopping_block.player_about_to_die
                nb_votes = chopping_block.nb_votes
                if player_about_to_die:
                    msg += stats_chopping.format(player_about_to_die.game_nametag, nb_votes)
                    msg += " "
                    msg += stats_1.format(nb_votes, nb_votes + 1)
                else:
                    msg += stats_tied.format(nb_votes)
                    msg += " "
                    msg += stats_2.format(nb_votes + 1)
            else:
                msg += stats_no_one
                msg += " "
                msg += stats_3.format(math.ceil(nb_alive_players / 2))

        msg += game.create_sitting_order_stats_string()
        await ctx.send(msg)

    @stats.error
    async def stats_error(self, ctx, error):
        # Command on cooldown -> commands.CommandOnCooldown
        if isinstance(error, commands.CheckFailure):
            return
        else:
            try:
                raise error
            except Exception:
                await ctx.send(error_str)
                await botutils.log(botutils.Level.error, traceback.format_exc()) 

def setup(client):
    client.add_cog(Stats(client))
    