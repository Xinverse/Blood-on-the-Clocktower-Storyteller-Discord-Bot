"""Contains the Chef Character class"""

from botc import Townsfolk

class Chef(Townsfolk):
    """Chef:
    You start knowing how many pairs of evil players there are.
    """
    
    def __init__(self):

        Townsfolk.__init__(self)

        self._desc_string = "The Chef knows if evil players are sitting next to each other.\n" \
                            "- On the first night, the Chef learns exactly how many pairs there " \
                            "are in total. A pair is two players, but one player may be a part of " \
                            "two pairs. So, two players sitting next to each other count as one " \
                            "pair, three players sitting next to each other count as two pairs. " \
                            "Four players sitting next to each other count as three pairs. And so " \
                            "on."
        self._examp_string = "- No evil players are sitting next to each other. The Chef learns " \
                             "a '0.'\n" \
                             "- The Imp is sitting next to the Baron. Across the circle, " \
                             "the Poisoner is sitting next to the Scarlet Woman. The Chef learns " \
                             "a '2.'\n" \
                             "- An evil Scapegoat is sitting between the Imp and a Minion. " \
                             "Across the circle, two other Minions are sitting next to each other. " \
                             "The Chef learns a '3.'"
        self._instr_string = "You start knowing how many pairs of evil players there are."
        self._lore_string = "This evening's reservations seem odd. Never before has Mrs. " \
                            "Mayweather kept company with that scamp from Hudson Lane."
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/4c/Chef_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Chef"

