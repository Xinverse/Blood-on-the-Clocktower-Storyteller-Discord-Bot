"""Contains the Investigator Character class"""

from botc import Townsfolk

class Investigator(Townsfolk):
    """Investigator:
    You start knowing 1 of 2 players is a particular Minion.
    """

    def __init__(self):

        Townsfolk.__init__(self)

        self._desc_string = "The Investigator learns that a particular Minion character is in play, " \
                            "but not exactly which player it is.\n" \
                            "- During the first night, the Investigator is woken and shown two players, " \
                            "but only learns the character of one of them.\n" \
                            "- They learn this only once and then learn nothing more."
        self._examp_string = "- Amy is the Baron, and Julian is the Mayor. The Investigator learns " \
                             "that either Amy or Julian is the Baron.\n" \
                             "- Angelus is the Spy, and Lewis is the Poisoner. The Investigator " \
                             "learns that either Angelus or Lewis is the Spy.\n" \
                             "- Brianna is the Recluse, and Marianna is the Imp. The Investigator " \
                             "learns that either Brianna or Marianna is the Poisoner. (This happens " \
                             "because the Recluse is registering as a Minion—in this case, the Poisoner.)"
        self._instr_string = "You start knowing 1 of 2 players is a particular Minion."
        self._lore_string = "It is a fine night for a stroll, wouldn't you say, Mister Morozov? " \
                            "Or should I say... BARON Morozov?"
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/e/ec/Investigator_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Investigator"

