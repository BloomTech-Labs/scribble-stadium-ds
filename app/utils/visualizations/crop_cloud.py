# Function to produce a json file for web to display a Plotly line graph that
# maps the history of a specific student's submission scores

# Imports
import os
import base64
from math import sqrt
import random
import json
import zipfile
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import cv2
import psycopg2

load_dotenv()


def create_connection():
    """RDS connection"""
    # connect to ElephantSQL-hosted PostgreSQL
    DB_NAME = os.getenv("RDS_DB_NAME", default="OOPS")
    DB_USER = os.getenv("RDS_USERNAME", default="OOPS")
    DB_PASSWORD = os.getenv("RDS_PASSWORD", default="OOPS")
    DB_HOST = os.getenv("RDS_HOSTNAME", default="OOPS")
    pg_connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    return pg_connection


# resize so the longest side is max_length
def load_image(filename, max_length=None):
    image = cv2.imread(filename)
    if max_length:
        original_length = max(image.shape[:2])
        scale_factor = max_length / original_length
        image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
    return image


# Convert the image into black and white, separating the text from the background
def make_monochrome(image, blur=1, block_size=31, c=13):
    # blur must be an odd number >= 1
    # block_size is for smoothing out a varying exposure. too small etches out text. must be an odd number > 1
    # c is for denoising. too small and you have noise. too big erodes text.

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert to grayscale
    image = cv2.adaptiveThreshold(
        src=image,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=block_size,
        C=c)
    if blur > 1:
        image = cv2.GaussianBlur(image, (blur, blur), 0)
    return image


# Implementation of simple de-lining algorithm, performed cropped word by cropped word
def deline(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Remove horizontal
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (255, 255, 255), 2)

    # Repair image (this part doesnt seem to be doing its job as well...)
    repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 8))
    result = 255 - cv2.morphologyEx(255 - image, cv2.MORPH_OPEN, repair_kernel, iterations=2)
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            image[i][j][0], image[i][j][2] = image[i][j][2], image[i][j][0]
    return result


# Visualize the segmented words on a page by drawing the bounding boxes
def markup(page, boxes):
    for row in boxes.to_dict('records'):
        left = row['left']  # 224
        top = row['top']  # 132
        width = row['width']  # 234
        height = row['height']  # 50
        conf = row['conf'] / 100  # 52 / 100
        max = 255
        green = max * conf
        red = max * (1 - conf)
        color = (0, green, red)
        page = cv2.rectangle(page, (left, top), (left + width, top + height), color, 2)
    return page


# Converts an image to base64 for a given image format
def img_to_base64(image, format='.png'):
    retval, buffer = cv2.imencode(format, image)
    b64_bytes = base64.b64encode(buffer)
    b64_string = b64_bytes.decode()
    return b64_string
    # There are many flags you can use to configure the compression, but they are different for each image format
    # https://docs.opencv.org/4.5.2/d8/d6a/group__imgcodecs__flags.html#ga292d81be8d76901bff7988d18d2b42ac


# Computes the complexity of all words in the 'text' column of a DataFrame
def get_complexity(words):
    # Import the csv file of words that don't fit into the complexity metric
    complex_words = pd.read_csv(
        '../../../data/crop-cloud/complex_words.csv'
    )

    # https://medium.com/@mholtzscher/programmatically-counting-syllables-ca760435fab4
    def count_syllables(word):
        word = word.lower()
        syllable_count = 0
        vowels = 'aeiouy'
        if len(word) == 0:
            return 0
        if word[0] in vowels:
            syllable_count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                syllable_count += 1
        if word.endswith('e'):
            syllable_count -= 1
        if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
            syllable_count += 1
        if syllable_count == 0:
            syllable_count = 1
        return syllable_count

    words['count'] = words.groupby('text')['text'].transform('size')

    # make a column for letter counts
    words['len'] = words['text'].apply(len)

    # column for syllable count
    words['syllables'] = words['text'].apply(count_syllables)

    # make a column for how complex a word is

    # first setting words that are in the complex_words with their set complexity
    # these are words at higher grade levels, that don't work with the complexity metric
    vdic = pd.Series(complex_words.complexity.values, index=complex_words.word).to_dict()
    words.loc[words.text.isin(vdic.keys()), 'complexity'] = words.loc[words.text.isin(vdic.keys()), 'text'].map(vdic)

    # then filling in the rest with the complexity metric
    words['complexity'] = words['complexity'].fillna(words['syllables'] + words['len'])
    words = words.astype({"complexity": int})

    # Dividing the complexity by how many times the word appears in the story
    words['complexity'] = words['complexity'] / words['count']
    words = words.sort_values(by=['complexity'], ascending=False)

    # Returns the words df columns 'word' and 'complexity' and rows up to how many are selected (default=20)
    return words['complexity']


# Compute the master scale needed to hit a certain density
def get_scale(boxes, canvas_area, density):
    desired_area = canvas_area * density
    complexity_word_area = sum(boxes.width * boxes.height * boxes.complexity ** 2)
    scale = sqrt(desired_area / complexity_word_area)

    return scale


# Crop the words out of the page and return them as a list of images in RGBA format
def get_clips(image, blur=1):
    """splits, then rejoins into png"""

    B, G, R = cv2.split(image)
    A = make_monochrome(image)
    A = cv2.GaussianBlur(A, (blur, blur), 0)
    A = 255 - A
    BGRA = cv2.merge((B, G, R, A))

    return BGRA


# Resizes the cropped words for a given canvas area and density
def scale_clips(boxes, canvas_area, density=0.40):
    master_scale = get_scale(boxes, canvas_area, density=density)

    scaled_clips = []
    for row in boxes.to_dict('records'):
        image_scale = master_scale * row['complexity']
        image = row['image']
        new_y = int(image.shape[0] * image_scale)
        new_x = int(image.shape[1] * image_scale)
        if new_x < 3 or new_y < 3:
            scaled_clips.append(None)
            continue
        new_size = (new_x, new_y)

        if image_scale < 1:
            resize_algo = cv2.INTER_AREA  # recommended for shrinking
        else:
            resize_algo = cv2.INTER_CUBIC  # recommended for enlarging
        image = cv2.resize(image, dsize=new_size, interpolation=resize_algo)
        scaled_clips.append(image)
    return scaled_clips


# Collate all the requested pages into one words table, including the file path, date, and cropped words
def get_user_words(user_id, date_range=None):
    conn = create_connection()
    curs = conn.cursor()
    if date_range[0] != 'None':
        query = f"""SELECT * FROM images WHERE date BETWEEN '{date_range[0]}' and '{date_range[1]}' AND
        username='{user_id}' LIMIT 200"""
    else:
        query = f"""SELECT * FROM images WHERE username='{user_id}' LIMIT 600"""

    curs.execute(query)
    user_words = pd.DataFrame(columns=['width', 'height', 'text', 'page_uri', 'date', 'image', 'complexity'])
    for row in curs.fetchall():
        new_row = pd.DataFrame(columns=['width', 'height', 'text', 'page_uri', 'date', 'image', 'complexity'])
        new_row['width'] = [row[0]]
        new_row['height'] = [row[1]]
        new_row['text'] = [row[2]]
        new_row['page_uri'] = [row[3]]
        new_row['date'] = [row[4]]
        with open('here.png', 'wb') as fp:
            fp.write(row[6])
            fp.close()
        image = cv2.imread('here.png')
        image = get_clips(image)
        new_row['image'] = [image]
        new_row['complexity'] = [row[7]]
        user_words = pd.concat([user_words, new_row], ignore_index=True)
    user_words.sort_values(by='complexity', ascending=False, inplace=True)

    return user_words


# Picks a random horizontal location for a cropped word
# This is the heart of arranging the words chronologically
def pick_x(canvas_width, word_width, date_number=None, total_dates=None):
    if total_dates:  # this is untested and may need to be debugged
        # for now, this divides the space into even fractions
        # I had wanted to use arc cosine waves to give a fuzzy distribution, but never finished the function bending
        x_float = np.random.uniform(
            low=date_number / total_dates,
            high=(date_number + 1) / total_dates,
        )
    else:
        x_float = np.random.uniform()
    available_room = canvas_width - word_width
    return int(x_float * available_room)


# Picks a random vertical location for a cropped word
# This uses a triangular distribution which biases the words towards the midline, where your eyes will start
def pick_y(canvas_height, word_height):
    y_float = np.random.triangular(0, 0.5, 1)
    available_room = canvas_height - word_height
    return int(y_float * available_room)


# Constructs and renders a crop cloud. Returns an image
def make_crop_cloud(canvas, boxes):
    # propose a location for the word
    # does this location collide with anything already placed?
    # if not, then place the word
    # OpenCV uses [y:x] coordinates for images

    occupied = np.zeros(shape=(canvas.shape[:2]), dtype=bool)
    placed = 0
    collisions = 0
    total = len(boxes)
    word_area = 0
    for row in boxes.to_dict('records'):
        image = row['image']

        max_attempts = 20
        failed_attempts = 0
        while failed_attempts < max_attempts:
            # pick a horizontal position
            x1 = pick_x(
                canvas_width=canvas.shape[1],
                word_width=image.shape[1],
                date_number=0,
                total_dates=1,
            )
            x2 = x1 + image.shape[1]

            # pick a vertical position
            y1 = pick_y(canvas_height=canvas.shape[0], word_height=image.shape[0])
            y2 = y1 + image.shape[0]

            R, G, B, mask = cv2.split(image)  # split the image into channels
            color = cv2.merge((B, G, R))
            mask = np.atleast_3d(mask) / 255

            mask_bool = mask.reshape(mask.shape[:2]).astype('bool')
            intersection = np.logical_and(mask_bool, occupied[y1:y2, x1:x2])

            if intersection.sum() > 0:
                # reject this placement
                failed_attempts += 1
                collisions += 1
                continue
            else:
                # place the word
                canvas[y1:y2, x1:x2] = (mask * color + (1 - mask) * canvas[y1:y2, x1:x2])
                occupied[y1:y2, x1:x2] = np.logical_or(mask_bool, occupied[y1:y2, x1:x2])
                word_area += (x2 - x1) * (y2 - y1)
                placed += 1
                break

    return canvas


# Scaled Multipage Word Data
def get_cropped_words(user_id, date_range=None, complexity_metric="len_count", image_format=".webp",
                      canvas_area=960 * 686, density=0.40):
    """
    Produces a table of cropped words for all pages belonging to the given user over a date range

    Input:
        `user_id` str - a string containing the username
        `date_range` List[str] - a list of two dates in the format of YYYY-MM-DD
        `complexity_metric` str - how to calculate the complexity of words (from 'len', 'syl', 'len_count', 'syl_count')
        `image_format` str - the format of the cropped word images (from '.png', '.webp', or anything OpenCV supports)
        `canvas_area` int - the area of the canvas in pixels
        `density` float - the bounding box area of the cropped words divided by the canvas area

    Output:
        json(csv([width, height, text, page_uri, date, complexity, image_base64])) - a table of the cropped words
    """
    user_words = get_user_words(user_id, date_range)
    user_words['complexity'] = get_complexity(user_words)

    # scale the word images
    user_words['image'] = scale_clips(user_words, canvas_area, density)
    # images which would be smaller than 3 pixels in either direction are set to None
    user_words = user_words[user_words.image.notnull()]

    # convert images to base64
    user_words['image_base64'] = user_words['image'].apply(img_to_base64, format=image_format)
    user_words.drop(columns=['image'], inplace=True)

    # package into json
    words_csv = user_words.to_csv(index=False)
    words_json = json.dumps(words_csv)
    return words_json


def get_crop_cloud(user_id, date_range=None, complexity_metric="len_count", image_format=".webp", canvas_width=1024,
                   density=0.40, max_words=None):
    """
    Renders and returns a whole crop cloud for a user's submissions over a given date range

    Input:
        `user_id` str - a string containing the username
        `date_range` List[str] - a list of two dates in the format of YYYY-MM-DD
        `complexity_metric` str - how to calculate the complexity of words (from 'len', 'syl', 'len_count', 'syl_count')
        `image_format` str - the format of the cropped word images (from '.png', '.webp', or anything OpenCV supports)
        `width` int - the width of the crop cloud in pixels
        `density` float - the bounding box area of the cropped words divided by the canvas area
        `max_words` int - the max number of words to include in the cloud

    Output:
        json(image_base64) - a rendered crop cloud as an image
    """

    user_words = get_user_words(user_id, date_range)
    user_words['complexity'] = get_complexity(user_words)

    # load the canvas
    canvas = load_image("./data/crop-cloud/cream_paper.jpg", max_length=canvas_width)
    canvas_area = canvas.shape[0] * canvas.shape[1]

    # scale the word images
    user_words['image'] = scale_clips(user_words, canvas_area, density)
    # images which would be smaller than 3 pixels wide are set to None
    user_words = user_words[user_words.image.notnull()]

    # display(user_words)

    crop_cloud = make_crop_cloud(canvas, user_words[:max_words])
    # cv2.imshow("crop cloud", crop_cloud)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # package into json
    crop_cloud_base64 = img_to_base64(crop_cloud, format=image_format)
    crop_cloud_json = json.dumps(crop_cloud_base64)
    return crop_cloud_json


if __name__ == "__main__":
    # Test GET viz/crop_cloud, which calls get_crop_cloud()
    crop_cloud_json = get_crop_cloud(
        user_id="PenDragon",
        date_range=("2019-10-01", "2020-10-31"),
        complexity_metric="len",
        image_format=".webp",
        canvas_width=960,
        density=0.40,
        max_words=200,
    )
    print(f"crop_cloud_json is {len(crop_cloud_json) / 1024:,.0f} KB")

    # Save the json to a sample response
    with open("crop_cloud.json", mode='w') as file:
        file.write(crop_cloud_json)
