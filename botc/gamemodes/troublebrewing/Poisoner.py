"""Contains the Poisoner Character class"""

import json 
from botc import Minion, Character
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.poisoner.value.lower()]


class Poisoner(Minion, TroubleBrewing, Character):
    """Poisoner: Each night, choose a player, their ability malfunctions tonight and tomorrow day.

    ===== POISONER ===== 

    true_self = poisoner
    ego_self = poisoner
    social_self = poisoner
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Minion.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/a/af/Poisoner_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Poisoner"

        self._role_enum = TBRole.poisoner
