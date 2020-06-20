"""Contains the Investigator Character class"""

import json 
from botc import Townsfolk, Character
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.investigator.value.lower()]


class Investigator(Townsfolk, TroubleBrewing, Character):
    """Investigator: You start knowing 1 of 2 players is a particular Minion.

    ===== INVESTIGATOR ===== 

    true_self = investigator
    ego_self = investigator
    social_self = investigator

    commands:
    - None

    initialize setup? -> NO
    initialize role? -> NO

    override first night instruction? -> YES  # default is to send instruction string only
                                      => Send passive initial information
    override regular night instruction -> NO  # default is to send nothing
    """

    def __init__(self):

        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/e/ec/Investigator_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Investigator"

        self._role_enum = TBRole.investigator
        self._emoji = "<:investigator:722685830585384971>"
