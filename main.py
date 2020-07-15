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
# Night interactions (left from investigator)
# Investigator minion bug fix
# Night death string in day announcement.
# Master states stability and inter-game state clearing
# Winning conditions and end game message
# Spy grimoire reminder tokens
# Better logging system
# Center text for townsquare


import globvars
import configparser
import botc
from discord.ext import commands


if __name__ == "__main__":

    Config = configparser.ConfigParser()
    Config.read("config.INI")

    TOKEN = Config["secret"]["TOKEN"]
    OWNER_ID = Config["user"]["OWNER_ID"]
    PREFIX = Config["settings"]["PREFIX"]

    globvars.init_client()
    globvars.init_master_state()

    def command_prefix(bot, message):
        if message.guild is None:
            return (PREFIX, "")
        else:
            return PREFIX

    globvars.client = commands.Bot(
        command_prefix=command_prefix, 
        owner_id=int(OWNER_ID), 
        case_insensitive=True, 
        description="Storyteller Bot"
    )

    # Loading game packs
    print("===== LOADING GAME PACKS =====")
    botc.load_pack(globvars.master_state)
    print(globvars.master_state.game_packs)

    extensions = ["Admin", "Fun", "Gameplay", "Info", "listeners", "Owner"]

    # Loading command extensions
    print("===== LOADING COMMAND EXTENSIONS =====")

    for extension in extensions:
        globvars.client.load_extension(f"cmd.{extension}")
        print(f"> {extension} cog successfully loaded")

    print("===== LOGGING IN =====")
    globvars.client.run(TOKEN)
