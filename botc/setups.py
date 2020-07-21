"""Contains functions to help load the game pack into the main bot"""

from models import FormatterMeta
from .Game import Game
from .gamemodes.troublebrewing import Baron, Butler, Chef, Drunk, Empath, FortuneTeller, \
        Imp, Investigator, Librarian, Mayor, Monk, Poisoner, Ravenkeeper, Recluse, Saint, \
        ScarletWoman, Slayer, Soldier, Spy, Undertaker, Virgin, Washerwoman
from .gamemodes.badmoonrising import Assassin, Chambermaid, Courtier, DevilsAdvocate, \
        Exorcist, Fool, Gambler, Godfather, Goon, Gossip, Grandmother, Innkeeper, Lunatic, \
        Mastermind, Minstrel, Moonchild, Pacifist, Po, Professor, Pukka, Sailor, Shabaloth, \
        TeaLady, Tinker, Zombuul
from .gamemodes.sectsandviolets import Artist, Barber, Cerenovus, Clockmaker, Dreamer, \
    EvilTwin, FangGu, Flowergirl, Juggler, Klutz, Mathematician, Mutant, NoDashii, Oracle, \
    Philosopher, PitHag, Sage, Savant, Seamstress, SnakeCharmer, Sweetheart, TownCrier, \
    Vigormortis, Vortox, Witch


class BOTCFormatter(FormatterMeta):
    """Group several functions to format game pack related information to display in the bot"""

    def create_complete_roles_list(self):
        """Create the list of roles from the game pack when the !roles command is used without argument."""
        final_text = self.make_header("Blood on the Clocktower (BoTC)")
        final_text += "\n\n"
        global setup
        for mode_title in setup["botc"]["gamemodes"]: 
            final_text += self.make_section_header(mode_title)
            final_text += "\n"
            role_obj_list = setup["botc"]["gamemodes"][mode_title]
            temp = ", ".join([self.format_role_name(role.name) for role in role_obj_list])
            final_text += temp
            final_text += "\n\n"
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
                            Spy(),
                            Undertaker(),
                            Virgin(),
                            Washerwoman()

                        ],
            
            "bad-moon-rising" : [

                            Assassin(),
                            Chambermaid(),
                            Courtier(),
                            DevilsAdvocate(),
                            Exorcist(),
                            Fool(),
                            Gambler(),
                            Godfather(),
                            Goon(),
                            Gossip(),
                            Grandmother(),
                            Innkeeper(),
                            Lunatic(),
                            Mastermind(),
                            Minstrel(),
                            Moonchild(),
                            Pacifist(),
                            Po(),
                            Professor(),
                            Pukka(),
                            Sailor(),
                            Shabaloth(),
                            TeaLady(),
                            Tinker(),
                            Zombuul()

                        ],
            
            "sects-&-violets" : [

                            Artist(),
                            Barber(),
                            Cerenovus(),
                            Clockmaker(),
                            Dreamer(),
                            EvilTwin(),
                            FangGu(),
                            Flowergirl(),
                            Juggler(),
                            Klutz(),
                            Mathematician(),
                            Mutant(),
                            NoDashii(),
                            Oracle(),
                            Philosopher(),
                            PitHag(),
                            Sage(),
                            Savant(),
                            Seamstress(),
                            SnakeCharmer(),
                            Sweetheart(),
                            TownCrier(),
                            Vigormortis(),
                            Vortox(),
                            Witch()

                        ]

        }

    }

}   


def load_pack(master_state):
    """Load the game pack into the main bot state"""
    master_state.add_pack(setup)
    import globvars
    globvars.client.load_extension("botc.commands.botc_general_commands")
