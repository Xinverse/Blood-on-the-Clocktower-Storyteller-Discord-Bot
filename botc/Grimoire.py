"""Contains the Grimoire class"""

import math
from PIL import Image, ImageFont, ImageDraw
from botc.gamemodes import Gamemode


class Grimoire:
    """Grimoire object to show the grimoire representation to the Spy Character"""

    BACKGROUND_PATH = "botc/assets/grimoire/background.png"
    GRIMOIRE_PATH = "botc/assets/grimoire/grimoire.png"
    TB_ICON = "botc/assets/editions/TB_Logo.png"
    BMR_ICON = "botc/assets/editions/BMR_Logo.png"
    SV_ICON = "botc/assets/editions/SV_Logo.png"
    SHROUD = "botc/assets/grimoire/shroud.png"
    FONT = "botc/assets/grimoire/Bitstream_Cyberbit.ttf"

    def __init__(self):

        background = Image.open(self.BACKGROUND_PATH)
        background.convert("RGBA")

        self.PIC_SQUARE_SIDE = min(background.size)
        self.PIC_LENGTH = max(background.size)

        background.save(self.GRIMOIRE_PATH, format="PNG")
    
    @property
    def token_width(self):
        "Find the width of each token based on the background size"
        return math.ceil(self.PIC_SQUARE_SIDE/5.5)
    
    @property
    def sitting_circle_radius(self):
        """Find the radius of the big sitting circle based on the background size"""
        return math.ceil(self.PIC_SQUARE_SIDE * 0.75 * 0.5)
    
    @property
    def font_size(self):
        """Find the font size appropriate for the size of the image"""
        return math.ceil(self.PIC_SQUARE_SIDE * 0.04)
    
    def create(self, game_obj):

        nb_players = len(game_obj.sitting_order)
        background = Image.open(self.GRIMOIRE_PATH)
        draw = ImageDraw.Draw(background, "RGBA")
        font = ImageFont.truetype(self.FONT, self.font_size)
        self.paste_gamemode_icon(game_obj, background)

        for n in range(nb_players):

            player_obj = game_obj.sitting_order[n]
            true_role = player_obj.role.true_self
            token_file_path = TokenPathGrabber().getpath(true_role)
            token = Image.open(token_file_path)
            token.thumbnail((self.token_width, self.token_width), Image.ANTIALIAS)

            x = self.get_x_from_angle(n*self.get_rad_angle(nb_players))
            y = self.get_y_from_angle(n*self.get_rad_angle(nb_players))

            new_x, new_y = self.translate(x, y)
            token_center_x = int(new_x + self.token_width / 2)
            token_center_y = int(new_y + self.token_width / 2)

            try:
                background.paste(token, (new_x, new_y), token.convert("RGBA"))
            except Exception:
                pass
            
            # Add the shroud reminder
            if player_obj.is_apparently_dead():

                shroud = Image.open(self.SHROUD)
                shroud_size_x = shroud.size[0]
                shroud_size_y = shroud.size[1]

                ratio = shroud_size_y / (self.token_width / 2)
                ratio = 1 / ratio
                thumbnail_x = int(shroud_size_x * ratio)
                thumbnail_y = int(shroud_size_y * ratio)
                shroud.thumbnail((thumbnail_x, thumbnail_y), Image.ANTIALIAS)
                
                shroud_x = int(token_center_x - thumbnail_x / 2)
                shroud_y = int(token_center_y - self.token_width / 2)
                background.paste(shroud, (shroud_x, shroud_y), shroud.convert("RGBA"))
            
            text = player_obj.user.display_name
            w, h = font.getsize(text)
            new_x, new_y = self.translate_text(x, y, w)
            draw.rectangle((new_x, new_y, new_x + w, new_y + h), fill = (37, 30, 23, 140))
            draw.text((new_x, new_y), text, (255, 255, 255), font = font)

        background.save(self.GRIMOIRE_PATH)

    def paste_gamemode_icon(self, game_obj, background):

        x = self.PIC_LENGTH / 2
        y = self.PIC_SQUARE_SIDE / 2

        if game_obj.gamemode == Gamemode.trouble_brewing:

            edition_logo = Image.open(self.TB_ICON)

            logo_size_x = edition_logo.size[0]
            logo_size_y = edition_logo.size[1]
            ratio = logo_size_y / (self.PIC_SQUARE_SIDE / 4)
            ratio = 1 / ratio
            thumbnail_x = int(logo_size_x * ratio)
            thumbnail_y = int(logo_size_y * ratio)

            edition_logo.thumbnail((thumbnail_x, thumbnail_y), Image.ANTIALIAS)

            x -= thumbnail_x / 2
            y -= thumbnail_y / 2

            try:
                background.paste(edition_logo, (int(x), int(y)), edition_logo.convert("RGBA"))
            except Exception:
                pass

        elif game_obj.gamemode == Gamemode.bad_moon_rising:
            pass

        elif game_obj.gamemode == Gamemode.sects_and_violets:
            pass
    
    def translate(self, x, y):
        image_center_x = self.PIC_LENGTH / 2
        image_center_y = self.PIC_SQUARE_SIDE / 2

        image_center_x -= self.token_width / 2
        image_center_y -= self.token_width / 2

        return(int(x + image_center_x), int(y + image_center_y))
    
    def translate_text(self, x, y, text_width):
        image_center_x = self.PIC_LENGTH / 2
        image_center_y = self.PIC_SQUARE_SIDE / 2

        image_center_x -= self.token_width / 2
        image_center_y -= self.token_width / 2

        offset = (text_width - self.token_width) / 2

        return(int(x + image_center_x - offset), int(y + image_center_y))
    
    def get_image(self):
        return self.GRIMOIRE_PATH
    
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
            return "botc/assets/tb_tokens_rgba/" + file_name
        # Bad moon rising gamemode
        elif character_obj.gm_of_appearance == Gamemode.bad_moon_rising:
            pass
        # Sects and violets gamemode
        elif character_obj.gm_of_appearance == Gamemode.sects_and_violets:
            pass
