"""Contains the Drunk Character class"""

from botc import Outsider
from ._utils import TroubleBrewing
from ._utils import TBRole

class Drunk(Outsider, TroubleBrewing):
    """Drunk:
    You think you are a Townsfolk, but your ability malfunctions.
    """

    def __init__(self):

        TroubleBrewing.__init__(self)
        Outsider.__init__(self)

        self._desc_string = "The Drunk player thinks that they are a Townsfolk, " \
                            "and has no idea that they are actually the Drunk."
        self._examp_string = ""
        self._instr_string = "You do not know you are the Drunk. " \
                             "You think you are a Townsfolk, but your ability malfunctions."
        self._lore_string = ""
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/0/03/Drunk_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Drunk"

        self._role_name = TBRole.drunk