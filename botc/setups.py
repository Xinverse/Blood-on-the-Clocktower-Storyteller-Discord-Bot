"""Contains functions to help load the game pack into the main bot"""

from .Game import Game
from .gamemodes.troublebrewing import Baron, Butler, Chef, Drunk, Empath, FortuneTeller, \
        Imp, Investigator, Librarian, Mayor, Monk, Poisoner, Ravenkeeper, Recluse, Saint, \
        ScarletWoman, Slayer, Soldier, Undertaker, Virgin, Washerwoman

setup = {

    "botc" : {

        "game_obj" : Game(),

        "gamemodes" : {

            "trouble-brewing" : [

                            Baron(),
                            Butler(),
                            Chef(),
                            Drunk(),
                            Empath(),
                            FortuneTeller(),
                            Imp(),
                            Investigator(),
                            Librarian(),
                            Mayor(),
                            Monk(),
                            Poisoner(),
                            Ravenkeeper(),
                            Recluse(),
                            Saint(),
                            ScarletWoman(),
                            Slayer(),
                            Soldier(),
                            Undertaker(),
                            Virgin(),
                            Washerwoman()

                        ]

        }

    }

}   


def load_pack(master_state):
    """Load the game pack into the main bot state"""
    master_state.add_pack(setup)
