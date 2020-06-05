"""Example game pack:
Required file: setups.py

Contains functions to help load the game pack into the main bot.
"""

# ----- Imports -----

from models import FormatterMeta
from .Game import Game
# Import all your roles here


# ----- Formatter -----

class CustomFormatter(FormatterMeta):
    """Group several functions to format game pack related information to display in the bot"""

    def create_complete_roles_list(self):
        """Create the list of roles from the game pack when the !roles command is used without argument."""      
        return ""


# ----- Setup -----

setup = {

    "game_pack_name" : {

        "game_obj" : Game(),

        "formatter" : CustomFormatter(),

        "gamemodes" : {

            "gamemode_name1" : [

                            # Role1(),
                            # Role2(),
                            # Role3()
                            # etc.

                        ],

            "gamemode_name2" : [

                            # Role1(),
                            # Role2(),
                            # Role3()
                            # etc.

                        ],

        }

    }

}   


# ----- Load Pack Function -----

def load_pack(master_state):
    """Load the game pack into the main bot state"""
    master_state.add_pack(setup)


