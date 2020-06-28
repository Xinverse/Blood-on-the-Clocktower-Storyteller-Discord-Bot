"""Contains the Drunk Character class"""

import json 
import random
from botc import Outsider, Character, Townsfolk
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.drunk.value.lower()]

class Drunk(Outsider, TroubleBrewing, Character):
    """Drunk: You think you are a Townsfolk, but your ability malfunctions.

    ===== DRUNK ===== 

    true_self = drunk
    ego_self = [townsfolk] *persistent
    social_self = drunk

    commands
    - None

    initialize setup? -> NO
    initialize role? -> YES

    ----- First night
    START:
    override first night instruction? -> NO  # default is to send instruction string only

    ----- Regular night
    START:
    override regular night instruction? -> NO  # default is to send nothing
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Outsider.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        self._brief_string = character_text["brief"]
        self._action = character_text["action"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/0/03/Drunk_Token.png"
        self._art_link_cropped = "https://imgur.com/vWuRgdS.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Drunk"

        self._role_enum = TBRole.drunk
        self._emoji = "<:drunk:722687457828798515>"

    def create_n1_instr_str(self):
        """Create the instruction field on the opening dm card"""

        # First line is the character instruction string
        msg = f"{self.emoji} {self.instruction}"
        addendum = character_text["n1_addendum"]
        
        # Some characters have a line of addendum
        if addendum:
            with open("botutils/bot_text.json") as json_file:
                bot_text = json.load(json_file)
                scroll_emoji = bot_text["esthetics"]["scroll"]
            msg += f"\n{scroll_emoji} {addendum}"
            
        return msg
    
    def exec_init_role(self, setup):
        """Randomly choose a townsfolk that is not in play. (persistent throughout the game)"""
        possibilities = [role_class() for role_class in TroubleBrewing.__subclasses__() if issubclass(role_class, Townsfolk)]
        taken = [player.role.name for player in setup.townsfolks]
        random.shuffle(possibilities)
        for p in possibilities:
            if p.name not in taken:
                self._ego_role = p
                break
        globvars.logging.info(f">>> Drunk [exec_init_role] Initialized ego_self as {self._ego_role}.")
        