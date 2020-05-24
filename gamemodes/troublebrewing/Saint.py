"""Contains the Saint Character class"""

from botc import Outsider
from ._utils import TroubleBrewing
from ._utils import TBRole

class Saint(Outsider, TroubleBrewing):
    """Saint:
    If you die by execution, your team loses.
    """

    def __init__(self):

        TroubleBrewing.__init__(self)
        Outsider.__init__(self)

        self._desc_string = "The Saint ends the game if they are executed."
        self._examp_string = ""
        self._instr_string = "If you die by execution, your team loses."
        self._lore_string = ""
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/7/77/Saint_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Saint"

        self._role_name = TBRole.saint
