"""Contains the Recluse Character class"""

from botc import Outsider
from ._utils import TroubleBrewing
from ._utils import TBRole

class Recluse(Outsider, TroubleBrewing):
    """Recluse:
    You might register as evil & as a Minion or Demon, even if dead.
    """

    def __init__(self):

        TroubleBrewing.__init__(self)
        Outsider.__init__(self)

        self._desc_string = "The Recluse might appear to be an evil character, but is actually good."
        self._examp_string = ""
        self._instr_string = "You might register as evil & as a Minion or Demon, even if dead."
        self._lore_string = ""
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/b/bb/Recluse_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Recluse"

        self._role_name = TBRole.recluse
        