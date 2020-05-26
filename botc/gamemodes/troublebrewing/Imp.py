"""Contains the Imp Character class"""

from botc import Demon
from ._utils import TroubleBrewing
from ._utils import TBRole

class Imp(Demon, TroubleBrewing):
    """Imp:
    Each night*, choose a player: they die. If you kill yourself this way, a Minion becomes the Imp.
    """

    def __init__(self):
        
        TroubleBrewing.__init__(self)
        Demon.__init__(self)

        self._desc_string = "The Imp kills a player each night, and can make copies of itself... " \
                            "for a terrible price."
        self._examp_string = ""
        self._instr_string = "Each night*, choose a player: they die. " \
                             "If you kill yourself this way, a Minion becomes the Imp."
        self._lore_string = ""
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/42/Imp_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Imp"

        self._role_name = TBRole.imp