import discord
import configparser
import json
import logging
from discord.ext import tasks
from discord.ext import commands

Config = configparser.ConfigParser()
Config.read("config.INI")

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

client = commands.Bot(command_prefix=PREFIX, owner_id=OWNER_ID)
logging.basicConfig(level=logging.WARNING)

extensions = ["Fun", "Gameplay", "Info"]

from gamemodes.troublebrewing import Imp

print(Imp()._instr_string)
print(Imp()._team)
print(Imp()._gm_of_appearance)

print(ADMINS_ID)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    print(f"Bot ID {client.user.id}")
    print("----------")

if __name__ == "__main__":
    for extension in extensions:
        client.load_extension(f"cogs.{extension}")
    client.run(TOKEN)