"""Playtest command cog"""

import botutils
from ._admin import Admin
from discord.ext import commands


class Playtest(Admin):
    """Playtest command"""

    # ---------- PLAYTEST COMMAND ----------------------------------------
    @commands.command(pass_context=True, name = "playtest")
    @commands.check(botutils.check_if_lobby_or_dm_or_admin)
    async def playtest(self, ctx):
        """Playtest command"""
        
        import globvars
        playtesters = [
            600426113285750785,
            606332710989856778,
            635674760247771136,
            614109280508968980,
            270904126974590976
            #159985870458322944,
            #184405311681986560,
            #235088799074484224,
            #460105234748801024,
            #438057969251254293
            ]
        for userid in playtesters:
            globvars.master_state.pregame.safe_add_player(userid)
        globvars.master_state.game = globvars.master_state.game_packs["botc"]["game_obj"]
        await globvars.master_state.game.start_game()
