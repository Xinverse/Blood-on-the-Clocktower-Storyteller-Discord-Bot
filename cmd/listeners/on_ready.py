"""Contains the on_ready event listener"""

import configparser
import json
import csv
import botutils
from discord.ext import commands

Config = configparser.ConfigParser()
Config.read("config.INI")

SERVER_ID = Config["user"]["SERVER_ID"]
LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]
ALIVE_ROLE_ID = Config["user"]["ALIVE_ROLE_ID"]
DEAD_ROLE_ID = Config["user"]["DEAD_ROLE_ID"]

with open('botutils/bot_text.json') as json_file:
    language = json.load(json_file)

restart_msg = language["system"]["restart"]
restarted_notify_msg = language["system"]["restarted_notify"]


class on_ready(commands.Cog):
    """Event listener on_ready"""
    
    def __init__(self, client):
        self.client = client
      
    @commands.Cog.listener()
    async def on_ready(self):
        """On_ready event"""

        import globvars

        # Import the ignore data from csv file
        globvars.ignore_list.clear()

        with open('ignore.csv', mode = 'r') as ignore_file:
            csv_reader = csv.reader(ignore_file, delimiter = ',')
            for row in csv_reader:
                globvars.ignore_list = [int(item) for item in row]
                break
        
        # Import the notify data from csv file
        globvars.notify_list.clear()

        with open('notify.csv', mode = 'r') as notify_file:
            csv_reader = csv.reader(notify_file, delimiter = ',')
            for row in csv_reader:
                globvars.notify_list = [int(item) for item in row]
                break
        
        # Start the backup loop
        botutils.backup_loop.start()

        # Print the login message in console
        print(f"Logged in as {self.client.user.name}")
        print(f"Bot ID {self.client.user.id}")
        print("----------")

        # Start cycling playing message
        botutils.cycling_bot_status.start()

        # Send the message in log
        await botutils.log(botutils.Level.info, restart_msg)

        pings = []

        alive_role = globvars.client.get_guild(int(SERVER_ID)).get_role(int(ALIVE_ROLE_ID))
        dead_role = globvars.client.get_guild(int(SERVER_ID)).get_role(int(DEAD_ROLE_ID))

        num_alive = len(alive_role.members)
        num_dead = len(dead_role.members)

        if num_alive:
            pings.append(botutils.make_role_ping(ALIVE_ROLE_ID))
        if num_dead:
            pings.append(botutils.make_role_ping(DEAD_ROLE_ID))
        if pings:
            lobby_channel = globvars.client.get_channel(int(LOBBY_CHANNEL_ID))
            await lobby_channel.send(restarted_notify_msg.format(" ".join(pings)))

        for player in alive_role.members:
            await botutils.remove_alive_role(player)
        for player in dead_role.members:
            await botutils.remove_dead_role(player)

        await botutils.unlock_lobby()


def setup(client):
    client.add_cog(on_ready(client))
