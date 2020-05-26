"""Contains the Librarian Character class"""

from botc import Townsfolk
from ._utils import TroubleBrewing
from ._utils import TBRole

class Librarian(Townsfolk, TroubleBrewing):
    """Librarian:
    You start knowing that 1 of 2 players is a particular Outsider.
    (Or that zero are in play)
    """
    
    def __init__(self):

        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = "The Librarian learns that a particular Outsider character is in play, " \
                            "but not who is playing it.\n" \
                            "- During the first night, the Librarian learns that one of two players " \
                            "is a specific Outsider.\n" \
                            "- They learn this only once and then learn nothing more.\n" \
                            "- The Drunk is an Outsider. If the Librarian learns that 1 of 2 " \
                            "players is the Drunk, they do not learn the Townsfolk that the player " \
                            "thinks that they are."
        self._examp_string = "- Benjamin is the Saint, and Filip is the Baron. The Librarian learns " \
                             "that either Benjamin or Filip is the Saint.\n" \
                             "- The Storyteller decides that the Recluse registers as a Minion, " \
                             "not an Outsider. There are no other Outsiders in play. The Librarian " \
                             "learns a '0'.\n" \
                             "- Abdallah is the Drunk, who thinks they are the Monk, and Douglas is " \
                             "the Undertaker. The Librarian learns that either Abdallah or Douglas " \
                             "is the Drunk."
        self._instr_string = "You start knowing that 1 of 2 players is a particular Outsider." \
                             "(Or that zero are in play)"
        self._lore_string = "Certainly, madam, you may borrow the Codex Malificarium from the " \
                            "library vaults."
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/8/86/Librarian_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Librarian"

        self._role_name = TBRole.librarian