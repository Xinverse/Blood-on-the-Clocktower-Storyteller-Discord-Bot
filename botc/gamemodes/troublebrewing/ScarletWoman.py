"""Contains the Scarlet Woman Character class"""

from botc import Minion
from ._utils import TroubleBrewing
from ._utils import TBRole

class ScarletWoman(Minion, TroubleBrewing):
    """Scarlet Woman:
    If there are 5 or more players alive & the Demon dies, you become the Demon.
    """

    def __init__(self):

        TroubleBrewing.__init__(self)
        Minion.__init__(self)

        self._desc_string = "The Scarlet Woman becomes the Demon when the Demon dies."
        self._examp_string = ""
        self._instr_string = "If there are 5 or more players alive & the Demon dies, you become the Demon."
        self._lore_string = ""
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/7/7c/Scarlet_Woman_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Scarlet_Woman"

        self._role_name = TBRole.scarletwoman
