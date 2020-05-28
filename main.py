import configparser
import json
import time
import logging
from discord.ext import commands

bootTime = time.time()

Config = configparser.ConfigParser()
Config.read("config.INI")

TOKEN = Config["secret"]["TOKEN"]
OWNER_ID = Config["user"]["OWNER_ID"]
PREFIX = Config["settings"]["PREFIX"]

client = commands.Bot(command_prefix=PREFIX, owner_id=OWNER_ID)
logging.basicConfig(level=logging.WARNING)

extensions = ["Admin", "Fun", "Gameplay", "Info"]


from botc.gamemodes.troublebrewing import Baron
print(Baron()._lore_string)

if __name__ == "__main__":
    for extension in extensions:
        client.load_extension(f"cmd.{extension}")
    client.run(TOKEN)