"""Contains other helper functions"""

import configparser
import datetime
import globvars


Config = configparser.ConfigParser()
Config.read("config.INI")

SERVER_ID = Config["user"]["SERVER_ID"]
ALIVE_ROLE_ID = Config["user"]["ALIVE_ROLE_ID"]
DEAD_ROLE_ID = Config["user"]["DEAD_ROLE_ID"]


def make_ping(userid):
    """Turn a user ID into a ping"""
    return f"<@{userid}>"


def make_role_ping(roleid):
    """Turn a role ID into a ping"""
    return f"<@&{roleid}>"


def make_alive_ping():
    """Ping the @alive role."""
    global ALIVE_ROLE_ID
    return f"<@&{ALIVE_ROLE_ID}>"


def make_dead_ping():
    """Ping the @dead role."""
    global DEAD_ROLE_ID
    return f"<@&{DEAD_ROLE_ID}>"


def strip_ping(raw):
    """Strip a ping to get the user ID"""
    return raw.strip("<@!>")


def get_member_obj(userid):
    """Get the member object from the user ID"""
    return globvars.client.get_guild(int(SERVER_ID)).get_member(int(userid))


def get_user_obj(userid):
    """Get the user object from the user ID"""
    return globvars.client.get_user(int(userid))


def make_code_block(msg):
    """Turn a message into a code block"""
    return f"```{msg}```"


def make_time_string(seconds):
    """Turn the number of seconds into a formatted time string"""
    return str(datetime.timedelta(seconds=seconds))


def update_state_machine():
    """Update the state machine"""
    globvars.master_state.state_machine.run(globvars.master_state)


def find_role_in_all(role_name):
    """
    Find a role name amongst all the loaded game packs. 
    Return the role class if it is found, else return None

    The game_packs variable is coded in the following way:

    {'botc': {'game_obj': <botc.Game.Game object at 0x1187bffd0>, 'gamemodes': {'trouble-brewing': 
    [Baron Obj, Butler Obj, Chef Obj, Drunk Obj, Empath Obj, Fortune Teller Obj, Imp Obj, 
    Investigator Obj, Librarian Obj, Mayor Obj, Monk Obj, Poisoner Obj, Ravenkeeper Obj, 
    Recluse Obj, Saint Obj, Scarlet Woman Obj, Slayer Obj, Soldier Obj, Undertaker Obj, 
    Virgin Obj, Washerwoman Obj]}}}
    """
    for game_pack_title in globvars.master_state.game_packs:
        pack_content = globvars.master_state.game_packs[game_pack_title]
        for gamemode_title in pack_content["gamemodes"]:
            gamemode_content = pack_content["gamemodes"][gamemode_title]
            for role in gamemode_content:
                if role_name.lower() in role.name.lower():
                    return role


