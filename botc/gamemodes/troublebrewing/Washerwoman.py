"""Contains the Washerwoman Character class"""

import json 
from botc import Townsfolk, Character
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.washerwoman.value.lower()]


class Washerwoman(Townsfolk, TroubleBrewing, Character):
    """Washerwoman: You start knowing 1 of 2 players is a particular Townsfolk.

    ===== WASHERWOMAN ===== 

    true_self = washerwoman
    ego_self = washerwoman
    social_self = washerwoman

    commands:
    - None
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/4d/Washerwoman_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Washerwoman"

        self._role_enum = TBRole.washerwoman
    
    @property
    def true_self(self):
        """Layers of Role Identity:
        1. true_self = what the game uses for win-con computations
        """
        return Washerwoman()

    @property
    def ego_self(self):
        """Layers of Role Identity:
        2. ego_self = what the player thinks they are
        """
        return Washerwoman()

    @property
    def social_self(self):
        """Layers of Role Identity:
        3. social_self = what the other players think the player is
        """
        return Washerwoman()
