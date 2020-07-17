"""

STORYTELLER BOT
-------------------------
[2020] Code by Xinverse

NOTICE: The copyrights of the games belong to their respective holders, 
unless otherwise specified. This project is an independent adaptation 
of commercial board games into Discord bot format; the Developer is not 
affiliated with them in any way. 

"""

import globvars
import configparser
import botc
import json
import botutils
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

    # The help command
    with open('botutils/bot_text.json') as json_file: 
        language = json.load(json_file)

    help_command = commands.DefaultHelpCommand(
        verify_checks = False, 
        show_hidden = False,
        dm_help = None,
        dm_help_threshold = 700,
        no_category = language["system"]["others_cog"],
        command_attrs = {
            "brief" : language["doc"]["help"]["brief"],
            "help" : language["doc"]["help"]["help"],
            "description" : language["doc"]["help"]["description"]
        }
    )

    # The bot
    globvars.client = commands.Bot(
        command_prefix = command_prefix, 
        owner_id = int(OWNER_ID), 
        case_insensitive = True, 
        description = "〘 Blood on the Clocktower Storyteller Bot 〙 - by Xinverse#4011",
        paginator = commands.Paginator(),
        help_command = help_command
    )

    globvars.client.add_check(botutils.check_if_not_ignored)
    botutils.rate_limit_commands.start()

    # Loading game packs
    print("===== LOADING GAME PACKS =====")
    botc.load_pack(globvars.master_state)
    print(globvars.master_state.game_packs)

    extensions = ["admin", "gameplay", "miscellaneous", "listeners"]

    # Loading command extensions
    print("===== LOADING COMMAND EXTENSIONS =====")

    for extension in extensions:
        globvars.client.load_extension(f"cmd.{extension}")
        print(f"> {extension} cog successfully loaded")

    print("===== LOGGING IN =====")
    globvars.client.run(TOKEN)
