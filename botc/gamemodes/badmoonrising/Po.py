import json
from botc import Character
from ._utils import BadMoonRising, BMRRole

with open('botc/gamemodes/badmoonrising/character_text.json') as json_file: 
    character_text = json.load(json_file)[BMRRole.po.value.lower()]

class Po(Character):
    def __init__(self):
        pass
