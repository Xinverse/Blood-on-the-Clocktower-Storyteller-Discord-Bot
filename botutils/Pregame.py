"""Contains the Pregame class"""

import globvars
import configparser

Config = configparser.ConfigParser()
Config.read("config.INI")

SERVER_ID = Config["user"]["SERVER_ID"]
SERVER_ID = int(SERVER_ID)

class Pregame:
    """Pregame class: for storing session before game start"""

    def __init__(self):
        self._userid_list = []

    @property
    def list(self):
        """Access the list of user id"""
        self.remove_left_guild_players()
        return self._userid_list
    
    def is_empty(self):
        """Is the pregame lobby empty? (meaning that there are 0 players who have joined)"""
        return len(self._userid_list) == 0

    def add_player(self, userid):
        """Add a player based on its user ID"""
        userid = int(userid)
        if userid not in self._userid_list:
            self._userid_list.append(userid)

    def remove_player(self, userid):
        """Remove a player based on its user ID"""
        userid = int(userid)
        if userid in self._userid_list:
            self._userid_list.remove(userid)
    
    def is_joined(self, userid):
        """Check if a userid is already in self._userid_list"""
        self.remove_left_guild_players()
        userid = int(userid)
        return userid in self._userid_list
    
    def safe_add_player(self, userid):
        """Add a player based on its user ID only if the player has not joined"""
        userid = int(userid)
        if not self.is_joined(userid):
            self.add_player(userid)

    def safe_remove_player(self, userid):
        """Remove a player based on its user ID only if the player has joined"""
        userid = int(userid)
        if self.is_joined(userid):
            self.remove_player(userid)
    
    def clear(self):
        """Clear the user ID list"""
        self.__init__()
    
    def __str__(self):
        return f"Pregame Object with {len(self)} users"

    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        self.remove_left_guild_players()
        return len(self._userid_list)
    
    def __iter__(self):
        self.remove_left_guild_players()
        return iter(self._userid_list)

    def remove_left_guild_players(self):
        for userid in self._userid_list:
            fetched_member = globvars.client.get_guild(SERVER_ID).get_member(int(userid))
            if fetched_member == None:
                #User left server
                self._userid_list.remove(userid)
