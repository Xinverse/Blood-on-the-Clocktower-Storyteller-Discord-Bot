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
# Night interactions
# Lobby game start message: make it look better
# Spy grimoire lookup
# End night information/feedback
# Drunk/poison effect when sending info
# Better log with embed


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
        owner_id=OWNER_ID, 
        case_insensitive=True, 
        description="Storyteller Bot"
        )

    # Loading game packs
    print("===== LOADING GAME PACKS =====")
    botc.load_pack(globvars.master_state)
    print(globvars.master_state.game_packs)

    extensions = ["Admin", "Fun", "Gameplay", "Info", "listeners"]

    # Loading command extensions
    print("===== LOADING COMMAND EXTENSIONS =====")

    for extension in extensions:
        globvars.client.load_extension(f"cmd.{extension}")
        print(f"> {extension} cog successfully loaded")

    print("===== LOGGING IN =====")
    globvars.client.run(TOKEN)
