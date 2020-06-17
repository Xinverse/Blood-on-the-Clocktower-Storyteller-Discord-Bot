"""Contains the cog for BoTC in-game commands"""

from discord.ext import commands
from botc import BOTCUtils
import globvars


def check_if_can_serve(ctx):
    """Can serve: butler"""
    pass


def check_if_can_poison(ctx):
    """Can poison: poisoner"""
    pass


def check_if_can_learn(ctx):
    """Can learn: ravenkeeper"""
    pass


def check_if_can_read(ctx):
    """Can read: fortune teller"""
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


def check_if_is_day(ctx):
    """Check if the game is in day phase"""
    pass


def check_if_dm(ctx):
    """Check if the command is invoked in a dm channel."""
    return ctx.guild is None


def check_if_lobby(ctx):
    """Check if the command is invoked in the lobby."""
    pass


def check_if_player_alive(ctx):
    """Check if the player is alive"""
    pass


class BoTCCommands(commands.Cog, name="BoTC in-game commands"):
    """BoTC in-game commands cog
    (privilege one unique command keyword per character ability)

    Ability commands:
    - serve: butler
    - poison: poisoner
    - learn: ravenkeeper
    - read: fortune teller
    - kill: imp
    - slay: slayer
    - protect: monk

    Day commands:
    - nominate
    - yes
    - no
    """
    
    def __init__(self, client):
        self.client = client
    

    # ---------- SERVE COMMAND (Butler) ----------------------------------------
    @commands.command(pass_context=True, name = "serve")
    @commands.check(check_if_can_serve)
    @commands.check(check_if_dm)
    @commands.check(check_if_is_night)
    @commands.check(check_if_player_alive)
    async def serve(self, ctx):
        pass


    # ---------- POISON COMMAND (Poisoner) ----------------------------------------
    @commands.command(pass_context=True, name = "poison")
    @commands.check(check_if_can_poison)
    @commands.check(check_if_dm)
    @commands.check(check_if_is_night)
    @commands.check(check_if_player_alive)
    async def poison(self, ctx):
        pass


    # ---------- LEARN COMMAND (Ravenkeeper) ----------------------------------------
    @commands.command(pass_context=True, name = "learn")
    @commands.check(check_if_can_learn)
    @commands.check(check_if_dm)
    @commands.check(check_if_is_night)
    @commands.check(check_if_player_alive)
    async def learn(self, ctx):
        pass


    # ---------- READ COMMAND (Fortune Teller) ----------------------------------------
    @commands.command(pass_context=True, name = "read")
    @commands.check(check_if_can_read)
    @commands.check(check_if_dm)
    @commands.check(check_if_is_night)
    @commands.check(check_if_player_alive)
    async def read(self, ctx):
        pass


    # ---------- KILL COMMAND (Imp) ----------------------------------------
    @commands.command(pass_context=True, name = "kill")
    @commands.check(check_if_can_kill)
    @commands.check(check_if_dm)
    @commands.check(check_if_is_night)
    @commands.check(check_if_player_alive)
    async def kill(self, ctx):
        pass


    # ---------- SLAY COMMAND (Slayer) ----------------------------------------
    @commands.command(pass_context=True, name = "slay")
    @commands.check(check_if_can_slay)
    @commands.check(check_if_lobby)
    @commands.check(check_if_is_day)
    @commands.check(check_if_player_alive)
    async def slay(self, ctx):
        pass


    # ---------- PROTECT COMMAND (Monk) ----------------------------------------
    @commands.command(pass_context=True, name = "protect")
    @commands.check(check_if_can_protect)
    @commands.check(check_if_dm)
    @commands.check(check_if_is_night)
    @commands.check(check_if_player_alive)
    async def protect(self, ctx):
        pass
    

    # ---------- NOMINATE COMMAND (Voting) ----------------------------------------
    @commands.command(pass_context=True, name = "nominate", aliases = ["nom", "nomination"])
    @commands.check(check_if_lobby)
    @commands.check(check_if_is_day)
    async def nominate(self, ctx):
        pass

    
    # ---------- YES COMMAND (Voting) ----------------------------------------
    @commands.command(pass_context=True, name = "yes", aliases = ["y"])
    @commands.check(check_if_lobby)
    @commands.check(check_if_is_day)
    async def yes(self, ctx):
        pass
    

    # ---------- NO COMMAND (Voting) ----------------------------------------
    @commands.command(pass_context=True, name = "no", aliases = ["n"])
    @commands.check(check_if_lobby)
    @commands.check(check_if_is_day)
    async def no(self, ctx):
        pass

    
def setup(client):
    client.add_cog(BoTCCommands(client))
