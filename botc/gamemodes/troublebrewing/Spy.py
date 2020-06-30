"""Contains the Spy Character class"""

import json 
import random
import discord
from botc import Minion, Character, Townsfolk, Outsider
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.spy.value.lower()]


class Spy(Minion, TroubleBrewing, Character):
    """Spy: The Spy might appear to be a good character, but is actually evil. 
    They also see the Grimoire, so they know the characters (and status) of all players.

    ===== SPY =====

    true_self = spy
    ego_self = spy
    social_self = [townsfolk] / [outsider] / spy *ephemeral

    commands:
    - None

    initialize setup? -> NO
    initialize role? -> NO

    ----- First night
    START:
    override first night instruction? -> YES  # default is to send instruction string only
                                      => Send demon and minion identities to this minion if 7 players or more
    
    ----- Regular night
    START:
    override regular night instruction -> NO  # default is to send nothing
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Minion.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        self._brief_string = character_text["brief"]
        self._action = character_text["action"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/3/31/Spy_Token.png"
        self._art_link_cropped = "https://imgur.com/Je21heV.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Spy"

        self._role_enum = TBRole.spy
        self._emoji = "<:spy2:722687672002543656>"

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
    
    def set_new_social_self(self):
        """Social self: what the other players think he is.
        The spy may register as a townsfolk, an outsider, or as spy.
        """
        possibilities = [role_class() for role_class in TroubleBrewing.__subclasses__() 
                         if issubclass(role_class, Townsfolk) or issubclass(role_class, Outsider)]
        possibilities.append(Spy())
        random.shuffle(possibilities)
        chosen = random.choice(possibilities)
        globvars.logging.info(f">>> Spy [social_self] Registered as {chosen}.")
        self._social_role = chosen
    
    def create_grimoire(self):
        pass
