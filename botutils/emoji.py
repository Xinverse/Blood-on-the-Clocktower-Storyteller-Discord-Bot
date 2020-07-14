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

    # Plain emojis
    scroll = emojis["scroll"]
    approved = emojis["approved"]
    denied = emojis["denied"]
    people = emojis["people"]
    votes = emojis["votes"]
    alive = emojis["alive"]

    # Unicode emojis
    skull = emojis["skull"]
    fquit = emojis["fquit"]
    vote = emojis["vote"]

    # BOTC
    demonhead = emojis["demon_head"]
