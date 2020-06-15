"""Contains the Drunk Character class"""

import json 
import random
from botc import Outsider, Character, Townsfolk
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.drunk.value.lower()]

class Drunk(Outsider, TroubleBrewing, Character):
    """Drunk: You think you are a Townsfolk, but your ability malfunctions.

    ===== DRUNK ===== 

    true_self = drunk
    ego_self = [townsfolk] *persistent
    social_self = drunk
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Outsider.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/0/03/Drunk_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Drunk"

        self._role_enum = TBRole.drunk

        self.__init_ego_self()
    
    def __init_ego_self(self):
        """Randomly choose a townsfolk. (persistent)
        """
        possibilities = [role_class() for role_class in TroubleBrewing.__subclasses__() if issubclass(role_class, Townsfolk)]
        self._ego_role = random.choice(possibilities)
    
    @property
    def ego_self(self):
        """Ego self: what the player thinks they are.
        The Drunk thinks they are a townsfolk.
        """
        return self._ego_role

        