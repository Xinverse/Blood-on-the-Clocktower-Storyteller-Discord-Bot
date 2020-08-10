"""Contains the Assassin Character class"""

import json
from botc import Character, Minion, ActionTypes
from ._utils import BadMoonRising, BMRRole
import globvars

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.assassin.value.lower()]


class Assassin(Minion, BadMoonRising, Character):
    """Assassin: Once per game, at night*, choose a player: they die, even if for some reason they could not.
    """

    def __init__(self):

        Character.__init__(self)
        BadMoonRising.__init__(self)
        Minion.__init__(self)

        self._desc_string = character_text["description"]
        self._examp_string = character_text["examples"]
        self._instr_string = character_text["instruction"]
        self._lore_string = character_text["lore"]
        self._brief_string = character_text["brief"]
        self._action = character_text["action"]

        self._art_link = "http://bloodontheclocktower.com/wiki/images/e/e0/Assassin_Token.png"
        self._art_link_cropped = "https://imgur.com/aiJxUkC.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Assassin"

        self._role_enum = BMRRole.assassin
        self._emoji = "<:assassin:722688859925905419>"
    
    def has_finished_night_action(self, player):
        """Return True if assassin has submitted the assassinate action"""
        
        if player.is_alive():
            # First night, assassin does not act
            if globvars.master_state.game._chrono.is_night_1():
                return True
            current_phase_id = globvars.master_state.game._chrono.phase_id
            received_action = player.action_grid.retrieve_an_action(current_phase_id)
            return received_action is not None and received_action.action_type == ActionTypes.assassinate
        return True