"""

STORYTELLER BOT
-------------------------
[2020] Code by Xinverse

NOTICE: The copyrights of the games belong to their respective holders, 
unless otherwise specified. This project is an independent adaptation 
of commercial board games into Discord bot format; the Developer is not 
affiliated with them in any way. 

"""

# TODO
# BOTC Game object

import configparser
import logging
import botc
import globvars
from discord.ext import commands

if __name__ == "__main__":

    Config = configparser.ConfigParser()
    Config.read("config.INI")

    TOKEN = Config["secret"]["TOKEN"]
    OWNER_ID = Config["user"]["OWNER_ID"]
    PREFIX = Config["settings"]["PREFIX"]

    client = commands.Bot(
        command_prefix=PREFIX, 
        owner_id=OWNER_ID, 
        case_insensitive=True, 
        description="Storyteller Bot"
        )
    logging.basicConfig(level=logging.WARNING)

    print("===== LOADING GAME PACKS =====")
    botc.load_pack(globvars.master_state)
    print(globvars.master_state.game_packs)

    globvars.client = client

    extensions = ["Admin", "Fun", "Gameplay", "Info", "listeners"]

    print("===== LOADING COMMAND EXTENSIONS =====")

    for extension in extensions:
        globvars.client.load_extension(f"cmd.{extension}")
        print(f"> {extension} cog successfully loaded")

    print("===== LOGGING IN =====")
    globvars.client.run(TOKEN)
