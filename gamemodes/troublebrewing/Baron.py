"""Contains the Baron Character class"""

from botc import Minion
from ._utils import TroubleBrewing
from ._utils import TBRole

class Baron(Minion, TroubleBrewing):
    """Baron:
    There are extra Outsiders in play [+2 Outsiders]
    """

    def __init__(self):
        
        TroubleBrewing.__init__(self)
        Minion.__init__(self)

        self._desc_string = "The Baron changes the number of Outsiders present in the game."
        self._examp_string = ""
        self._instr_string = "There are extra Outsiders in play. [+2 Outsiders]"
        self._lore_string = ""
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/b/ba/Baron_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Baron"

        self._role_name = TBRole.baron