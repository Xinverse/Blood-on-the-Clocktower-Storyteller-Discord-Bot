"""Contains the Fortune Teller Character class"""

import json 
from botc import Townsfolk, Character
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.fortuneteller.value.lower()]

class FortuneTeller(Townsfolk, TroubleBrewing, Character):
    """Fortune Teller: Each night, choose 2 players: you learn if either is a Demon. 
    There is 1 good player that registers falsely to you.

    ===== FORTUNE TELLER ===== 

    true_self = fortune teller
    ego_self = fortune teller
    social_self = fortune teller

    commands:
    - read <player> and <player>
    """
    
    def __init__(self):

        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/3/3a/Fortune_Teller_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Fortune_Teller"

        self._role_enum = TBRole.fortuneteller
        self._emoji = "<:fortuneteller:722687043666313218>"
