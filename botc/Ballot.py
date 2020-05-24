"""Contains the Ballot class"""

import enum

class Ballot(enum.Enum):
    """Ballot class for choices of vote"""

    yes = "yes"
    no = "no"
    abstain = "abstain"