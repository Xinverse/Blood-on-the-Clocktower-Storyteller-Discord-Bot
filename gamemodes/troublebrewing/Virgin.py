"""Contains the Virgin Character class"""

from botc import Townsfolk

class Virgin(Townsfolk):
    """Virgin:
    The 1st time you are nominated, if the nominator is a Townsfolk, 
    they are executed immediately.
    """

    def __init__(self):

        Townsfolk.__init__(self)

        self._desc_string = "The Virgin is safe from execution...perhaps. In the process, " \
                            "they confirm if their nominator is a Townsfolk.\n" \
                            "- If a Townsfolk nominates the Virgin, then that Townsfolk is " \
                            "executed immediately. Because there can only be one execution " \
                            "per day, the nomination process immediately ends, even if a " \
                            "player was about to die.\n" \
                            "- Only Townsfolk are executed due to the Virgin's ability. " \
                            "If an Outsider, Minion, or Demon nominates the Virgin, nothing " \
                            "happens, and voting continues.\n" \
                            "- The Virgin’s ability is powerful because if a Townsfolk nominates " \
                            "them and dies, then both characters are almost certainly Townsfolk.\n" \
                            "- After being nominated for the first time, the Virgin loses their " \
                            "ability, even if the nominator did not die, and even if the Virgin " \
                            "was poisoned or drunk."
        self._examp_string = "- The Washerwoman nominates the Virgin. The Washerwoman dies, " \
                             "and voting ends.\n" \
                             "- The Drunk, who thinks they are the Chef, nominates the Virgin. " \
                             "The Drunk remains alive, and the Virgin loses their ability. " \
                             "Players may now vote on whether or not to execute the Virgin. " \
                             "(This happens because the Drunk is not a Townsfolk.)"
        self._instr_string = "The 1st time you are nominated, if the nominator is a Townsfolk, " \
                             "they are executed immediately."
        self._lore_string = "I am pure. Let those who are without sin cast themself down " \
                            "and suffer in my stead. My reputation shall not be stained with " \
                            "your venomous accusations."
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/5/5e/Virgin_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Virgin"
