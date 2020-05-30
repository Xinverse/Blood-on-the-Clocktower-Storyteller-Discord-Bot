# TODO
# Catch invalid command exceptions
# Discord messages of more than 2000 letters
# Game object

import configparser
import json
import logging
from discord.ext import commands
from botutils import MasterState

# Globals
master_state = MasterState()

if __name__ == "__main__":

    Config = configparser.ConfigParser()
    Config.read("config.INI")

    TOKEN = Config["secret"]["TOKEN"]
    OWNER_ID = Config["user"]["OWNER_ID"]
    PREFIX = Config["settings"]["PREFIX"]

    client = commands.Bot(command_prefix=PREFIX, owner_id=OWNER_ID)
    logging.basicConfig(level=logging.WARNING)

    extensions = ["Admin", "Fun", "Gameplay", "Info", "listeners"]

    for extension in extensions:
        client.load_extension(f"cmd.{extension}")

    client.run(TOKEN)
