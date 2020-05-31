"""Contains other helper functions"""

import configparser
import datetime

Config = configparser.ConfigParser()
Config.read("config.INI")

SERVER_ID = Config["user"]["SERVER_ID"]

def make_ping(userid):
    """Turn a user ID into a ping"""
    return f"<@{userid}>"


def make_role_ping(roleid):
    """Turn a role ID into a ping"""
    return f"<@&{roleid}>"


def strip_ping(raw):
    """Strip a ping to get the user ID"""
    return raw.strip("<@!>")


def get_member_obj(client, userid):
    """Get the member object from the user ID"""
    return client.get_guild(int(SERVER_ID)).get_member(int(userid))


def get_user_obj(client, userid):
    """Get the user object from the user ID"""
    return client.get_user(int(userid))


def make_code_block(msg):
    """Turn a message into a code block"""
    return f"```{msg}```"


def make_time_string(seconds):
    """Turn the number of seconds into a formatted time string"""
    return str(datetime.timedelta(seconds=seconds))