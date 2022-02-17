"""
This file will create synthetic data from inputted strings.

"""

import glob
import os
from PIL import Image

# Variables created for functions
cwd = os.path.dirname(os.path.abspath(__file__))
char_list = [[] for i in range(55)]


# Takes a PIL image (im1, img2) and attaches img2 to the right of img1
def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


# Takes a PIL image (im1, img2) and attaches img2 to the bottom of img1
def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


# Creates the list of characters from the folder "character_images"
# These images need to have the letter in the image at the start of the name
def create_char_list():
    supported_file_extensions = ["jpg", "jpeg", "png", "tif", "tiff"]
    img_files = []
    for ext in supported_file_extensions:
        img_files += glob.glob(cwd + f"/character_images/*.{ext}", recursive=True)

    for file_path in img_files:
        file_name = os.path.basename(file_path)[5]
        char_place = get_place_from_char(file_name)

        char_list[char_place].append(Image.open(file_path))


# Gets the list position for the specified character
def get_place_from_char(char: str):
    char_place = ord(char)
    if 91 > char_place > 64:  # Upper case letters
        return char_place - 65
    elif 123 > char_place > 96:  # Lower case letters
        return char_place - 96 + 26
    elif char_place == 32:  # The ' ' white space
        return 53
    elif char_place == 46:  # The '.' period
        return 54
    else:
        return -1


# Returns an image of the character
def get_char_as_image(char: str, handwriting_type: int = 0):
    return char_list[get_place_from_char(char)][handwriting_type]


# Creates a full image from the complete text desired to become synthetic data
def create_image_from_string(sentence: str):
    if sentence is None or len(sentence) == 0:
        return None
    characters = [char for char in sentence.lower()]
    length = len(sentence) * 36 if len(sentence) * 36 < 1500 else 1500
    width = 0

    return_image = None
    row_image = Image.new(mode="RGB", size=(0, 64))

    while len(characters) > 0:
        char = characters.pop(0)
        if char == ' ':
            place = 0
            char_check = '_'
            while char_check != ' ' and place + 1 < len(characters):
                char_check = characters[place]
                place += 1
            if place * 36 + row_image.width > 1500:
                if return_image is None:
                    return_image = Image.new(mode="RGB", size=(length, 0))

                return_image = get_concat_v(return_image, row_image)
                row_image = Image.new(mode="RGB", size=(0, 64))

                char = characters.pop(0)

        char_img = get_char_as_image(char)
        if width + char_img.width > 1500:
            if return_image is None:
                return_image = Image.new(mode="RGB", size=(length, 0))

            return_image = get_concat_v(return_image, row_image)
            row_image = Image.new(mode="RGB", size=(0, 64))
        width += char_img.width
        row_image = get_concat_h(row_image, char_img)

    if return_image is None:
        return_image = Image.new(mode="RGB", size=(length, 0))
    return_image = get_concat_v(return_image, row_image)
    return return_image


create_char_list()
string_for_data = """Once apon a time there was a girl named Mary. On a warm 
sunny day Mary was walking through the woods near hear nouse 
to look for some critters to take pictures of. She loved animals 
and nature all her life even though she was only nine years old 
She thinks that she is going to die soon. She does go to school 
but she isn't that smart. For example Mary recycled a pie 
even though the pie was not even bitten. Another thing she did 
was leave her muffin in the woods while she was traveling with  
her family to Andrea's house which is one of Mary's friends at 
school and Mary's muffin was eaten by a bear that sniffed it 
from far away. Yes. Mary could be a little weird but that is 
just how she is. Back to the real story now. Mary found a 
fox, took a picture she also found a rabbit took a picture 
she found a squirrel and took a picture before it ran away. 
But sooner or later she saw two eyes peeking through a bush 
on the side of the path she was walking on."""
syn_image = create_image_from_string(string_for_data)
processed_path = cwd + "/created_synthetic_data/" + "SYNTHETIC_FILE.png"
# create text file based on string
syn_image.save(processed_path)
with open(cwd + "/created_synthetic_data/" + "SYNTHETIC_FILE.gt.txt", 'w') as f:
    f.write(string_for_data)
