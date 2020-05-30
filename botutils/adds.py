"""Contains functions to handle roles and permissions"""

import configparser
from discord.ext import commands

Config = configparser.ConfigParser()
Config.read("config.INI")

LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]
SERVER_ID = Config["user"]["SERVER_ID"]
ALIVE_ROLE_ID = Config["user"]["ALIVE_ROLE_ID"]
DEAD_ROLE_ID = Config["user"]["DEAD_ROLE_ID"]

class Adds(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    async def add_alive_role(self, member_obj):
        """Grand the alive role to a player"""
        role = self.client.get_guild(int(SERVER_ID)).get_role(int(ALIVE_ROLE_ID))
        await member_obj.add_roles(role)

    async def remove_alive_role(self, member_obj):
        """Remove the alive role to a player"""
        server = self.client.get_guild(int(SERVER_ID))
        role = server.get_role(int(ALIVE_ROLE_ID))
        await member_obj.remove_roles(role)

    async def add_dead_role(self, member_obj):
        """Grant the dead role to a player"""
        role = self.client.get_guild(int(SERVER_ID)).get_role(int(DEAD_ROLE_ID))
        await member_obj.add_roles(role)

    async def remove_dead_role(self, member_obj):
        """Remove the dead role to a player"""
        role = self.client.get_guild(int(SERVER_ID)).get_role(int(DEAD_ROLE_ID))
        await member_obj.remove_roles(role)

    async def lock_lobby(self):
        """Lock the lobby channel to non players"""
        pass

    async def unlock_lobby(self):
        """Unlock the lobby channel to non players"""
        pass

def setup(client):
    client.add_cog(Adds(client))