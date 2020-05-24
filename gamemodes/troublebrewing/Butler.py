"""Contains the Butler Character class"""

from botc import Outsider
from ._utils import TroubleBrewing
from ._utils import TBRole

class Butler(Outsider, TroubleBrewing):
    """Butler:
    Each night, choose a player (not yourself): tomorrow, you may only vote if they are voting 
    too.
    """

    def __init__(self):

        TroubleBrewing.__init__(self)
        Outsider.__init__(self)

        self._desc_string = "The Butler may only vote when their Master (another player) votes."
        self._examp_string = ""
        self._instr_string = "Each night, choose a player (not yourself): " \
                             "tomorrow, you may only vote if they are voting too."
        self._lore_string = ""
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/1/1a/Butler_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Butler"

        self._role_name = TBRole.butler