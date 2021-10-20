# Imports
import os
import base64
from math import sqrt
import json
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import cv2
import psycopg2
import imageio

load_dotenv()


def create_connection():
    """
    RDS connection
    returns connection
    """

    DB_NAME = os.getenv("RDS_DB_NAME", default="OOPS")
    DB_USER = os.getenv("RDS_USERNAME", default="OOPS")
    DB_PASSWORD = os.getenv("RDS_PASSWORD", default="OOPS")
    DB_HOST = os.getenv("RDS_HOSTNAME", default="OOPS")
    pg_connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    return pg_connection


def load_image(filename, max_length=None):
    """
    Loads and resizes canvas so the longest side is max_length

    Input:
        `filename` file uri
        `max_length` desired longest size

    Output:
        returns resized canvas
    """
    image = cv2.imread(filename)
    if max_length:
        original_length = max(image.shape[:2])
        scale_factor = max_length / original_length
        image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor)
    return image


def make_monochrome(image, blur=1, block_size=31, c=13):
    """
    Convert the image into black and white, seperating the text from the background

    Input:
        `image` numpy array
        `blur` integer -> for additional smoothing of cropped word array - must be an odd number >= 1
        `block_size` odd sized integer > 1 -> block_size is for smoothing out a varying exposure. too small etches out text. must be an odd number
        `c` integer -> for de-noising. too small and you have noise. too big erodes text

    Output:
        returns numpy grayscale array
    """

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


def deline(image):
    """
    Produces a de-lined image, performed cropped word by cropped word

    Input:
        `image` numpy array

    Output:
        de-lined cropped word image
    """
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


def img_to_base64(image, format='.png'):
    """
    Converts an image to base64 for a given image format

    Inputs:
        `image` numpy dataframe
        `format` - refer to acceptable image formats for base64 encoder

    Output:
        base64 string
    """
    retval, buffer = cv2.imencode(format, image)
    b64_bytes = base64.b64encode(buffer)
    b64_string = b64_bytes.decode()
    return b64_string
    # There are many flags you can use to configure the compression, but they are different for each image format
    # https://docs.opencv.org/4.5.2/d8/d6a/group__imgcodecs__flags.html#ga292d81be8d76901bff7988d18d2b42ac


def get_complexity(words):
    """
    Computes the complexity of all words in the text column of a given dataframe

    Input:
        `words` pandas dataframe of words

    Output:
        complexity column of given pandas dataframe
    """

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

    return words['complexity']


def get_scale(boxes, canvas_area, density):
    """
    Compute the master scale needed to hit a certain density

    Input:
        `boxes` pandas dataframe of user words
        `canvas_area` total area of canvas image
        `density` desired area to fill on canvas

    Output:
        float -- see 'scale_clips' function
    """
    desired_area = canvas_area * density
    complexity_word_area = sum(boxes.width * boxes.height * boxes.complexity ** 2)
    scale = sqrt(desired_area / complexity_word_area)

    return scale


def get_clips(image, blur=1):
    """
    Splits, then rejoins given jpg image into png
    Alpha channel generated using make_monochrome function above

    Input:
        `image` numpy 3 dimensional array
        `blur` odd integer...

    Output:
        `Reformed cropped word with alpha channel`
    """

    B, G, R = cv2.split(image)
    A = make_monochrome(image)
    A = cv2.GaussianBlur(A, (blur, blur), 0)
    A = 255 - A
    BGRA = cv2.merge((B, G, R, A))

    return BGRA


# Resizes the cropped words for a given canvas area and density
def scale_clips(boxes, canvas_area, density=0.40):
    """
    Resizes and returns cropped words based on canvas area, density, and word complexity

    Input:
        `boxes` user words pandas dataframe
        `canvas_area` total area of canvas
        `density` float of desired area to fill on canvas

    Output:
        returns list of cropped words
    """

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


def get_user_words(user_id, date_range=None):
    """
    Produces table of cropped words and word data including:
    image width, height, text and more.

    Input:
        `user_id` string username, select from api listed names
        `date_range` currently not in use.... leave blank
    """
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


def pick_x(canvas_width, word_width, date_number=None, total_dates=None):
    """
    For now... picks random x coordinate for cropped word placement

    Input:
        `canvas_width` canvas.shape[1]
        `word_width` canvas.shape[1]
        `date_number` (not yet used, leave blank)
        `total_dates` (not yet used, leave blank)

    Output:
        random x coordinate integer

    """
    if total_dates:  # this is untested and may need to be debugged
        # for now, this divides the space into even fractions
        # I had wanted to use arc cosine waves to give a fuzzy distribution,
        # but never finished the function bending
        x_float = np.random.uniform(
            low=date_number / total_dates,
            high=(date_number + 1) / total_dates,
        )
    else:
        x_float = np.random.uniform()
    available_room = canvas_width - word_width
    return int(x_float * available_room)


def pick_y(canvas_height, word_height):
    """
    Picks random y coordinate for cropped word placement in 'make_word_cloud'

    Input:
        `canvas_height` canvas.shape[0]
        `word_height` word.shape[0]

    Output:
        random integer
    """

    # Picks a random vertical location for a cropped word
    # This uses a triangular distribution which biases the words towards the midline,
    # where your eyes will start
    y_float = np.random.triangular(0, 0.5, 1)
    available_room = canvas_height - word_height
    return int(y_float * available_room)


def bungie(arr, frame, pic_width, pic_height):
    """
    Produces animation for a wiggle style of movement

    Input:
        `arr` array of single x and y coordinate
        `frame` frame number for positional reference
        `pic_width` image.shape[1]
        `pic_height` image.shape[0]

    Output:
        returns pixel adjustment for y coordinate
    """
    # function math below
    x_pos = frame
    frame = ((2 * np.pi) / 12) * frame
    b = np.pi / pic_width
    x = b * arr
    pre = np.sin(x)
    a = 1 / (pic_width * .15)
    pixel_position = (pre / a)
    factor = np.sin(frame)

    x_pos = (1 / 12) * x_pos
    eulers = np.e ** -((9 * x_pos) - 5)
    eulers += 1
    eulers = 1 / eulers
    factor = factor - (eulers * factor)

    pixel_position = pixel_position * factor
    return int(pixel_position)


def wiggle(arr, frame, pic_width, pic_height):
    """
    Produces animation for a wiggle style of movement

    Input:
        `arr` array of single x and y coordinate
        `frame` frame number for positional reference
        `pic_width` image.shape[1]
        `pic_height` image.shape[0]

    Output:
        returns pixel adjustment for y coordinate
    """
    frame = ((2 * np.pi) / 12) * frame
    b = (8 * np.pi) / pic_width
    x = b * arr
    pre = np.sin(x)
    a = 1 / (pic_width * pic_height * .0005)
    pixel_position = (pre / a) * np.sin(frame)
    return int(pixel_position)


def boogie(arr, frame, pic_width, pic_height):
    """
    Produces animation for a wiggle style of movement

    Input:
        `arr` array of single x and y coordinate
        `frame` frame number for positional reference
        `pic_width` image.shape[1]
        `pic_height` image.shape[0]

    Output:
        returns fully adjusted coordinates
    """
    # boogie function math below:
    frame = ((2 * np.pi) / 12) * frame
    frame = np.sin(frame) / 5
    height = pic_height / 2
    width = pic_width / 10

    to_be_sin = arr[1] * (4 * np.pi) / pic_width
    sin = np.sin(to_be_sin)
    final_y = height * frame * sin

    to_be_cos = arr[0] * np.pi / pic_height
    cos = np.cos(to_be_cos)
    final_x = width * frame * cos

    return [final_y + arr[0], final_x + arr[1]]


def spinner(arr1, frame, img):
    """
    Produces spinning movement canvas by canvas

    Input:
        'arr1' array of single x and y coordinate
        'frame' frame number for positional reference

    Output:
        'x and y adjustment for cropping'
    """

    def formula(frame):
        numerator = (frame - 6) ** 2
        denominator = 2 * 2 * 2
        exp = -(numerator / denominator)
        eul = 3 * (np.e ** exp)
        frame = ((3 * np.pi) / 12) * eul
        return frame

    # spins word in place
    angle = formula(frame) - formula(frame - 1)
    arr = arr1.copy()
    arr = np.array(arr, np.float64)
    a = np.cos(angle)
    b = -np.sin(angle)
    c = np.sin(angle)
    d = np.cos(angle)
    arr[0] -= (img.shape[0] // 2)
    arr[1] -= (img.shape[1] // 2)
    if frame != 0:
        prev_angle = formula(frame - 1) - formula(frame - 2)
        if frame == 1:
            if prev_angle > angle:
                arr[0] -= ((arr[1] / ((img.shape[1] / 4) - (2 * (abs(angle) - abs(prev_angle))))) ** 3) / 2
            else:
                arr[0] += ((arr[1] / ((img.shape[1] / 4) - (2 * (abs(angle) - abs(prev_angle))))) ** 3) / 2
        else:
            if prev_angle > angle:
                arr[0] -= (arr[1] / ((img.shape[1] / 5.4) - (5 * (abs(angle) - abs(prev_angle))))) ** 3
            else:
                arr[0] += (arr[1] / ((img.shape[1] / 5.4) - (5 * (abs(angle) - abs(prev_angle))))) ** 3
    rotation_matrix = np.array([[a, b],
                                [c, d]])
    new_coords = np.array(arr) * rotation_matrix
    new_coords = np.sum(new_coords, 1)

    new_coords += np.array(((img.shape[0] // 2), (img.shape[1] // 2)))
    return new_coords


def render_movement(positive_arrays, moving_images, canvas, static_arrays, static_positives):
    """
    Function creates a set of canvases to make up final gif

    Input:
        `positive arrays` arrays that point to specifically occupied locations on image arrays, used for moving images
        `moving_images` set of images that are designated for some kind of movement
        `canvas` blank canvas loaded from cream_paper, in numpy array format
        `static_arrays` images to be redrawn but not moved
        `static_positives` positive arrays for reference to static_images

    Output:
        canvas_set -> array of filled in canvases
    """

    # target for progress tally to hit
    target = len(moving_images)
    # progress tally (see implementation below)
    progress = 0
    # canvas set to be returned
    canvas_set = []
    # word croppings currently in motion
    in_motion = []
    # positives for word croppings in motion
    in_motion_positives = []
    # counter is dummy variable to decide when image should begin moving... creates sense of asynchronicity
    counter = 0
    # move_type (below) rotates through 4 numbers [0 - 3]; used for animation type selection
    move_type = 0
    while True:
        canvas_to_app = canvas.copy()
        # place statics first, then moving images that arent currently in motion:
        for i, image in enumerate(static_arrays):
            pos = static_positives[i]
            y1 = pos[1]
            x1 = pos[2]
            for coord in pos[0]:
                canvas_to_app[coord[0] + y1][coord[1] + x1] = image[coord[0]][coord[1]] * coord[2] + (
                        (1 - coord[2]) * canvas_to_app[coord[0] + y1][coord[1] + x1])
        for i, image in enumerate(moving_images):
            pos = positive_arrays[i]
            y1 = pos[1]
            x1 = pos[2]
            for coord in pos[0]:
                canvas_to_app[coord[0] + y1][coord[1] + x1] = image[coord[0]][coord[1]] * coord[2] + (
                        (1 - coord[2]) * canvas_to_app[coord[0] + y1][coord[1] + x1])
        # now place the moving images:
        # if counter indicates, start animating new image
        if counter % 17 == 0 or counter % 29 == 0:
            if len(moving_images) != 0:
                begin_moving = moving_images.pop()
                begin_moving_also = positive_arrays.pop()
                in_motion.append([begin_moving, move_type, 0])
                in_motion_positives.append(begin_moving_also)
        counter += 1
        for i, temp in enumerate(in_motion):
            pos = in_motion_positives[i]
            image = temp[0]
            move_type_ind = temp[1]
            # total animation canvas length is 12 frames for each animation.. Once that number is hit
            # animation frame is hard set to 0
            if temp[2] == 12:
                frame = 0
                progress += 1
            else:
                frame = temp[2]
                temp[2] += 1
            # these variables are extracted to configure arrays to appropriate location, decided in
            # 'make_crop_cloud'.
            y1 = pos[1]
            x1 = pos[2]
            if move_type_ind == 1:
                for coord in pos[0]:
                    # for bungee movement
                    coord_ind2 = coord[1] + x1
                    if i % 2 == 0:
                        coord_ind1 = bungie(coord[1], frame, image.shape[1], image.shape[0]) + y1 + coord[0]
                    else:
                        coord_ind1 = -bungie(coord[1], frame, image.shape[1], image.shape[0]) + y1 + coord[0]

                    if 0 < coord_ind1 < canvas_to_app.shape[0]:
                        canvas_to_app[coord_ind1][coord_ind2] = image[coord[0]][coord[1]] * coord[2] + (
                                (1 - coord[2]) * canvas_to_app[coord_ind1][coord_ind2])
            elif move_type_ind == 0:
                for coord in pos[0]:
                    # for bungee movement
                    coord_ind2 = coord[1] + x1
                    coord_ind1 = wiggle(coord[1], frame, image.shape[1], image.shape[0]) + y1 + coord[0]
                    if 0 < coord_ind1 < canvas_to_app.shape[0]:
                        canvas_to_app[coord_ind1][coord_ind2] = image[coord[0]][coord[1]] * coord[2] + (
                                (1 - coord[2]) * canvas_to_app[coord_ind1][coord_ind2])
            elif move_type_ind == 2:
                for coord in pos[0]:
                    coords = spinner(coord[:2], frame, image)
                    coord_ind2 = int(coords[1] + x1)
                    coord_ind1 = int(coords[0] + y1)
                    if 0 < coord_ind1 < canvas_to_app.shape[0] and 0 < coord_ind2 < canvas_to_app.shape[1]:
                        canvas_to_app[coord_ind1][coord_ind2] = image[coord[0]][coord[1]] * coord[2] + (
                                (1 - coord[2]) * canvas_to_app[coord_ind1][coord_ind2])
            elif move_type_ind == 1:
                for coord in pos[0]:
                    coords = boogie(coord[:2], frame, image.shape[1], image.shape[0])
                    coord_ind1 = int(coords[0] + y1)
                    coord_ind2 = int(coords[1] + x1)
                    if 0 < coord_ind1 < canvas_to_app.shape[0] and 0 < coord_ind2 < canvas_to_app.shape[1]:
                        canvas_to_app[coord_ind1][coord_ind2] = image[coord[0]][coord[1]] * coord[2] + (
                                (1 - coord[2]) * canvas_to_app[coord_ind1][coord_ind2])
        canvas_set.append(canvas_to_app)
        # if target is hit: function returns completed canvas set.
        # if not, progress is set to 0
        if progress == target:
            break
        else:
            progress = 0
        move_type = (move_type + 1) % 4
    return canvas_set


def make_crop_cloud(canvas, boxes):
    """
    Propose a location for the word
    does this location collide with anything already placed?
    if not, then place the word
    OpenCV uses [y:x] coordinates for images

    Input:
        `canvas`: numpy array read from cream_paper.jpg
        `boxes`: user word pandas dataframe containing image column (full of numpy arrays)

    Output:
        list of arrays -> canvas, moving_images, positive_arrays, static_arrays, static_positives
        necessary for crop-cloud animation
    """

    occupied = np.zeros(shape=(canvas.shape[:2]), dtype=bool)
    placed = 0
    switch = 0
    collisions = 0
    word_area = 0
    moving_images = []
    positive_arrays = []
    static_arrays = []
    static_positives = []
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
                if switch < 10:
                    moving_images.append(color)
                    alt_arr = []
                    for i in range(mask.shape[0]):
                        for j in range(mask.shape[1]):
                            if mask[i][j] != 0:
                                alt_arr.append([i, j, mask[i][j][0]])
                    positive_arrays.append([alt_arr, y1, x1])
                else:
                    static_arrays.append(color)
                    alt_arr = []
                    for i in range(mask.shape[0]):
                        for j in range(mask.shape[1]):
                            if mask[i][j] != 0:
                                alt_arr.append([i, j, mask[i][j][0]])
                    static_positives.append([alt_arr, y1, x1])
                switch += 1
                break
        if placed == 100:
            break

    return canvas, moving_images, positive_arrays, static_arrays, static_positives


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
        saves 'giffy.gif' to local directory
    """

    user_words = get_user_words(user_id, date_range)

    # load the canvas
    canvas = load_image("data/crop-cloud/cream_paper.jpg", max_length=canvas_width)
    canvas_area = canvas.shape[0] * canvas.shape[1]
    # scale the word images
    user_words['image'] = scale_clips(user_words, canvas_area, density)
    user_words.sort_values(by='complexity', ascending=False, inplace=True)
    # images which would be smaller than 3 pixels wide are set to None
    user_words = user_words[user_words.image.notnull()]
    user_words['image'].apply(deline)
    crop_cloud, moving_images, positive_arrays, static_arrays, static_positives = make_crop_cloud(canvas, user_words)

    # return set of canvases rendering movement
    canvas = load_image("data/crop-cloud/cream_paper.jpg", max_length=canvas_width)
    canvas_set = render_movement(positive_arrays, moving_images, canvas, static_arrays, static_positives)

    imageio.mimsave('giffy.gif', canvas_set, fps=15)

    return 'success'


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
