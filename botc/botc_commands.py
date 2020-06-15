"""Contains the cog for BoTC in-game commands"""

from discord.ext import commands


def check_if_can_serve(ctx):
    """Can serve: butler"""
    pass


def check_if_can_learn(ctx):
    """Can learn: ravenkeeper"""
    pass


def check_if_can_read(ctx):
    """Can read: fortune teller"""
    pass


def check_if_can_starpass(ctx):
    """Can starpass: imp"""
    pass


def check_if_can_kill(ctx):
    """Can kill: imp"""
    pass


def check_if_can_slay(ctx):
    """Can slay: slayer"""
    pass


def check_if_can_protect(ctx):
    """Can protect: monk"""
    pass


def check_if_is_night(ctx):
    """Check if the game is in night phase"""
    pass


def check_if_dm(ctx):
    """Check if the command is invoked in a dm channel."""
    return ctx.guild is None


def check_if_lobby(ctx):
    """Check if the command is invoked in the lobby."""
    pass


class BoTCCommands(commands.Cog, name="BoTC in-game commands"):
    """BoTC in-game commands cog"""
    
    def __init__(self, client):
        self.client = client
    

    # ---------- SERVE COMMAND (Butler) ----------------------------------------
    @commands.command(pass_context=True, name = "serve")
    @commands.check(check_if_can_serve)
    @commands.check(check_if_dm)
    async def serve(self, ctx):
        pass


    # ---------- LEARN COMMAND (Ravenkeeper) ----------------------------------------
    @commands.command(pass_context=True, name = "learn")
    @commands.check(check_if_can_learn)
    @commands.check(check_if_dm)
    async def learn(self, ctx):
        pass


    # ---------- READ COMMAND (Fortune Teller) ----------------------------------------
    @commands.command(pass_context=True, name = "read")
    @commands.check(check_if_can_read)
    @commands.check(check_if_dm)
    async def read(self, ctx):
        pass


    # ---------- STARPASS COMMAND (Imp) ----------------------------------------
    @commands.command(pass_context=True, name = "starpass")
    @commands.check(check_if_can_starpass)
    @commands.check(check_if_dm)
    async def starpass(self, ctx):
        pass


    # ---------- KILL COMMAND (Imp) ----------------------------------------
    @commands.command(pass_context=True, name = "kill")
    @commands.check(check_if_can_kill)
    @commands.check(check_if_dm)
    async def kill(self, ctx):
        pass


    # ---------- SLAY COMMAND (Slayer) ----------------------------------------
    @commands.command(pass_context=True, name = "slay")
    @commands.check(check_if_can_slay)
    @commands.check(check_if_lobby)
    async def slay(self, ctx):
        pass


    # ---------- PROTECT COMMAND (Monk) ----------------------------------------
    @commands.command(pass_context=True, name = "protect")
    @commands.check(check_if_can_protect)
    @commands.check(check_if_dm)
    async def protect(self, ctx):
        pass

    
def setup(client):
    client.add_cog(BoTCCommands(client))
