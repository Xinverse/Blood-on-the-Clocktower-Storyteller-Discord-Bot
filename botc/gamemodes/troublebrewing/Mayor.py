"""Contains the Mayor Character class"""

from botc import Townsfolk
from ._utils import TroubleBrewing
from ._utils import TBRole

class Mayor(Townsfolk, TroubleBrewing):
    """Mayor:
    If only 3 players live and no execution occurs, your team wins. If you die at night, another
    player might die instead.
    """

    def __init__(self):

        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = "The Mayor can win by peaceful means on the final day."
        self._examp_string = ""
        self._instr_string = "If only 3 players live & no execution occurs, your team wins. " \
                             "If you die at night, another player might die instead."
        self._lore_string = ""
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/c/c4/Mayor_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Mayor"

        self._role_name = TBRole.mayor