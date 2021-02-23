"""Contains functions to handle roles and permissions"""

import configparser
import json
import traceback

import discord

import globvars
from .sends import Level, log

Config = configparser.ConfigParser()
Config.read("config.INI")

LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]
SERVER_ID = Config["user"]["SERVER_ID"]
ALIVE_ROLE_ID = Config["user"]["ALIVE_ROLE_ID"]
DEAD_ROLE_ID = Config["user"]["DEAD_ROLE_ID"]
ADMINS_ROLE_ID = Config["user"]["ADMINS_ROLE_ID"]
LOCK_CHANNELS_ID = json.loads(Config["user"].get("LOCK_CHANNELS_ID", "[]"))
LOCK_CHANNELS_SPECIAL_ID = json.loads(Config["user"].get("LOCK_CHANNELS_SPECIAL_ID", "[]"))


async def add_admin_role(user):
    """Grant the admin role to a member"""
    role = globvars.client.get_guild(int(SERVER_ID)).get_role(int(ADMINS_ROLE_ID))
    member_obj = globvars.client.get_guild(int(SERVER_ID)).get_member(user.id)
    if member_obj is not None:
        await member_obj.add_roles(role)


async def remove_admin_role(user):
    """Remove the admin role from a member"""
    role = globvars.client.get_guild(int(SERVER_ID)).get_role(int(ADMINS_ROLE_ID))
    member_obj = globvars.client.get_guild(int(SERVER_ID)).get_member(user.id)
    if member_obj is not None:
        await member_obj.remove_roles(role)


async def add_alive_role(member_obj):
    """Grant the alive role to a player"""
    alive_role = globvars.client.get_guild(int(SERVER_ID)).get_role(int(ALIVE_ROLE_ID))

    # Refetch member from server before proceeding so that we don't accidentally try to give a role to a nonexistent user
    member_obj = globvars.client.get_guild(int(SERVER_ID)).get_member(int(member_obj.id))

    if member_obj is not None:
        await member_obj.add_roles(alive_role)


async def remove_alive_role(member_obj):
    """Remove the alive role from a player"""
    alive_role = globvars.client.get_guild(int(SERVER_ID)).get_role(int(ALIVE_ROLE_ID))

    # Refetch member from server before proceeding so that we don't accidentally try to give a role to a nonexistent user
    member_obj = globvars.client.get_guild(int(SERVER_ID)).get_member(int(member_obj.id))

    if member_obj is not None:
        await member_obj.remove_roles(alive_role)


async def add_dead_role(member_obj):
    """Grant the dead role to a player"""
    dead_role = globvars.client.get_guild(int(SERVER_ID)).get_role(int(DEAD_ROLE_ID))

    # Refetch member from server before proceeding so that we don't accidentally try to give a role to a nonexistent user
    member_obj = globvars.client.get_guild(int(SERVER_ID)).get_member(int(member_obj.id))

    if member_obj is not None:
        await member_obj.add_roles(dead_role)


async def remove_dead_role(member_obj):
    """Remove the dead role from a player"""
    dead_role = globvars.client.get_guild(int(SERVER_ID)).get_role(int(DEAD_ROLE_ID))

    # Refetch member from server before proceeding so that we don't accidentally try to give a role to a nonexistent user
    member_obj = globvars.client.get_guild(int(SERVER_ID)).get_member(int(member_obj.id))

    if member_obj is not None:
        await member_obj.remove_roles(dead_role)


async def remove_all_alive_roles_pregame():
    """Remove the alive roles from all players during pregame"""
    for userid in globvars.master_state.pregame:
        member_obj = globvars.client.get_guild(int(SERVER_ID)).get_member(int(userid))
        await remove_alive_role(member_obj)


async def remove_all_alive_dead_roles_after_game():
    """Remove the alive and the dead roles from all players after the game is over"""
    for player in globvars.master_state.game.sitting_order:
        if player.is_alive():
            await remove_alive_role(player.user)
        else:
            await remove_dead_role(player.user)


async def lock_lobby():
    """Lock the lobby channel from non players"""
    server = globvars.client.get_guild(int(SERVER_ID))

    lobby_channel = globvars.client.get_channel(int(LOBBY_CHANNEL_ID))
    await lobby_channel.set_permissions(server.default_role, send_messages=False)

    alive_role = globvars.client.get_guild(int(SERVER_ID)).get_role(int(ALIVE_ROLE_ID))

    for channel_id in LOCK_CHANNELS_ID:
        channel = globvars.client.get_channel(int(channel_id))
        try:
            await channel.set_permissions(alive_role, view_channel=False)
        except discord.errors.Forbidden:
            await log(Level.warning, f'Unable to lock {channel.mention}')
            await log(Level.error, traceback.format_exc())

    for channel_id in LOCK_CHANNELS_SPECIAL_ID:
        channel = globvars.client.get_channel(int(channel_id))
        try:
            await channel.set_permissions(alive_role, send_messages=False, connect=False)
        except discord.errors.Forbidden:
            await log(Level.warning, f'Unable to lock {channel.mention}')
            await log(Level.error, traceback.format_exc())


async def unlock_lobby():
    """Unlock the lobby channel to non players"""
    server = globvars.client.get_guild(int(SERVER_ID))

    lobby_channel = globvars.client.get_channel(int(LOBBY_CHANNEL_ID))
    await lobby_channel.set_permissions(server.default_role, send_messages=None)

    alive_role = globvars.client.get_guild(int(SERVER_ID)).get_role(int(ALIVE_ROLE_ID))

    for channel_id in LOCK_CHANNELS_ID:
        channel = globvars.client.get_channel(int(channel_id))
        try:
            await channel.set_permissions(alive_role, view_channel=None)
        except discord.errors.Forbidden:
            await log(Level.warning, f'Unable to unlock {channel.mention}')
            await log(Level.error, traceback.format_exc())

    for channel_id in LOCK_CHANNELS_SPECIAL_ID:
        channel = globvars.client.get_channel(int(channel_id))
        try:
            await channel.set_permissions(alive_role, send_messages=None, connect=None)
        except discord.errors.Forbidden:
            await log(Level.warning, f'Unable to unlock {channel.mention}')
            await log(Level.error, traceback.format_exc())
