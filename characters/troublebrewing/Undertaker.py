"""Contains the Undertaker Character class"""

class Undertaker:
    """Undertaker:
    Each night, you learn which character died by execution today.
    """

    def __init__(self):
        self._desc_string = "The Undertaker learns which character was executed today.\n" \
                            "- The player must have died from execution for the Undertaker to " \
                            "learn who they are. Deaths during the day for other reasons, such " \
                            "as the Gunslinger choosing a player to kill, or the exile of a " \
                            "Traveler, do not count. Execution without death—rare as it is—does " \
                            "not count.\n" \
                            "- The Undertaker wakes each night except the first, as there have " \
                            "been no executions yet.\n" \
                            "- If nobody died by execution today, the Undertaker learns nothing. " \
                            "The Storyteller either does not wake the Undertaker at night, or " \
                            "wakes them but does not show a token.\n" \
                            "- If the Drunk is executed, the Undertaker is shown the the Drunk " \
                            "character token, not the Townsfolk that the player thought they were."
        self._examp_string = "- The Mayor is executed today. That night, the Undertaker is " \
                             "shown the Mayor token.\n" \
                             "- The Drunk, who thinks they are the Virgin, is executed today. " \
                             "The Undertaker is shown the Drunk token, because the Undertaker " \
                             "learns the actual character of the player, not the character " \
                             "the player thinks they are.\n" \
                             "- The Spy is executed. Two Travelers are exiled. That night, " \
                             "the Undertaker is shown the Butler token, because the Spy is " \
                             "registering as the Butler, and because the exiles are not " \
                             "executions.\n" \
                             "- Nobody was executed today. That night, the Undertaker does not wake."
        self._instr_string = "Each night, you learn which character died by execution today."
        self._lore_string = "Hmmm....what have we here? The left boot is worn down to the " \
                            "heel, with flint shavings under the tongue. This is the garb of " \
                            "a military man."
        self._art_link = "http://bloodontheclocktower.com/wiki/images/f/fe/Undertaker_Token.png"
        self._wiki_link = "http://bloodontheclocktower.com/wiki/Undertaker"

