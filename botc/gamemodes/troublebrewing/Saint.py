"""Contains the Saint Character class"""

import json 
from botc import Outsider, Character
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.saint.value.lower()]


class Saint(Outsider, TroubleBrewing, Character):
    """Saint: If you die by execution, your team loses.

    ===== SAINT ===== 

    true_self = saint
    ego_self = saint
    social_self = saint

    commands:
    - None

    initialize setup? -> NO
    initialize role? -> NO

    ----- First night
    START:
    override first night instruction? -> NO  # default is to send instruction string only

    ----- Regular night
    START:
    override regular night instruction -> NO  # default is to send nothing
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Outsider.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/7/77/Saint_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Saint"

        self._role_enum = TBRole.saint
        self._emoji = "<:saint:722687457946107924>"
