"""Contains the on_ready event listener"""

import json
import csv
import botutils
import botutils
from discord.ext import commands

with open('botutils/bot_text.json') as json_file: 
    language = json.load(json_file)

restart_msg = language["system"]["restart"]


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

def setup(client):
    client.add_cog(on_ready(client))
