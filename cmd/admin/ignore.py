"""ignore command"""

import botutils
import discord
import json
import configparser
from ._admin import Admin
from discord.ext import commands

Config = configparser.ConfigParser()
Config.read("config.INI")

PREFIX = Config["settings"]["PREFIX"]
SERVER_ID = int(Config["user"]["SERVER_ID"])

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)
    add_ignore = language["cmd"]["add_ignore"]
    remove_ignore = language["cmd"]["remove_ignore"]
    already_ignored = language["cmd"]["already_ignored"]
    not_ignored = language["cmd"]["not_ignored"]
    ignore_list_empty = language["cmd"]["ignore_list_empty"]
    people_total = language["cmd"]["people_total"]
    clear_ignore = language["cmd"]["clear_ignore"]
    force_clear = language["cmd"]["force_clear"]
    ignore_sync = language["cmd"]["ignore_sync"]
    

class Ignore(Admin, name = "༺ 𝕬𝖉𝖒𝖎𝖓𝖎𝖘𝖙𝖗𝖆𝖙𝖔𝖗 ༻"):
    """Ignore command"""

    @commands.group(
        pass_context = True, 
        name = "ignore", 
        aliases = ["fignore"],
        brief = language["doc"]["ignore"]["ignore"]["brief"],
        help = language["doc"]["ignore"]["ignore"]["help"],
        description = language["doc"]["ignore"]["ignore"]["description"]
    )
    async def ignore(self, ctx):
        """If no subcommand is invoked, display the list of ignored users"""
        if ctx.invoked_subcommand is None:
            import globvars
            n = len(globvars.ignore_list)
            if n:
                msg = people_total.format(n, botutils.BotEmoji.people)
                msg += "\n"
                for userid in globvars.ignore_list:
                    user = globvars.client.get_user(int(userid))
                    msg += f"**{user.name}**#**{user.discriminator}** `({userid})`"
                    msg += " "
                await ctx.send(msg)
            else:
                await ctx.send(ignore_list_empty)

    @ignore.command(
        pass_context = True,
        name = "add",
        aliases = ["+"],
        brief = language["doc"]["ignore"]["add"]["brief"],
        help = language["doc"]["ignore"]["add"]["help"],
        description = language["doc"]["ignore"]["add"]["description"]
    )
    async def add(self, ctx, *, member: discord.Member):
        """Add a user into the ignore list"""
        import globvars
        if member.id not in globvars.ignore_list:
            globvars.ignore_list.append(member.id)
            msg = add_ignore.format(
                botutils.BotEmoji.check, 
                member.display_name, 
                member.id
            )
            await ctx.send(msg)
        else:
            msg = already_ignored.format(
                ctx.author.mention, 
                botutils.BotEmoji.cross, 
                member.display_name, 
                member.id
            )
            await ctx.send(msg)

    @ignore.command(
        pass_context = True,
        name = "remove",
        aliases = ["-"],
        brief = language["doc"]["ignore"]["remove"]["brief"],
        help = language["doc"]["ignore"]["remove"]["help"],
        description = language["doc"]["ignore"]["remove"]["description"]
    )
    async def remove(self, ctx, *, member: discord.Member):
        """Remove a user from the ignore list"""
        import globvars
        if member.id not in globvars.ignore_list:
            msg = not_ignored.format(
                ctx.author.mention, 
                botutils.BotEmoji.cross, 
                member.display_name, 
                member.id
            )
            await ctx.send(msg)
        else:
            globvars.ignore_list.remove(member.id)
            msg = remove_ignore.format(
                botutils.BotEmoji.check, 
                member.display_name, 
                member.id
            )
            await ctx.send(msg)
    
    @ignore.command(
        pass_context = True,
        name = "sync",
        brief = language["doc"]["ignore"]["sync"]["brief"],
        help = language["doc"]["ignore"]["sync"]["help"],
        description = language["doc"]["ignore"]["sync"]["description"]
    )
    async def sync(self, ctx):
        """Remove users that are not in the server"""
        import globvars
        count = 0
        guild = globvars.client.get_guild(SERVER_ID)
        for userid in globvars.ignore_list:
            if guild.get_member(userid) is None:
                globvars.ignore_list.remove(userid)
                count += 1
        msg = ignore_sync.format(botutils.BotEmoji.check, count)
        await ctx.send(msg)
    
    @ignore.group(
        pass_context = True,
        name = "clear",
        brief = language["doc"]["ignore"]["clear"]["brief"],
        help = language["doc"]["ignore"]["clear"]["help"],
        description = language["doc"]["ignore"]["clear"]["description"]
    )
    async def clear(self, ctx):
        """Clear the ignore list"""
        if ctx.invoked_subcommand is None:
            import globvars
            n = len(globvars.ignore_list)
            if n:
                msg = clear_ignore.format(ctx.author.mention, n, PREFIX)
                await ctx.send(msg)
            else:
                await ctx.send(ignore_list_empty)

    @clear.group(
        pass_context = True,
        name = "--force",
        brief = language["doc"]["ignore"]["--force"]["brief"],
        help = language["doc"]["ignore"]["--force"]["help"],
        description = language["doc"]["ignore"]["--force"]["description"]
    )
    async def force(self, ctx):
        """Force flag for the clear subcommand"""
        import globvars
        globvars.ignore_list.clear()
        msg = force_clear.format(botutils.BotEmoji.check)
        await ctx.send(msg)
