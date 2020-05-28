"""Contains the Soldier Character class"""

import json 
from botc import Townsfolk, Character
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.soldier.value.lower()]

class Soldier(Townsfolk, TroubleBrewing, Character):
    """Soldier:
    You are safe from the Demon.
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text[self.name]["description"]
        self._examp_string = character_text[self.name]["examples"]
        self._instr_string = character_text[self.name]["instruction"]
        self._lore_string = character_text[self.name]["lore"]
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/9/9e/Soldier_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Soldier"

        self._role_enum = TBRole.soldier
