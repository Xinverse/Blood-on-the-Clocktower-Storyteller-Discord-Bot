"""Contains the Virgin Character class"""

import json 
import botutils
from botc import Townsfolk, Character, NonRecurringAction, Inventory, Flags, Category
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.virgin.value.lower()]

with open('botc/game_text.json') as json_file: 
    documentation = json.load(json_file)
    immediately_executed = documentation["gameplay"]["immediately_executed"]


class Virgin(Townsfolk, TroubleBrewing, Character, NonRecurringAction):
    """Virgin: The 1st time you are nominated, if the nominator is a Townsfolk, 
    they are executed immediately.

    ===== VIRGIN ===== 

    true_self = virgin
    ego_self = virgin
    social_self = virgin

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
        Townsfolk.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        self._brief_string = character_text["brief"]
        self._action = character_text["action"]
                            
        self._art_link = "https://bloodontheclocktower.com/wiki/images/5/5e/Virgin_Token.png"
        self._art_link_cropped = "https://imgur.com/1RiN6lr.png"
        self._wiki_link = "https://bloodontheclocktower.com/wiki/Virgin"

        self._role_enum = TBRole.virgin
        self._emoji = "<:tbvirgin:739317351173980201>"

        self.inventory = Inventory(
            Flags.virgin_first_nomination,
            Flags.slayer_unique_attempt
        )

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
    
    async def on_being_nominated(self, nominator_player, virgin_player):
        """Function that runs after the player is nominated.
        Override the parent Character class' implementation which is to do nothing.
        """
        import globvars

        assert virgin_player.role.true_self.name == self.name, \
            f"The nominated player's role is {virgin_player.role.true_self.name} instead of Virgin"
        
        # Virgin ability is active
        if virgin_player.is_alive() and not virgin_player.is_droisoned():
            if virgin_player.role.true_self.inventory.has_item_in_inventory(Flags.virgin_first_nomination):
                # Remove the unique use ability from the player's inventory
                virgin_player.role.true_self.inventory.remove_item_from_inventory(Flags.virgin_first_nomination)
                # The nominator player registers as a new social self
                nominator_player.role.set_new_social_self(nominator_player)
                if nominator_player.role.social_self.category == Category.townsfolk:
                    msg = immediately_executed.format(
                        botutils.BotEmoji.guillotine,
                        nominator_player.game_nametag
                    )
                    await nominator_player.role.true_self.on_being_executed(nominator_player)
                    await botutils.send_lobby(msg)
                    import botc.switches
                    botc.switches.master_proceed_to_night = True
                    return 

        from botc.gameloops import nomination_loop
        nomination_loop.start(globvars.master_state.game, nominator_player, virgin_player)
