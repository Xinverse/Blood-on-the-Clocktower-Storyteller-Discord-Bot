class Washerwoman:
    """Washerwoman:
    You start knowing 1 of 2 players is a particular Townsfolk.
    """

    def __init__(self):
        self._desc_string = "- The Washerwoman learns that a particular Townsfolk character is in play, " \
                            "but not exactly who is playing it.\n" \
                            "- During the first night, the Washerwoman is woken, shown two players, " \
                            "and learns the character of one of them.\n" \
                            "- They learn this only once and then learn nothing more."
        self._examp_string = "- Evin is the Chef, and Amy is the Ravenkeeper. The Washerwoman learns that " \
                             "either Evin or Amy is the Chef.\n" \
                             "- Julian is the Imp, and Alex is the Virgin. The Washerwoman learns that " \
                             "either Julian or Alex is the Virgin.\n" \
                             "- Marianna is the Spy, and Sarah is the Scarlet Woman. The Washerwoman " \
                             "learns that one of them is the Ravenkeeper. (This happens because the Spy " \
                             "is registering as a Townsfolk— in this case, the Ravenkeeper.)"
        self._instr_string = "You start knowing 1 of 2 players is a particular Townsfolk."
        self._lore_string = "Bloodstains on a dinner jacket? No. This is cooking sherry. How careless."
        self._art_link = "http://bloodontheclocktower.com/wiki/images/4/4d/Washerwoman_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Washerwoman"
