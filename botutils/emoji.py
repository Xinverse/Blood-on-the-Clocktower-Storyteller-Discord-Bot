"""Contains the emoji class"""

import configparser

Config = configparser.ConfigParser()
Config.read("emojis.INI")


class BotEmoji:
    """A class to store and easily access bot custom emojis"""

    gears = Config["GEARS_EMOJI"]
