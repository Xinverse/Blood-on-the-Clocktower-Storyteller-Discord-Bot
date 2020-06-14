"""Contains the Librarian Character class"""

import json 
from botc import Townsfolk, Character
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.librarian.value.lower()]


class Librarian(Townsfolk, TroubleBrewing, Character):
    """Librarian: You start knowing that 1 of 2 players is a particular Outsider.
    (Or that zero are in play)

    ===== LIBRARIAN ===== 

    true_self = librarian
    ego_self = librarian
    social_self = librarian
    """
    
    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/8/86/Librarian_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Librarian"

        self._role_enum = TBRole.librarian
    