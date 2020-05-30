"""Contains other helper functions"""

import configparser

Config = configparser.ConfigParser()
Config.read("config.INI")

SERVER_ID = Config["user"]["SERVER_ID"]

def make_ping(userid):
    """Turn a user ID into a ping"""
    return f"<@{userid}>"

def strip_ping(raw):
    """Strip a ping to get the user ID"""
    return raw.strip("<@!>")

def get_member_obj(client, userid):
    """Get the member object from the user ID"""
    return client.get_guild(int(SERVER_ID)).get_member(int(userid))

def get_user_obj(client, userid):
    """Get the user object from the user ID"""
    return client.get_user(int(userid))
