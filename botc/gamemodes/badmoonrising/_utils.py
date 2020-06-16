"""Contains BMRRole enum class and Bad Moon Rising class"""

import enum
from botc.gamemodes import Gamemode


class BMRRole(enum.Enum):
    """Enum object for all Bad Moon Rising edition roles"""

    assassin = "Assassin"
    chambermaid = "Chambermaid"
    courtier = "Courtier"
    devilsadvocate = "Devil's Advocate"
    exorcist = "Exorcist"
    fool = "Fool"
    gambler = "Gambler" 
    godfather = "Godfather" 
    goon = "Goon"
    gossip = "Gossip"
    grandmother = "Grandmother"
    innkeeper = "Innkeeper"
    lunatic = "Lunatic"
    mastermind = "Mastermind"
    minstrel = "Minstrel"
    moonchild = "Moonchild"
    pacifist = "Pacifist"
    po = "Po"
    professor = "Professor"
    pukka = "Pukka"
    sailor = "Sailor"
    shabaloth = "Shaboloth"
    tealady = "Tea Lady"
    tinker = "Tinker"
    zombuul = "Zombuul"


class BadMoonRising:
    """Parent class for all Bad Moon Rising edition roles"""

    def __init__(self):

        self._gm_of_appearance = Gamemode.bad_moon_rising
        self._gm_art_link = "http://bloodontheclocktower.com/wiki/images/d/d9/BMR_Logo.png"
        