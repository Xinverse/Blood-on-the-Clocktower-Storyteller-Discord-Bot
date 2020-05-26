"""Contains the Ravenkeeper Character class"""

from botc import Townsfolk
from ._utils import TroubleBrewing
from ._utils import TBRole

class Ravenkeeper(Townsfolk, TroubleBrewing):
    """Ravenkeeper:
    If you die at night, you are woken to choose a player: you learn their character.
    """
    
    def __init__(self):

        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = "The Ravenkeeper learns any player's character, but only if they die " \
                            "at night.\n" \
                            "- The Ravenkeeper is woken on the night that they die, and chooses a " \
                            "player immediately.\n" \
                            "- The Ravenkeeper may choose a dead player if they wish."
        self._examp_string = "- The Ravenkeeper is killed by the Imp, and then wakes to choose a " \
                             "player. After some deliberation, they choose Benjamin. Benjamin is " \
                             "the Empath, and the Ravenkeeper learns this.\n" \
                             "- The Imp attacks the Mayor. The Mayor doesn't die, but the " \
                             "Ravenkeeper dies instead, due to the Mayor's ability. The " \
                             "Ravenkeeper is woken and chooses Douglas, who is a dead Recluse. " \
                             "The Ravenkeeper learns that Douglas is the Scarlet Woman, since the " \
                             "Recluse registered as a Minion."
        self._instr_string = "If you die at night, you are woken to choose a player: " \
                             "you learn their character."
        self._lore_string = "My birds will avenge me! Fly! Fly, my sweet and dutiful pets! Take " \
                            "your message to those in dark corners! To the manor and to the river! " \
                            "Let them read of the nature of my death."
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/45/Ravenkeeper_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Ravenkeeper"
        
        self._role_name = TBRole.ravenkeeper
        