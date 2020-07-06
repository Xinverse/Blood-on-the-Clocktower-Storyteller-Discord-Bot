
import os
import numpy as np
from PIL import Image


def crop(image_path, saved_location):
    """
    @param image_path: The path to the image to edit
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    w, h = image_obj.size
    cropped_image = image_obj.crop((1, 0, w, h))
    cropped_image.save(saved_location)
    #cropped_image.show()


def alpha_to_color(image, color=(255, 255, 255)):
    """Set all fully transparent pixels of an RGBA image to the specified color.
    This is a very simple solution that might leave over some ugly edges, due
    to semi-transparent areas. You should use alpha_composite_with color instead.

    Source: http://stackoverflow.com/a/9166671/284318

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)

    """ 
    x = np.array(image)
    r, g, b, a = np.rollaxis(x, axis=-1)
    r[a == 0] = color[0]
    g[a == 0] = color[1]
    b[a == 0] = color[2] 
    x = np.dstack([r, g, b, a])
    return Image.fromarray(x, 'RGBA')


def transform_png_to_rgba(image_path, saved_location):
    """
    @param image_path: The path to the image to edit
    @param saved_location: Path to save the cropped image
    """
    png = Image.open(image_path)
    png.load() # required for png.split()
    background = Image.new("RGB", png.size, (255, 255, 255))
    background.paste(png, mask=png.split()[3]) # 3 is the alpha channel
    background.save(saved_location, 'JPEG', quality=80)


def transform_png_to_rgba2(image_path, saved_location):
    """
    @param image_path: The path to the image to edit
    @param saved_location: Path to save the cropped image
    """
    png = Image.open(image_path)
    png.convert("RGBA")
    png.save(saved_location, "PNG")


if __name__ == '__main__':
    p = "/Users/home/Documents/Projects/Coding/BOTC-Bot/botc/assets/tb_tokens"
    for filename in os.listdir(p):
        if filename.endswith(".png"):
            print(filename)
            path = p + "/" + filename
            new_path = "/Users/home/Documents/Projects/Coding/BOTC-Bot/botc/assets/tb_tokens_rgba/" + filename
            #crop(path, new_path)
            #alpha_to_color(path).save(new_path)
            transform_png_to_rgba2(path, new_path)
