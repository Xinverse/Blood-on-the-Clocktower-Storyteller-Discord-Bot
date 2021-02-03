"""Contains the on_ready event listener"""

import configparser
import json
import csv
import sqlite3
import botutils
from discord.ext import commands

Config = configparser.ConfigParser()
Config.read("config.INI")

SERVER_ID = Config["user"]["SERVER_ID"]
LOBBY_CHANNEL_ID = Config["user"]["LOBBY_CHANNEL_ID"]
ALIVE_ROLE_ID = Config["user"]["ALIVE_ROLE_ID"]
DEAD_ROLE_ID = Config["user"]["DEAD_ROLE_ID"]
LOCK_CHANNELS_SPECIAL_ID = json.loads(Config["user"].get("LOCK_CHANNELS_SPECIAL_ID", "[]"))

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

        with sqlite3.connect("data.sqlite3") as db:
            c = db.execute("PRAGMA user_version")
            schema_version, = c.fetchone()

            db.execute("""
            CREATE TABLE IF NOT EXISTS gamestats (
                id INTEGER PRIMARY KEY CHECK (id = 0),
                total_games INTEGER NOT NULL DEFAULT 0,
                good_wins INTEGER NOT NULL DEFAULT 0,
                evil_wins INTEGER NOT NULL DEFAULT 0
            )""")
            db.execute("""
            CREATE TABLE IF NOT EXISTS playerstats (
                user_id INTEGER PRIMARY KEY,
                games INTEGER NOT NULL DEFAULT 0,
                wins INTEGER NOT NULL DEFAULT 0
            )
            """)
            db.execute("""
            INSERT OR IGNORE INTO gamestats (id, total_games, good_wins, evil_wins) VALUES (0, 0, 0, 0)
            """)

            if schema_version < 1:
                print("Performing database migration from version 0 to 1")
                db.execute("ALTER TABLE playerstats ADD good_games INTEGER NOT NULL DEFAULT 0")
                db.execute("ALTER TABLE playerstats ADD good_wins INTEGER NOT NULL DEFAULT 0")
                db.execute("ALTER TABLE playerstats ADD evil_games INTEGER NOT NULL DEFAULT 0")
                db.execute("ALTER TABLE playerstats ADD evil_wins INTEGER NOT NULL DEFAULT 0")
                db.execute("PRAGMA user_version = 1")

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
        for player in alive_role.members + dead_role.members:
            for channel_id in LOCK_CHANNELS_SPECIAL_ID:
                channel = globvars.client.get_channel(int(channel_id))
                await channel.set_permissions(player, view_channel=None)

        await botutils.unlock_lobby()


def setup(client):
    client.add_cog(on_ready(client))
