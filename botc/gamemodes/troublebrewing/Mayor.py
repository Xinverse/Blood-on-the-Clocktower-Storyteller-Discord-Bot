"""Contains the Mayor Character class"""

import json 
import random
from botc import Townsfolk, Character, NonRecurringAction, Category, Team, StatusList
from ._utils import TroubleBrewing, TBRole

with open('botc/gamemodes/troublebrewing/character_text.json') as json_file: 
    character_text = json.load(json_file)[TBRole.mayor.value.lower()]


class Mayor(Townsfolk, TroubleBrewing, Character, NonRecurringAction):
    """Mayor: If only 3 players live and no execution occurs, your team wins. If you die at night, 
    another player might die instead.

    ===== MAYOR ===== 

    true_self = mayor
    ego_self = mayor
    social_self = mayor

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
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/c/c4/Mayor_Token.png"
        self._art_link_cropped = "https://imgur.com/o6keIRB.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Mayor"

        self._role_enum = TBRole.mayor
        self._emoji = "<:mayor:722687261879304214>"

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
    
    async def on_being_demon_killed(self, killed_player):
        """Function that runs after the player has been killed by the demon at night.
        Overriding the parent behaviour. 
        This implements the star passing mechanic.
        """
        if killed_player.is_alive():
            import globvars
            # Tha mayor ability, for now, works 100% of the time if the mayor is 
            # not droisoned, unless all surviving players cannot die from demon.
            if not killed_player.is_droisoned():
                possibilities = [player for player in globvars.master_state.game.sitting_order \
                    if player.is_alive() and \
                        player.role.category != Category.demon and \
                        player.user.id != killed_player.user.id and \
                        not player.has_status_effect(StatusList.safety_from_demon)]
                if possibilities:
                    deflected_to = random.choice(possibilities)
                    await deflected_to.role.true_self.on_being_demon_killed(deflected_to)
                # All the surviving players cannot die from demon, the mayor must die.
                else:
                    await killed_player.exec_real_death()
                    globvars.master_state.game.night_deaths.append(killed_player)
            # If the mayor is droisoned, then the mayor dies as usual.
            else:
                await killed_player.exec_real_death()
                globvars.master_state.game.night_deaths.append(killed_player)
    
    def check_wincon_after_day(self, mayor_player):
        """The good team wins if no one has been executed today, 
        and if the mayor is alive and healthy
        """
        import globvars
        from botc.gameloops import master_game_loop

        if mayor_player.is_alive() and not mayor_player.is_droisoned():
            if globvars.master_state.game.nb_alive_players == 3:
                if not globvars.master_state.game.today_executed_player:
                    globvars.master_state.game.winners = Team.good
                    if master_game_loop.is_running():
                        master_game_loop.cancel()
