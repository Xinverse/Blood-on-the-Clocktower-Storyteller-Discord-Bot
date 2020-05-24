"""Contains the Empath Character class"""

from botc import Townsfolk
from ._utils import TroubleBrewing
from ._utils import TBRole

class Empath(Townsfolk, TroubleBrewing):
    """Empath:
    Each night, you learn how many of your 2 alive neighbors are evil.
    """
    
    def __init__(self):

        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = "The Empath keeps learning if their living neighbors are good or evil.\n" \
                            "- The Empath only learns how many of their neighbors are evil, not " \
                            "which one is evil.\n" \
                            "- The Empath does not detect dead players. So, if the Empath is sitting " \
                            "next to a dead player, the information refers not to the dead player, " \
                            "but to the closest alive player in that direction.\n" \
                            "- The Empath acts after the Demon, so if the Demon kills one of the " \
                            "Empath’s alive neighbors, the Empath does not learn about the now-dead " \
                            "player. The Empath's information is accurate at dawn, not at dusk."
        self._examp_string = "- The Empath neighbors two good players—a Soldier and a Monk. " \
                             "The Empath learns a '0.'\n" \
                             "- The next day, the Soldier is executed. That night, the Monk is " \
                             "killed by the Imp. The Empath now detects the players sitting " \
                             "next to the Soldier and the Monk, which are a Librarian and an " \
                             "evil Gunslinger. The Empath now learns a '1.'\n" \
                             "- There are only three players left alive: the Empath, the Imp, " \
                             "and the Baron. No matter who is seated where, the Empath learns a " \
                             "'2.'\n"
        self._instr_string = "Each night, you learn how many of your 2 alive neighbors are evil."
        self._lore_string = "My skin prickles. Something is not right here. I can feel it."
        
        self._art_link = "http://bloodontheclocktower.com/wiki/images/6/61/Empath_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Empath"

        self._role_name = TBRole.empath

