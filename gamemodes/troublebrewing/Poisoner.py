"""Contains the Poisoner Character class"""

from botc import Minion
from ._utils import TroubleBrewing
from ._utils import TBRole

class Poisoner(Minion, TroubleBrewing):
    """Poisoner:
    Each night, choose a player, their ability malfunctions tonight and tomorrow day.
    """

    def __init__(self):

        TroubleBrewing.__init__(self)
        Minion.__init__(self)

        self._desc_string = "The Poisoner secretly disrupts character abilities."
        self._examp_string = ""
        self._instr_string = "Each night, choose a player: their ability malfunctions " \
                             "tonight and tomorrow day."
        self._lore_string = ""
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/a/af/Poisoner_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Poisoner"

        self._role_name = TBRole.poisoner
