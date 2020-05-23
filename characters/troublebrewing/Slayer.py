class Slayer:
    """Slayer:
    Once per game, during the day, publicly choose a player: if they are the Demon, they die.
    """

    def __init__(self):
        self._desc_string = "The Slayer can kill the Demon by guessing who it is.\n" \
                            "- The Slayer can choose to use their ability at any time during " \
                            "the day, and must declare to everyone when they’re using it. If " \
                            "the Slayer chooses the Demon, the Demon dies immediately. Otherwise, " \
                            "nothing happens.\n" \
                            "- The players do not learn the identity of the dead player. After " \
                            "all, it may have been the Recluse!\n" \
                            "- A Slayer that uses their ability while poisoned or drunk may not " \
                            "use it again.\n" \
                            "- The Slayer will want to choose an alive player. Even if the Slayer " \
                            "chooses a dead Imp, nothing happens, because a dead player can’t die " \
                            "again."
        self._examp_string = "- The Slayer chooses the Imp. The Imp dies, and good wins!\n" \
                             "- The Slayer chooses the Recluse. The Storyteller decides " \
                             "that the Recluse registers as the Imp, so the Recluse dies, " \
                             "but the game continues.\n" \
                             "- The Imp is bluffing as the Slayer. They declare that they " \
                             "use their Slayer ability on the Scarlet Woman. Nothing happens."
        self._instr_string = "Once per game, during the day, publicly choose a player: " \
                             "if they are the Demon, they die."
        self._lore_string = "Die."
        self._art_link = "http://bloodontheclocktower.com/wiki/images/2/2f/Slayer_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Slayer"

