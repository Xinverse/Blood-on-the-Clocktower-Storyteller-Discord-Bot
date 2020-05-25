import discord
import configparser
import json
import logging

Config = configparser.ConfigParser()
Config.read("config.INI")

logging.basicConfig(level=logging.WARNING)

# Secret
TOKEN = Config["secret"]["TOKEN"]

# User
OWNER_ID = Config["user"]["OWNER_ID"]
ADMINS_ID = json.loads(Config["user"]["ADMINS_ID"])
SERVER_ID = Config["user"]["SERVER_ID"]
LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]
LOGGING_CHANNEL_ID = Config["user"]["LOGGING_CHANNEL_ID"]

# Settings
PREFIX = Config["settings"]["PREFIX"]

client = discord.Client()


from gamemodes.troublebrewing import Imp

print(Imp()._instr_string)
print(Imp()._team)
print(Imp()._gm_of_appearance)

print(ADMINS_ID)

client.run(TOKEN)