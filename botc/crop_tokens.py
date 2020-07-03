from PIL import Image

import os

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


if __name__ == '__main__':
    for filename in os.listdir("/Users/home/Documents/Projects/Coding/BOTC-Bot/botc/assets/bmr_tokens"):
        if filename.endswith(".png"):
            print(filename)
            path = "/Users/home/Documents/Projects/Coding/BOTC-Bot/botc/assets/bmr_tokens/" + filename
            new_path = "/Users/home/Documents/Projects/Coding/BOTC-Bot/botc/assets/bmr_tokens_cropped/" + filename
            crop(path, new_path)