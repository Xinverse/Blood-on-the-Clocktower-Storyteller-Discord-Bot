"""Contains some global switches"""

# Master switches: turn them on (True) to immediately switch phase
master_proceed_to_day = False
master_proceed_to_dawn = False
master_proceed_to_night = False


def init_switches():
    """Initialize (reset) these global switches"""
    global master_proceed_to_day
    global master_proceed_to_night
    global master_proceed_to_dawn
    master_proceed_to_day = False
    master_proceed_to_dawn = False
    master_proceed_to_night = False
