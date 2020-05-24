"""Contains the Fortune Teller Character class"""

from botc import Townsfolk

class FortuneTeller(Townsfolk):
    """Fortune Teller:
    Each night, choose 2 players: you learn if either is a Demon. There is 1 good player 
    that registers falsely to you.
    """
    
    def __init__(self):

        Townsfolk.__init__(self)

        self._desc_string = "The Fortune Teller detects who the Demon is, " \
                            "but sometimes thinks good players are Demons.\n" \
                            "- Each night, the Fortune Teller chooses two players and learns if at " \
                            "least one of them is a Demon. They do not learn which of them is a " \
                            "Demon, just that one of them is. If neither is the Demon, they learn " \
                            "this instead.\n" \
                            "- Unfortunately, one player, called the Red Herring, will register as " \
                            "a Demon to the Fortune Teller if chosen. The Red Herring is the same " \
                            "player throughout the entire game. This player may be any good player, " \
                            "even the Fortune Teller, and the Fortune Teller does not know which " \
                            "player it is.\n" \
                            "- The Fortune Teller may choose any two players—alive or dead, or even " \
                            "themself. If they choose a dead Demon, then the Fortune Teller still " \
                            "receives a nod."
        self._examp_string = "- The Fortune Teller chooses the Mayor and the Undertaker, and learns " \
                             "a 'no.'\n" \
                             "- The Fortune Teller chooses the Imp and the Empath, and learns a " \
                             "'yes.'\n" \
                             "- The Fortune Teller chooses an alive Imp and a dead Imp, and learns a " \
                             "'yes.'\n" \
                             "- The Fortune Teller chooses themself and a Saint, who is the Red " \
                             "Herring. The Fortune Teller learns a 'yes.'"
        self._instr_string = "Each night, choose 2 players: you learn if either is a Demon. " \
                             "There is 1 good player that registers falsely to you."
        self._lore_string = "I sense great evil in your soul! But... that could just be " \
                            "your perfume. I am allergic to elderberry."
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/3/3a/Fortune_Teller_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Fortune_Teller"

