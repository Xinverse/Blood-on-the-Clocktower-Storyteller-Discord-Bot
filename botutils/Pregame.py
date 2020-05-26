"""Contains the Pregame class"""

class Pregame:
    """Pregame class: for storing session before game start"""

    def __init__(self):
        self._userid_list = []

    def add_player(self, userid):
        """Add a player based on its user ID"""
        if userid not in self._userid_list:
            self._userid_list.append(userid)

    def remove_player(self, userid):
        """Remove a player based on its user ID"""
        if userid not in self._userid_list:
            self._userid_list.remove(userid)
    
    def clear(self):
        """Clear the user ID list"""
        self.__init__()
    
    def __repr__(self):
        return f"Pregame Object with {len(self)} users"
    
    def __len__(self):
        return len(self._userid_list)
    
    def __iter__(self):
         return iter(self._userid_list)
