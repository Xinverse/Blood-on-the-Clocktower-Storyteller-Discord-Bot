"""Contains the Grimoire class"""

import math
from PIL import Image
from botc.gamemodes import Gamemode


class Grimoire:
    """Grimoire object to show the grimoire representation to the Spy Character"""

    def __init__(self):

        background = Image.open("botc/assets/background.png").convert("RGBA")

        self.PIC_SQUARE_SIDE = min(background.size)
        self.BUFFER = 50

        background.save("botc/assets/grimoire.png", format="PNG")
    
    @property
    def token_width(self):
        "Find the width of each token based on the background size"
        return math.ceil(self.PIC_SQUARE_SIDE/6)
    
    @property
    def sitting_circle_radius(self):
        """Find the radius of the big sitting circle based on the background size"""
        return math.ceil(self.PIC_SQUARE_SIDE * 0.9 * 0.5)
    
    def create(self, game_obj):

        nb_players = len(game_obj.sitting_order)
        background = Image.open("botc/assets/grimoire.jpg")

        for n in range(nb_players):

            player_obj = game_obj.sitting_order[n]
            true_role = player_obj.role.true_self
            token_file_path = TokenPathGrabber().getpath(true_role)
            token = Image.open(token_file_path)
            token.convert("RGBA")
            token.thumbnail((self.token_width, self.token_width), Image.ANTIALIAS)
            print(token_file_path)

            x = self.get_x_from_angle(n*self.get_rad_angle(nb_players))
            y = self.get_y_from_angle(n*self.get_rad_angle(nb_players))
            background.paste(token, (int(x), int(y)), token)
        
        background.save("botc/assets/grimoire.jpg")
    
    def get_image(self):
        return 'botc/assets/grimoire.jpg'
    
    def get_rad_angle(self, nb_player):
        return 2 * math.pi / nb_player
    
    def get_x_from_angle(self, rad_angle):
        """For the tokens only"""
        return self.sitting_circle_radius * math.sin(rad_angle)
    
    def get_y_from_angle(self, rad_angle):
        """For the tokens only"""
        return self.sitting_circle_radius * math.cos(rad_angle)


class TokenPathGrabber:
    """A utility object to grab the path of a token png file"""
    
    def getpath(self, character_obj):
        # Trouble brewing gamemode
        if character_obj.gm_of_appearance == Gamemode.trouble_brewing:
            character_name = character_obj.name.title()
            words = character_name.split(" ")
            words.append("Token.png")
            file_name = "_".join(words)
            return "botc/assets/tb_tokens/" + file_name
        # Bad moon rising gamemode
        elif character_obj.gm_of_appearance == Gamemode.bad_moon_rising:
            pass
        # Sects and violets gamemode
        elif character_obj.gm_of_appearance == Gamemode.sects_and_violets:
            pass
