import configparser
import json
import time
import logging
from discord.ext import commands

Config = configparser.ConfigParser()
Config.read("config.INI")

TOKEN = Config["secret"]["TOKEN"]
OWNER_ID = Config["user"]["OWNER_ID"]
PREFIX = Config["settings"]["PREFIX"]

client = commands.Bot(command_prefix=PREFIX, owner_id=OWNER_ID)
logging.basicConfig(level=logging.WARNING)

bootTime = time.time()

extensions = ["Fun", "Gameplay", "Info"]

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    print(f"Bot ID {client.user.id}")
    print("----------")

if __name__ == "__main__":
    for extension in extensions:
        client.load_extension(f"cogs.{extension}")
    client.run(TOKEN)