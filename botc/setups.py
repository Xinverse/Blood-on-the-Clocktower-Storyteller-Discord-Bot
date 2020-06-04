"""Contains functions to help load the game pack into the main bot"""

from models import FormatterMeta
from .Game import Game
from .gamemodes.troublebrewing import Baron, Butler, Chef, Drunk, Empath, FortuneTeller, \
        Imp, Investigator, Librarian, Mayor, Monk, Poisoner, Ravenkeeper, Recluse, Saint, \
        ScarletWoman, Slayer, Soldier, Undertaker, Virgin, Washerwoman


class BOTCFormatter(FormatterMeta):
    """Group several functions to format game pack related information to display in the bot"""

    def create_complete_roles_list(self):
        """Create the list of roles from the game pack when the !roles command is used without argument."""
        final_text = self.make_header("Blood on the Clocktower (BoTC)")
        final_text += "\n"
        global setup
        for mode_title in setup["botc"]["gamemodes"]: 
            final_text += self.make_section_header(mode_title)
            final_text += "\n"
            role_obj_list = setup["botc"]["gamemodes"][mode_title]
            temp = ", ".join([self.format_role_name(role.name) for role in role_obj_list])
            final_text += temp           
        return final_text


setup = {

    "botc" : {

        "game_obj" : Game(),

        "formatter" : BOTCFormatter(),

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
