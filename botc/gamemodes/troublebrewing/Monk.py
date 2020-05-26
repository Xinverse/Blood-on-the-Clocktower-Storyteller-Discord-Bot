"""Contains the Monk Character class"""

from botc import Townsfolk
from ._utils import TroubleBrewing
from ._utils import TBRole

class Monk(Townsfolk, TroubleBrewing):
    """Monk:
    Each night*, choose a player (not yourself): they are safe from the Demon tonight.
    """
    
    def __init__(self):

        TroubleBrewing.__init__(self)
        Townsfolk.__init__(self)

        self._desc_string = "The Monk protects other people from the Demon.\n" \
                            "- Each night except the first, the Monk may choose to protect any " \
                            "player except themself.\n" \
                            "- If the Demon attacks a player who has been protected by the Monk, " \
                            "then that player does not die. The Demon does not get to attack " \
                            "another player—there is simply no death tonight.\n" \
                            "- The Monk does not protect against other harmful effects such as " \
                            "poisoning, drunkenness, or Outsider penalties. The Monk does not " \
                            "protect against the Demon nominating and executing someone."
        self._examp_string = "- The Monk protects the Fortune Teller. The Imp attacks the " \
                             "Fortune Teller. No deaths occur tonight.\n" \
                             "- The Monk protects the Mayor, and the Imp attacks the Mayor. " \
                             "The Mayor's 'another player dies' ability does not trigger, " \
                             "because the Mayor is safe from the Imp. Nobody dies tonight.\n" \
                             "- The Monk protects the Imp. The Imp chooses to kill themself " \
                             "tonight, but nothing happens. The Imp stays alive and a new " \
                             "Imp is not created.\n"
        self._instr_string = "Each night*, choose a player (not yourself): " \
                             "they are safe from the Demon tonight."
        self._lore_string = "Tis an ill and deathly wind that blows tonight. Come, my " \
                            "brother, take shelter in the abbey while the storm rages. By my " \
                            "word, or by my life, you will be safe."
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/1/1b/Monk_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Monk"

        self._role_name = TBRole.monk
