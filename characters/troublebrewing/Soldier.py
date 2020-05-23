"""Contains the Soldier Character class"""

class Soldier:
    """Soldier:
    You are safe from the Demon.
    """

    def __init__(self):

        self._desc_string = "The Soldier can not be killed by the Demon.\n" \
                            "- The Soldier cannot die due to the Demon’s ability. So, if the Imp attacks " \
                            "the Soldier at night, nothing happens. Nobody dies. The Imp does not get to " \
                            "choose another player to attack instead.\n" \
                            "- The Soldier can still die by execution, even if the nominator was the " \
                            "Demon. The Soldier is protected from the Demon’s ability to kill, not the " \
                            "actions of the Demon player.\n" \
                            "- The Soldier is not protected from other harmful effects such as poisoning " \
                            "or drunkenness."
        self._examp_string = "- The Imp attacks the Soldier. The Soldier does not die, so nobody dies " \
                             "that night.\n" \
                             "- The Poisoner poisons the Soldier, then the Imp attacks the Soldier. " \
                             "The Soldier dies, since they have no ability.\n" \
                             "- The Imp attacks the Mayor. The Storyteller chooses that the Soldier " \
                             "dies instead. However, because the Soldier cannot be killed by the Demon, " \
                             "nobody dies that night."
        self._instr_string = "You are safe from the Demon."
        self._lore_string = "As David said to Goliath, as Theseus said to the Minotaur, as Arjuna " \
                            "said to Bhagadatta... No."
                            
        self._art_link = "http://bloodontheclocktower.com/wiki/images/9/9e/Soldier_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Soldier"
