"""Contains the emoji class"""

import json

with open('emojis.json') as json_file:
    emojis = json.load(json_file)


class BotEmoji:
    """A class to store and easily access bot custom emojis"""

    # Animated emojis
    loading = emojis["loading"]
    butterfly = emojis["butterfly"]
    check = emojis["check"]
    cross = emojis["cross"]
    gears = emojis["gears"]
    success = emojis["success"]
    beating_heart = emojis["beating_heart"]
    trophy_animated = emojis["trophy_animated"]
    char1 = emojis["char1"]
    char2 = emojis["char2"]
    char3 = emojis["char3"]
    char4 = emojis["char4"]
    char5 = emojis["char5"]
    char6 = emojis["char6"]
    char7 = emojis["char7"]
    char8 = emojis["char8"]
    char9 = emojis["char9"]
    char10 = emojis["char10"]
    char11 = emojis["char11"]
    char12 = emojis["char12"]
    char13 = emojis["char13"]
    char14 = emojis["char14"]

    # Plain emojis
    scroll = emojis["scroll"]
    approved = emojis["approved"]
    denied = emojis["denied"]
    people = emojis["people"]
    votes = emojis["votes"]
    alive = emojis["alive"]
    grimoire = emojis["grimoire"]
    hourglass = emojis["hourglass"]
    winner = emojis["winner"]
    puppy = emojis["puppy"]
    guillotine = emojis["guillotine"]
    alarmclock = emojis["alarmclock"]
    whisper = emojis["whisper"]
    unread_message = emojis["unread_message"]
    opened_letter = emojis["opened_letter"]
    warning_sign = emojis["warning_sign"]
    clocktower = emojis["clocktower"]
    gallows = emojis["gallows"]
    murder = emojis["murder"]
    sun = emojis["sun"]
    moon = emojis["moon"]
    sunrise = emojis["sunrise"]
    mention = emojis["mention"]

    # Unicode emojis
    skull = emojis["skull"]
    fquit = emojis["fquit"]
    vote = emojis["vote"]

    # BOTC
    demonhead = emojis["demon_head"]
