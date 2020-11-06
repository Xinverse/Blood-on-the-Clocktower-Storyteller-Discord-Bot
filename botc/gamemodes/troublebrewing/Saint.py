"""Contains the Saint Character class"""

import json 
from botc import Outsider, Character, NonRecurringAction, AlreadyDead, Team
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.saint.value.lower()]


class Saint(Outsider, TroubleBrewing, Character, NonRecurringAction):
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
        self._brief_string = character_text["brief"]
        self._action = character_text["action"]
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/7/77/Saint_Token.png"
        self._art_link_cropped = "https://imgur.com/CKuDBku.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Saint"

        self._role_enum = TBRole.saint
        self._emoji = "<:tbsaint:739317351127711794>"

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
    
    async def on_being_executed(self, executed_player):
        """Funtion that runs after the player has been nominated.
        If a healthy and sober saint is executed, then the game ends with evil win.
        """
        try:
            await executed_player.exec_real_death()
        # The saint is already dead
        except AlreadyDead:
            pass
        # The saint was alive and has been executed
        else:
            if not executed_player.is_droisoned():
                import globvars
                globvars.master_state.game.winners = Team.evil
                from botc.gameloops import master_game_loop
                if master_game_loop.is_running():
                    master_game_loop.cancel()
