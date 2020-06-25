"""Contains the Character class"""

import json
import discord
import botutils
import configparser
from .Category import Category
from .Team import Team
import globvars

Config = configparser.ConfigParser()

Config.read("preferences.INI")

TOWNSFOLK_COLOR = Config["colors"]["TOWNSFOLK_COLOR"]
OUTSIDER_COLOR = Config["colors"]["OUTSIDER_COLOR"]
MINION_COLOR = Config["colors"]["MINION_COLOR"]
DEMON_COLOR = Config["colors"]["DEMON_COLOR"]

TOWNSFOLK_COLOR = int(TOWNSFOLK_COLOR, 16)
OUTSIDER_COLOR = int(OUTSIDER_COLOR, 16)
MINION_COLOR = int(MINION_COLOR, 16)
DEMON_COLOR = int(DEMON_COLOR, 16)

Config.read("config.INI")

PREFIX = Config["settings"]["PREFIX"]

with open('botc/game_text.json') as json_file: 
    strings = json.load(json_file)
    copyrights_str = strings["misc"]["copyrights"]
    role_dm = strings["gameplay"]["role_dm"]
    welcome_dm = strings["gameplay"]["welcome_dm"]
    blocked = strings["gameplay"]["blocked"]


class Character:
    """Character class
    Methods starting with "playtest" are used for console game creation for playtesting purposes.
    """
    
    def __init__(self):

        # Parent attributes
        self._main_wiki_link = "http://bloodontheclocktower.com/wiki/Main_Page"  # Main page url -> string
        self._botc_demon_link = "https://bloodontheclocktower.com/img/website/demon-head.png?" \
                              "rel=1589188746616"  # Demon head art url -> string
        self._botc_logo_link = "http://bloodontheclocktower.com/wiki/images/logo.png"  # Logo art url -> string

        # Override by child role class:
        self._desc_string = None
        self._examp_string = None
        self._instr_string = None
        self._lore_string = None
        self._brief_string = None
        self._art_link = None
        self._wiki_link = None
        self._role_enum = None
        self._true_role = self
        self._ego_role = self
        self._social_role = self

        # Override by gamemode class
        self._gm_of_appearance = None
        self._gm_art_link = None

        # Override by category class
        self._category = None
        self._team = None

        # Other
        self._emoji = None
        self._demon_head_emoji = "<:demonhead:722894653438820432>"
    
    async def send_first_night_instruction(self, recipient):
        """Send the first night instruction, which includes first night passive information, 
        and role instructions.
        Default is to send the instruction string.
        Override by child classes.
        """
        msg = self.emoji + " " + self.instruction
        try:
            await recipient.send(msg)
        except discord.Forbidden:
            pass
    
    async def send_regular_night_instruction(self, recipient):
        """Send the recurring night instruction for all subsequent nights except for the first.
        Default is to send nothing.
        Override by child classes.
        """
        pass
    
    def is_good(self):
        """Return True if the character is on the good team, False otherwise"""
        return self.team == Team.good
    
    def is_evil(self):
        """Return True if the character is on the evil team, False otherwise"""
        return self.team == Team.evil
    
    @property
    def true_self(self):
        """Layers of Role Identity:
        1. true_self = what the game uses for win-con computations
        """
        return self._true_role

    @property
    def ego_self(self):
        """Layers of Role Identity:
        2. ego_self = what the player thinks they are
        """
        return self._ego_role

    @property
    def social_self(self):
        """Layers of Role Identity:
        3. social_self = what the other players think the player is
        """
        return self._social_role
    
    def set_new_true_self(self):
        return
    
    def set_new_ego_self(self):
        return
    
    def set_new_social_self(self):
        return
    
    @property
    def emoji(self):
        return self._emoji
    
    @property
    def main_wiki_link(self):
        return self._main_wiki_link
    
    @property
    def botc_demon_link(self):
        return self._botc_demon_link
    
    @property
    def botc_logo_link(self):
        return self._botc_logo_link
    
    @property
    def description(self):
        return self._desc_string
    
    @property
    def examples(self):
        return self._examp_string
    
    @property
    def instruction(self):
        return self._instr_string
    
    @property
    def lore(self):
        return self._lore_string
    
    @property
    def brief(self):
        return self._brief_string
    
    @property
    def art_link(self):
        return self._art_link
    
    @property
    def wiki_link(self):
        return self._wiki_link

    @property
    def name(self):
        return self._role_enum.value
    
    @property
    def gm_of_appearance(self):
        return self._gm_of_appearance
    
    @property
    def gm_art_link(self):
        return self._gm_art_link
    
    @property
    def category(self):
        return self._category
    
    @property
    def team(self):
        return self._team
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name + " Obj"

    def exec_init_setup(self, townsfolk_obj_list, outsider_obj_list, minion_obj_list, demon_obj_list):
        """Allow for roles that change the setup to modify the role list
        Overridden by child classes that do need to modify the setup.
        """
        return [townsfolk_obj_list, outsider_obj_list, minion_obj_list, demon_obj_list] 
    
    def exec_init_role(self, setup):
        """Allow for roles that need to initialize certain status or flags to do so after the setup 
        is generated.
        Overridden by child classes that do need to set flags and initializations.
        """
        return

    async def send_role_card_embed(self, ctx):
        """Create the role card embed object and return it"""

        def make_embed(emote,
                       role_name, 
                       role_category, 
                       card_color, 
                       gm, 
                       gm_art_link, 
                       desc_str, 
                       ex_str, 
                       pic_link, 
                       wiki_link):

            embed = discord.Embed(title = "{} [{}] {}".format(role_name, role_category, emote), 
                                  description = "*{}*".format(self.lore), 
                                  color = card_color)
            embed.set_author(name = "Blood on the Clocktower - {}".format(gm), icon_url = gm_art_link)
            embed.set_thumbnail(url = pic_link)
            embed.add_field(name = ":small_orange_diamond: Description", value = desc_str, inline = False)
            embed.add_field(name = ":small_orange_diamond: Examples", value = ex_str + "\n" + wiki_link, inline = False)
            embed.set_footer(text = copyrights_str)

            return embed

        if self.category == Category.townsfolk:
            color = TOWNSFOLK_COLOR
        elif self.category == Category.outsider:
            color = OUTSIDER_COLOR
        elif self.category == Category.minion:
            color = MINION_COLOR
        elif self.category == Category.demon:
            color = DEMON_COLOR

        gm_art_link = self.gm_art_link if self.gm_art_link else self.botc_logo_link
        pic_link = self.art_link if self.art_link else self.botc_demon_link
        wiki_link = ":paperclip: " + self.wiki_link if self.wiki_link else ":paperclip: " + self.main_wiki_link

        embed = make_embed(self.emoji,
                           self.__str__(), 
                           self.category.value, 
                           color, 
                           self.gm_of_appearance.value, 
                           gm_art_link, 
                           self.description, 
                           self.examples, 
                           pic_link, 
                           wiki_link)
        await ctx.send(embed=embed)
    
    async def send_opening_dm_embed(self, recipient):
        """Create the opening DM (on game start) embed object and return it"""

        if self.ego_self.category == Category.townsfolk:
            color = TOWNSFOLK_COLOR  
        elif self.ego_self.category == Category.outsider:
            color = OUTSIDER_COLOR
        elif self.ego_self.category == Category.minion:
            color = MINION_COLOR
        else:
            color = DEMON_COLOR

        opening_dm = role_dm.format(
            role_name_str = self.ego_self.name,
            category_str = self.ego_self.category.value,
            team_str = self.ego_self.team.value,
            prefix = PREFIX)

        embed = discord.Embed(title = welcome_dm.format(self.ego_self.name.upper()),
                              url = self.ego_self.wiki_link,
                              description=opening_dm, color=color)
        instructions = f"{self.emoji} {self.instruction}"
        embed.add_field(name = "**Instruction**", value = instructions, inline = True)
        embed.set_author(name = "{} Edition - Blood on the Clocktower (BoTC)".format(self.ego_self.gm_of_appearance.value),
                         icon_url = self.ego_self.gm_art_link)
        embed.set_thumbnail(url = self.ego_self.art_link)
        embed.set_footer(text = copyrights_str)

        # If we have an evil team member, send evil list (if 7p or more)
        if globvars.master_state.game.nb_players >= 7:
            if self.is_evil():
                msg = globvars.master_state.game.setup.create_evil_team_string()
                embed.add_field(name = "**Evil Team**", value = msg, inline = True)

        try:
            await recipient.send(embed = embed)
        except discord.Forbidden:
            #await botutils.send_lobby(blocked.format(recipient.mention))
            pass
    
    # -------------------- Character ABILITIES --------------------
    
    async def exec_serve(self, player, targets):
        """Serve command. Override by child classes."""
        raise NotImplementedError

    async def register_serve(self, player, targets):
        """Serve command. Override by child classes"""
        raise NotImplementedError

    async def exec_poison(self, player, targets):
        """Poison command. Override by child classes"""
        raise NotImplementedError

    async def register_poison(self, player, targets):
        """Poison command. Override by child classes"""
        raise NotImplementedError

    async def exec_learn(self, player, targets):
        """Learn command. Override by child classes"""
        raise NotImplementedError

    async def register_learn(self, player, targets):
        """Learn command. Override by child classes"""
        raise NotImplementedError

    async def exec_read(self, player, targets):
        """Read command. Override by child classes"""
        raise NotImplementedError

    async def register_read(self, player, targets):
        """Read command. Override by child classes"""
        raise NotImplementedError

    async def exec_kill(self, player, targets):
        """Kill command. Override by child classes"""
        raise NotImplementedError

    async def register_kill(self, player, targets):
        """Kill command. Override by child classes"""
        raise NotImplementedError

    async def exec_slay(self, player, targets):
        """Slay command. Override by child classes"""
        raise NotImplementedError

    async def register_slay(self, player, targets):
        """Slay command. Override by child classes"""
        raise NotImplementedError

    async def exec_protect(self, player, targets):
        """Protect command. Override by child classes"""
        raise NotImplementedError

    async def register_protect(self, player, targets):
        """Protect command. Override by child classes"""
        raise NotImplementedError
