"""Contains functions to handle roles and permissions"""

import configparser

Config = configparser.ConfigParser()
Config.read("config.INI")

LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]
SERVER_ID = Config["user"]["SERVER_ID"]
ALIVE_ROLE_ID = Config["user"]["ALIVE_ROLE_ID"]
DEAD_ROLE_ID = Config["user"]["DEAD_ROLE_ID"]

async def add_alive_role(member_obj):
    """Grand the alive role to a player"""
    from main import client
    role = client.get_guild(int(SERVER_ID)).get_role(int(ALIVE_ROLE_ID))
    await member_obj.add_roles(role)

async def remove_alive_role(member_obj):
    """Remove the alive role to a player"""
    from main import client
    server = client.get_guild(int(SERVER_ID))
    print(server)
    role = server.get_role(int(ALIVE_ROLE_ID))
    await member_obj.remove_roles(role)

async def add_dead_role(member_obj):
    """Grant the dead role to a player"""
    from main import client
    role = client.get_guild(int(SERVER_ID)).get_role(int(DEAD_ROLE_ID))
    await member_obj.add_roles(role)

async def remove_dead_role(member_obj):
    """Remove the dead role to a player"""
    from main import client
    role = client.get_guild(int(SERVER_ID)).get_role(int(DEAD_ROLE_ID))
    await member_obj.remove_roles(role)

async def lock_lobby():
    """Lock the lobby channel to non players"""
    pass

async def unlock_lobby():
    """Unlock the lobby channel to non players"""
    pass
