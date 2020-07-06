"""Contains the Spy Character class"""

import json 
import random
import discord
import asyncio
import datetime
from botc import Minion, Character, Townsfolk, Outsider, NonRecurringAction
from ._utils import TroubleBrewing, TBRole
import globvars

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.spy.value.lower()]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    copyrights_str = strings["misc"]["copyrights"]
    spy_nightly = strings["gameplay"]["spy_nightly"]

GRIMOIRE_SHOW_TIME = 30


class Spy(Minion, TroubleBrewing, Character, NonRecurringAction):
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
    
    def set_new_social_self(self, player):
        """Social self: what the other players think he is.
        The spy may register as a townsfolk, an outsider, or as spy. If dead, the spy will 
        register as spy.
        """

        # Use the real player life/death here. If the player is alive, the spy may register
        # as good, or as spy.
        if player.is_alive():
            possibilities = [role_class() for role_class in TroubleBrewing.__subclasses__() 
                            if issubclass(role_class, Townsfolk) or issubclass(role_class, Outsider)]
            possibilities.append(Spy())
            random.shuffle(possibilities)
            chosen = random.choice(possibilities)
            self._social_role = chosen
            globvars.logging.info(f">>> Spy [social_self] Registered as {chosen}.")
        # If the player is dead, the spy will register as spy.
        else:
            self._social_role = Spy()
            globvars.logging.info(f">>> Spy [social_self] Registered as {Spy()}.")
        
    async def __send_grimoire(self, recipient):
        """Send the spy grimoire"""

        from botc import Grimoire
        try: 
            Grimoire().create(globvars.master_state.game)
        except Exception as e:
            print("Grimoire image was not able to be generated: " + str(e))

        msg = f"***{recipient.name}#{recipient.discriminator}***, the **{self.name}**:"
        msg += "\n"
        msg += self.emoji + " " + self.instruction
        msg += "\n"
        msg += spy_nightly

        embed = discord.Embed(description = msg)
        file = discord.File("botc/assets/grimoire/grimoire.png", filename="grimoire.png")
        embed.set_image(url="attachment://grimoire.png")
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text = copyrights_str)
        try:
            grimoire = await recipient.send(file = file, embed = embed)
        except discord.Forbidden:
            pass
        else:
            await asyncio.sleep(GRIMOIRE_SHOW_TIME)
            await grimoire.delete()
    
    async def send_n1_end_message(self, recipient):
        """Send the spy grimoire"""
        await self.__send_grimoire(recipient)
    
    async def send_regular_night_end_dm(self, recipient):
        """Send the spy grimoire"""
        await self.__send_grimoire(recipient)
