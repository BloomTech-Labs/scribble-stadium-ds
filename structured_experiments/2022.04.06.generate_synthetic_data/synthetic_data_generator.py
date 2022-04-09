"""
Original Author : Elijah Day
Experiment : 2022.02.17.synthetic_generation

Data generated from the original file caused the model to over-fit. This edit and inclusion of the preprocess_data.py
functionality attempts to generate enough data to fit the model with enough variance to mitigate over-fitting.
The original code is left intact except to address the model results.
"""

import glob
import os
import sys
from PIL import Image
import preprocess_data

# Variables created for functions
cwd = os.path.dirname(os.path.abspath(__file__))
processed_path = sys.argv[1] + "/"
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
# These images need to have the letter on the 6th letter which I put "char-" before.
# Needed since starting a file name with '.' or ' ' creates slight issues
def create_char_list():
    supported_file_extensions = ["jpg", "jpeg", "png", "tif", "tiff"]
    img_files = []
    for ext in supported_file_extensions:
        img_files += glob.glob(
            cwd + f"/data/character_images/*.{ext}", recursive=True)

    print(cwd)
    for file_path in img_files:
        file_char = os.path.basename(file_path)[5]
        char_place = get_place_from_char(file_char)

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
    characters = [char for char in sentence.upper()]
    length = len(sentence) * 36 if len(sentence) * 36 < 1500 else 1500
    width = 0

    return_image = None
    row_image = Image.new(mode="RGB", size=(0, 64))

    return_string = ""

    while len(characters) > 0:
        char = characters.pop(0)
        if char == "\n":
            continue
        if char == ' ':
            place = 0
            place_width = 0
            char_check = '_'
            while char_check != ' ' and place + 1 < len(characters):
                char_check = characters[place]
                if char_check == "\n":
                    place += 1
                    continue
                place_width += get_char_as_image(char_check).width
                place += 1
            if place_width + row_image.width > 1500:
                if return_image is None:
                    return_image = Image.new(mode="RGB", size=(length, 0))

                return_image = get_concat_v(return_image, row_image)
                row_image = Image.new(mode="RGB", size=(0, 64))
                width = 0

                char = characters.pop(0)
                return_string += '\n'

        char_img = get_char_as_image(char)
        return_string += char
        if char_img is None:
            continue

        if width + char_img.width > 1500:
            if return_image is None:
                return_image = Image.new(mode="RGB", size=(length, 0))

            return_image = get_concat_v(return_image, row_image)
            row_image = Image.new(mode="RGB", size=(0, 64))
            width = 0
        width += char_img.width
        row_image = get_concat_h(row_image, char_img)

    if return_image is None:
        return_image = Image.new(mode="RGB", size=(length, 0))
    return_image = get_concat_v(return_image, row_image)
    return return_image


# Lists to create different variations of a sentence
nouns = ["dog", "cat", "rat", "mouse", "kitty", "doggy", "rabbit", "bunny", "snake", "snail", "squirrel", "bird",
         "rodent", "duck", "goose", "zebra", "fox", "owl"]
verbs = ["jumps", "runs", "zooms", "swims", "dives", "sprints", "stalks", "submits", "catches", "chases", "claws"]
preps = ["towards", "inside", "under", "around", "behind", "beside", "above", "below", "within", "over"]
places = ["bridge", "school", "house", "office", "hospital", "castle", "court", "cafe", "library", "store", "box"]


# Create new string with a certain pattern
def create_simple_string(n: int, v: int, pr: int, pl: int):
    return f"the {nouns[n]} {verbs[v]} {preps[pr]} the {places[pl]}."


# Setup the character image list
create_char_list()
list_of_string_pairs = []

# Loops through every variation of nouns/verbs and creates a string from them
for i in range(len(nouns)):
    for j in range(len(verbs)):
        for k in range(len(preps)):
            for l in range(len(places)):
                list_of_string_pairs.append((str(i) + "-" + str(j) + "-" + str(k) + "-" + str(l),
                                             create_simple_string(i, j, k, l)))


list_of_string_pairs.append(("hello-world", "hello world"))
list_of_string_pairs.append(("cats", "cats catch mice"))
list_of_string_pairs.append(("dogs", "dogs chase cars"))

# Whatever has been added to the list_of_string_pairs will be created to an image
for file_name, text_data in list_of_string_pairs:

    syn_image = create_image_from_string(text_data)

    syn_image.save(processed_path + file_name + ".png")
    with open(processed_path + file_name + ".gt.txt", 'w') as f:
        f.write(text_data)
