import math
from .RoleGuide import RoleGuide
from PIL import Image, ImageDraw, ImageFont
from .PlayerState import PlayerState

class TownSquare:
    """Graphical representation of player sittings in a BoTC game."""
    
    PIC_SQUARE_SIDE = 500
    BUFFER = 50
    RADIUS = 200
    TOKEN_RADIUS = 25
    VOTE_TOKEN_RADIUS = 5
    ALIVE_TOKEN_COLOR = (242, 228, 201)
    DEAD_TOKEN_COLOR = (0, 0, 0)
    VOTE_TOKEN_COLOR = (255, 255, 255)
    BACKGROUND_COLOR = (181, 178, 172)
    TABLE_COLOR = (84, 84, 84)
    TEXT_COLOR = (255, 255, 255)
    LABEL_BACKGROUND_COLOR = (51, 51, 153)

    def __init__(self, game_obj):

        nb_players = len(game_obj.frozen_sitting)

        im = Image.new('RGB', (self.PIC_SQUARE_SIDE, self.PIC_SQUARE_SIDE), self.BACKGROUND_COLOR)
        draw = ImageDraw.Draw(im)

        # Draw the table
        draw.ellipse(self.find_boundary_box(self.get_x_center(), self.get_y_center(), self.RADIUS),
                     outline=self.TABLE_COLOR, fill=self.TABLE_COLOR)

        for n in range(nb_players):

            player_obj = game_obj.frozen_sitting[n]

            # Draw the tokens
            center_x = self.get_x_from_angle(n*self.get_rad_angle(nb_players))
            center_y = self.get_y_from_angle(n*self.get_rad_angle(nb_players))

            # Alive player token
            if player_obj.apparent_state == PlayerState.alive:
                draw.ellipse(self.find_boundary_box(center_x, center_y, self.TOKEN_RADIUS), 
                            outline=self.ALIVE_TOKEN_COLOR, fill=self.ALIVE_TOKEN_COLOR)

            # Dead player token
            elif player_obj.apparent_state == PlayerState.dead:
                draw.ellipse(self.find_boundary_box(center_x, center_y, self.TOKEN_RADIUS), 
                            outline=self.DEAD_TOKEN_COLOR, fill=self.DEAD_TOKEN_COLOR)

            # Fleaved player is drawn with a dead token without the vote token
            else:
                draw.ellipse(self.find_boundary_box(center_x, center_y, self.TOKEN_RADIUS), 
                            outline=self.DEAD_TOKEN_COLOR, fill=self.DEAD_TOKEN_COLOR)
            
            # Draw the username labels
            member = player_obj._user_obj
            label = member.name[:10]
            unicode_font = ImageFont.truetype("botc/assets/DejaVuSans.ttf", 12)
            w, h = unicode_font.getsize(label)
            x = center_x - 1.2 * self.TOKEN_RADIUS
            y = center_y + 1.2 * self.TOKEN_RADIUS
            draw.rectangle((x, y, x + w, y + h), fill = self.LABEL_BACKGROUND_COLOR)
            draw.text((x, y), font=unicode_font, text = label)

        # Center stats text
        guide = RoleGuide(nb_players)

        nb_townsfolk = guide.nb_townsfolks
        nb_outsider = guide.nb_outsiders
        nb_minion = guide.nb_minions
        nb_demon = guide.nb_demons

        center_msg = "{}\n[TOTAL] {} players.\n\nTownsfolk: {}\nOutsider: {}\nMinion: {}\n" \
                     "Demon: {}".format(
                         game_obj.gamemode.value,
                         str(nb_players),
                         str(nb_townsfolk),
                         str(nb_outsider),
                         str(nb_minion),
                         str(nb_demon)
                    )

        font_path = "botc/assets/wilson.ttf"
        font = ImageFont.truetype(font_path, 22)
        draw.text((180, 180), center_msg, fill=self.TEXT_COLOR, font=font)

        im.save('botc/assets/botctownsquare.jpg', quality=95)

        background = Image.open("botc/assets/botctownsquare.jpg")
        chair = Image.open("botc/assets/chair.png")
        chair_size_width, chair_size_height = chair.size[0], chair.size[1]

        # Draw the chairs
        for n in range(nb_players):
            x = self.get_chair_x_from_angle(n*self.get_rad_angle(nb_players))
            y = self.get_chair_y_from_angle(n*self.get_rad_angle(nb_players))
            x -= chair_size_width * 0.5
            y -= chair_size_height * 0.5
            rotated = chair.rotate(math.degrees(n*self.get_rad_angle(nb_players)), Image.NEAREST, expand=False)
            transposed  = rotated.transpose(Image.ROTATE_180)
            background.paste(transposed, (int(x), int(y)), transposed)

        background.save("botc/assets/botctownsquare.jpg", "JPEG")
    
    @staticmethod
    def get_x_center():
        coord = TownSquare.PIC_SQUARE_SIDE - TownSquare.BUFFER - TownSquare.RADIUS
        return coord

    @staticmethod
    def get_y_center():
        return TownSquare.get_x_center()

    @staticmethod
    def get_rad_angle(nb_player):
        return 2 * math.pi / nb_player
    
    @staticmethod
    def get_x_from_angle(rad_angle):
        """For the tokens only"""
        return 0.8 * TownSquare.RADIUS * math.sin(rad_angle) + TownSquare.get_x_center()
    
    @staticmethod
    def get_y_from_angle(rad_angle):
        """For the tokens only"""
        return 0.8 * TownSquare.RADIUS * math.cos(rad_angle) + TownSquare.get_y_center()
    
    @staticmethod
    def get_chair_x_from_angle(rad_angle):
        """For the chairs only"""
        return 1.2 * TownSquare.RADIUS * math.sin(rad_angle) + TownSquare.get_x_center()
    
    @staticmethod
    def get_chair_y_from_angle(rad_angle):
        """For the chairs only"""
        return 1.2 * TownSquare.RADIUS * math.cos(rad_angle) + TownSquare.get_y_center()
    
    @staticmethod
    def find_boundary_box(center_x, center_y, r):
        return (center_x - r, center_y - r, center_x + r, center_y + r)
    
    def get_image(self):
        return 'botc/assets/botctownsquare.jpg'

