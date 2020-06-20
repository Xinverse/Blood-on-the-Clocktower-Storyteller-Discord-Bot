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

    send first night instruction? -> FALSE
    """

    def __init__(self):
        
        Character.__init__(self)
        TroubleBrewing.__init__(self)
        Minion.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/3/31/Spy_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Spy"

        self._role_enum = TBRole.spy
        self._emoji = "<:spy2:722687672002543656>"
    
    @property
    def social_self(self):
        """Social self: what the other players think he is.
        The spy may register as a townsfolk, an outsider, or as spy.
        """
        possibilities = [role_class() for role_class in TroubleBrewing.__subclasses__() 
                         if issubclass(role_class, Townsfolk) or issubclass(role_class, Outsider)]
        possibilities.append(Spy())
        random.shuffle(possibilities)
        return random.choice(possibilities)
    
    async def send_first_night_instruction(self, recipient):
        """Send demon and minion list if there are 7 or more players. 
        Otherwise, send the default instruction string.
        """
        # Seven or more players, send the evil list
        if globvars.master_state.game.nb_players >= 7:
            msg1 = globvars.master_state.game.setup.create_evil_team_string()
            msg2 = self.emoji + " " + self.instruction
            msg = msg1 + msg2
            try:
                await recipient.send(msg)
            except discord.Forbidden:
                pass
        # Less than seven players, teensyville rules
        else:
            msg = self.emoji + " " + self.instruction
            try:
                await recipient.send(msg)
            except discord.Forbidden:
                pass
