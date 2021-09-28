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
import pytesseract


load_dotenv()
if os.getenv("TESSERACT_BINARY") is not None:
    TESSERACT_BINARY = os.getenv("TESSERACT_BINARY")
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_BINARY
    # on Windows, you can install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki
    # then add the install path to your .env file.
    # This is typically TESSERACT_BINARY = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    
    # on Ubuntu, you can install Tesseract by running `sudo apt install tesseract-ocr` 
    # and then `which tesseract` to find out where it went.
    # This is typically TESSERACT_BINARY = "/usr/bin/tesseract"

    # on Mac, you can install Tesseract by running `brew install tesseract`
    # and then `brew info tesseract` to find out where it went
    # This is typically TESSERACT_BINARY = "/usr/local/Cellar/tesseract"

    # Other settings you can change
    # TESSERACT_ENV = os.getenv("TESSERACT_ENV")
    # TESSERACT_CONFIG = os.getenv("TESSERACT_CONFIG")
    # pytesseract.pytesseract.tesseract_env = TESSERACT_ENV
    # pytesseract.pytesseract.tesseract_config = TESSERACT_CONFIG
else:
    raise RuntimeError("The Tesseract install path is missing from the .env file.")

# Load the filenames inside a given zip file
def get_filenames(zip_filename):
    with zipfile.ZipFile(zip_filename, 'r') as zip_file:
        files_in_zip = zip_file.filelist
    for i, fileinfo in enumerate(files_in_zip):
        files_in_zip[i] = fileinfo.filename
    return files_in_zip
# Working with Zip Files  https://www.geeksforgeeks.org/working-zip-files-python/

# Create a random database for all the story images
def create_random_database(db_filename):
    import datetime
    import re

    def get_random_name():
        return random.choice(["Chickpea","Holmes","XiChi","YoungBlood","PenDragon","Frogurt"])

    def get_random_date():
        start_date = datetime.datetime(2015, 1, 1, 0, 0, 0)
        end_date = datetime.datetime(2021, 12, 31, 23, 59, 59)
        total_seconds = (end_date - start_date).total_seconds()

        random_seconds = random.randrange(total_seconds)
        random_date = start_date + datetime.timedelta(seconds=random_seconds)
        return random_date

    page_filenames = get_filenames(zip_filename="./data/story_images.zip")

    names = []
    dates = []
    for filename in page_filenames:
        names.append(get_random_name())
        dates.append(get_random_date())
        # match = re.search("Photo (\d{4})",filename)
        # if match:
        #     pass
        #     # print(match[1])
        #     story_id = match[1]
        #     transcripts.append(transcript)
        # else:
        #     print(f"can't find {filename}'s story_id")

    user_stories = pd.DataFrame({
        'username':names,
        'submission_datetime':dates,
        'image_url':page_filenames,
    })
    user_stories.to_csv(open(db_filename,'w'), index=False)
    user_stories.head()

# resize so the longest side is max_length
def load_image(filename, max_length=None):
    image = cv2.imread(filename)
    if max_length:
      original_length = max( image.shape[:2] )
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

# Test preprocessing on page 3
def test_exposure():
    stories_archive = "./data/story_images.zip"
    page_filenames = get_filenames(stories_archive)
    with zipfile.ZipFile(stories_archive, 'r') as zip_file:
        page_filename = page_filenames[2]
        raw_data = zip_file.read(page_filename)
        original = cv2.imdecode(np.frombuffer(raw_data, np.uint8), 1)
        mono = make_monochrome(original, block_size=30, c=11, blur=3)  # convert to black and white
        print(page_filename)
        cv2.imshow(mono)

# Visualize the segmented words on a page by drawing the bounding boxes
def markup(page, boxes):
    for row in boxes.to_dict('records'):
        left = row['left'] # 224
        top = row['top'] # 132
        width = row['width'] # 234
        height = row['height'] # 50
        conf = row['conf'] / 100 # 52 / 100
        max = 255
        green = max * conf
        red = max * (1 - conf)
        color = (0, green, red)
        page = cv2.rectangle(page, (left, top), (left+width, top+height), color, 2)
    return page

# Computes the complexity of all words in the 'text' column of a DataFrame
def get_complexity(words, metric='len_count'):
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

    metrics = ['len', 'syl', 'len_count', 'syl_count']
    if metric == 'len':
        words['complexity'] = words['text'].apply(len)

    elif metric == 'syl':
        words['complexity'] = words['text'].apply(count_syllables)

    elif metric == 'len_count':
        length = words['text'].apply(len)
        count = words.groupby('text')['text'].transform('size')
        words['complexity'] = length / count

    elif metric == 'syl_count':
        syl = words['text'].apply(count_syllables)
        count = words.groupby('text')['text'].transform('size')
        words['complexity'] = syl / count
    
    else:
        raise ValueError(f"metric must be one of {['len', 'syl', 'len_count', 'syl_count']} but got '{metric}'")

    # scale the complexities so the sum is 1000
    # words['complexity'] = words['complexity'] / words['complexity'].sum()
    return words['complexity']

# Compute the master scale needed to hit a certain density
def get_scale(boxes, canvas_area, density):
    desired_area = canvas_area * density
    complexity_word_area = sum(boxes.width * boxes.height * boxes.complexity**2)
    scale = sqrt(desired_area / complexity_word_area)

    # print(f'canvas area = {canvas_area:,d}')
    # native_word_area = sum(boxes.width * boxes.height)
    # print(f'native word area = {native_word_area:,d}')
    # print(f'words scaled by complexity = {complexity_word_area:,.0f}')
    # print(f'desired area = {desired_area:,.0f}')
    # scaled_word_area = sum(boxes.width * boxes.height * boxes.complexity**2 * scale**2)
    # print(f'resulting density = {scaled_word_area/canvas_area:.2f}')
    # print(f'scale = {scale:.3f}')
    return scale

# Crop the words out of the page and return them as a list of images in RGBA format
def get_clips(page, mono, boxes, blur=3):
    clips = []
    for row in boxes.to_dict('records'):
        left = row['left'] # 224
        top = row['top'] # 132
        width = row['width'] # 234
        height = row['height'] # 50b_channel, g_channel, r_channel = cv2.split(img)
        BGR = page[top:top+height, left:left+width]  # crop the color image
        B, G, R = cv2.split(BGR)
        A = mono[top:top+height, left:left+width]  # crop out the mask
        A = cv2.GaussianBlur(A, (blur, blur), 0)
        A = 255 - A
        BGRA = cv2.merge((B, G, R, A))
        clips.append(BGRA)
    return clips

# Resizes the cropped words for a given canvas area and density
def scale_clips(boxes, canvas_area, density=0.40):
    master_scale = get_scale(boxes, canvas_area, density=0.40)
    
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
    
# Converts an image to base64 for a given image format
def img_to_base64(image, format='.png'):
    retval, buffer = cv2.imencode(format, image)
    b64_bytes = base64.b64encode(buffer)
    b64_string = b64_bytes.decode()
    return b64_string
    # There are many flags you can use to configure the compression, but they are different for each image format
    # https://docs.opencv.org/4.5.2/d8/d6a/group__imgcodecs__flags.html#ga292d81be8d76901bff7988d18d2b42ac

# Filters the dataframe of whole-page metadata for a given user and date range
# replace this with a SQL query that pulls from a database
def get_pages(user_id, date_range=None):
        pages = pd.read_csv("./data/crop-cloud/stories_db.csv")
        pages["submission_datetime"] = pd.to_datetime(pages["submission_datetime"], infer_datetime_format=True)
        pages = pages[pages["username"] == user_id]
        if date_range is not None:
            start_date, end_date = date_range
            start_date = pd.to_datetime(start_date, infer_datetime_format=True)
            end_date = pd.to_datetime(end_date, infer_datetime_format=True)
            end_date += pd.DateOffset(1)  # so this whole day is included
            
            pages = pages[pages["submission_datetime"] >= start_date]
            pages = pages[pages["submission_datetime"] <= end_date]
        return pages  # a subset of the pages metadata database

# Creates a table of metadata for the words on a page (without adding cropped words to the table)
# This is the slow step, taking 3-5 seconds per page
# One idea is to put this step in the submission pipeline, and cache this page_data
# It may also be possible to speed up this method through multi-threading
# Or through 
def parse_page(page_uri):
    # open zip, read in one image
    stories_archive = "./data/story_images.zip"
    with zipfile.ZipFile(stories_archive, 'r') as zip_file:
        # load and prep image
        raw_data = zip_file.read(page_uri)
    original = cv2.imdecode(np.frombuffer(raw_data, np.uint8), 1)
    mono = make_monochrome(original, block_size=31, c=13, blur=1)  # convert to black and white

    # get and process the bounding boxes of words
    page_data = pytesseract.image_to_data(mono, output_type='dict')  # segment image
    page_data = pd.DataFrame(page_data)
    page_data['conf'] = pd.to_numeric(page_data['conf'], errors='ignore')
    page_data = page_data[ (page_data['text'].str.contains('[A-Za-z]')) & (page_data['text'].str.len() > 2)]
    page_data = page_data[(page_data['width'] / page_data['height']) > 1]
    page_data.drop(columns=['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num'], inplace=True)
    return page_data

# Return a filename without the file extention
def get_root_filename(full_filename):
    filename_parts = full_filename.split('.')
    root_filename = filename_parts[:-1]  # lose the file extention
    root_filename = '.'.join(root_filename)
    return root_filename

# Check the metadata files and regenerate any missing ones
# This is a stand-in until a proper SQL database is created
# This method is untested and will probably need debugging
# Additionally, assemble_page_data() should be refactored to load the metadata that this generates
def fill_metadata_holes():
    page_metadata_file = "./data/page_metadata.zip"
    page_metas = get_filenames(zip_filename = page_metadata_file)
    page_metas = [get_root_filename(page_meta) for page_meta in page_metas]

    page_uris = get_filenames(zip_filename = "./data/story_images.zip")
    all_metadata = []
    for page_uri in page_uris:
        root_uri = get_root_filename(page_uri)
        csv_name = root_uri + '.csv'
        if root_uri not in page_metas:
            page_data = parse_page(page_uri)
        else:
            with zipfile.ZipFile(page_metadata_file, 'r') as zip_file:
                buffer = zip_file.read(page_uri)
            page_data = pd.read_csv(buffer)
        all_metadata.append((csv_name, page_data))

    with zipfile.ZipFile(page_metadata_file, 'w') as zip_session:        
        for csv_name, page_data in all_metadata:
            # convert page_data to a csv buffer
            page_buffer = page_data.to_csv(index=False)

            # write the csv buffer to the file under the filename
            zip_session.writestr(csv_name, page_buffer, compress_type=zipfile.ZIP_DEFLATED)

# Creates a word table for a single page, including the file path, date, and cropped words
# Right now this re-parses all pages from scratch, which is slow
# Refactor to pull saved metadata generated by fill_metadata_holes()
def assemble_page_data(page_specs):
    page_uri = page_specs["image_url"]
    page_data = parse_page(page_uri)
    
    # add the filename and date for this page, repeated on every row
    page_data['page_uri'] = page_uri
    page_data['date'] = page_specs["submission_datetime"]

    # add the cropped words
    with zipfile.ZipFile("./data/story_images.zip", 'r') as zip_file:
        # load and prep image
        raw_data = zip_file.read(page_uri)
        original = cv2.imdecode(np.frombuffer(raw_data, np.uint8), 1)
        mono = make_monochrome(original, blur=1)  # convert to black and white
    page_data['image'] = get_clips(original, mono, page_data, blur=1)

    return page_data

# Collate all the requested pages into one words table, including the file path, date, and cropped words
def get_user_words(user_id, date_range=None, complexity_metric="len_count"):
    pages_data = get_pages(user_id=user_id, date_range=date_range)
    if date_range is not None:
        if len(pages_data) == 1:
            plural = f'is {len(pages_data)} page'
        else:
            plural = f'are {len(pages_data)} pages'
        print(f'There {plural} for {user_id} between {date_range[0]} and {date_range[1]}')

    # load all pages and images into one table
    user_words = pd.DataFrame()
    for page_specs in pages_data.to_dict('records'):
        # returns a table of words with cropped images in RGBA format
        page_data = assemble_page_data(page_specs)
        user_words = pd.concat([user_words,page_data])
    user_words.drop(columns=['left', 'top', 'conf'], inplace=True, errors='ignore')

    # add complexity
    user_words["complexity"] = get_complexity(user_words, metric=complexity_metric)
    user_words.sort_values(by='complexity', ascending=False, inplace=True)
    return user_words

# Map the dates to integers. returns a dictionary
def map_dates(user_words):
    dates = sorted(user_words.date.unique())
    D = len(dates)
    date_map = dict()
    for i, date in enumerate(dates):
        date = pd.to_datetime(date)
        date_map[date] = i
    return date_map

# Picks a random horizontal location for a cropped word
# This is the heart of arranging the words chronologically
def pick_x(canvas_width, word_width, date_number=None, total_dates=None):
    if total_dates:  # this is untested and may need to be debugged
        # for now, this divides the space into even fractions
        # I had wanted to use arc cosine waves to give a fuzzy distribution, but never finished the function bending
        x_float = np.random.uniform(
            low=date_number/total_dates,
            high=(date_number+1)/total_dates,
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
                canvas[y1:y2, x1:x2] = (mask * color + (1-mask) * canvas[y1:y2, x1:x2])
                occupied[y1:y2, x1:x2] = np.logical_or(mask_bool, occupied[y1:y2, x1:x2])
                word_area += (x2-x1) * (y2-y1)
                placed += 1
                break

    # print(f'placed {placed}/{total} words')
    # print(f'there were {collisions} total collisions')
    # canvas_area = canvas.shape[0] * canvas.shape[1]
    # print(f'bounding box density =  {word_area/canvas_area:.2f}')
    # print(f'occupied density = {occupied.sum() / canvas_area:.2f}')

    # cv2.imshow(canvas)
    # cv2.imshow(occupied*255)
    return canvas









# Scaled Multipage Word Data
def get_cropped_words(user_id, date_range=None, complexity_metric="len_count", image_format=".webp", canvas_area=960*686, density=0.40):
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
    user_words = get_user_words(user_id, date_range, complexity_metric)

    # scale the word images
    user_words['image'] = scale_clips(user_words, canvas_area, density)
    # images which would be smaller than 3 pixels in either direction are set to None
    user_words = user_words[user_words.image.notnull()]

    # convert images to base64
    user_words['image_base64'] = user_words['image'].apply(img_to_base64, format=image_format)
    user_words.drop(columns=['image'], inplace=True)

    # print(user_words.head(10))

    # package into json
    words_csv = user_words.to_csv(index=False)
    words_json = json.dumps(words_csv)
    return words_json


def get_crop_cloud(user_id, date_range=None, complexity_metric="len_count", image_format=".webp", canvas_width=1024, density=0.40, max_words=None):
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

    user_words = get_user_words(user_id, date_range, complexity_metric)

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
    
    # `user_id` can be "Chickpea", "Holmes", "XiChi", "YoungBlood", "PenDragon", "Frogurt"
    # `date_range` - Dates were randomly generated between 2015-01-01 and 2021-12-31

    # # Test GET viz/cropped_words, which calls get_cropped_words()
    # words_json = get_cropped_words(
    #     user_id="PenDragon",
    #     date_range=("2019-10-01", "2020-10-31"),
    #     complexity_metric="len",
    #     image_format=".webp",
    #     canvas_area=658560,  # 960*686
    #     density=0.40,
    #     )
    # print(f"words_json is {len(words_json)/1024:,.0f} KB")

    # # Save the json to a sample response
    # with open("cropped_words.json", mode='w') as file:
    #   file.write(words_json)

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
    print(f"crop_cloud_json is {len(crop_cloud_json)/1024:,.0f} KB")

    # Save the json to a sample response
    with open("crop_cloud.json", mode='w') as file:
      file.write(crop_cloud_json)

    # Generate a new random stories database
    # create_random_database("./data/crop-cloud/stories_db.csv")



# XiChi's page dates:
# 2015-09-29 06:46:39
# 2016-02-15 11:01:07
# 2016-07-21 17:09:43
# 2017-04-02 00:57:37
# 2017-04-10 20:44:35
# 2017-07-03 11:18:34
# 2017-08-09 04:45:18
# 2018-02-01 00:00:06
# 2019-03-04 03:01:14
# 2019-04-10 04:44:16
# 2019-06-16 10:00:55
# 2020-10-01 17:19:19
# 2020-10-23 16:33:27
# 2020-11-14 19:31:27

# TODO:
# Features:
# Database Integration:
  # right now, the crop cloud pulls it's data from images and csv's stored in the repo in zip files
  # put this data in SQL tables in an actual database
  # hook the crop cloud code up to the database
# add a GET usernames endpoint so the frontend can add a drop down for usernames
# add a GET submission_dates endpoint (given a user_id) so the frontend can add date pickers to choose a start/end date (maybe)
# Color:
  # convert the submission dates for a given crop cloud to d = date number (starting at 0) and D = number of dates. 
  # colormap choices https://matplotlib.org/2.0.2/examples/color/colormaps_reference.html
  # make a function that converts a float number and the name of a colormap to a color in RGB
  # choose the color for each word based on it's submission date as a float (d/(D-1))
  # put extra blur on the transparency map and layer in a colored blurred halo behind the word
  # add parameters to both crop cloud endpoints: "color_map" and "border_width" so the frontend has artistic control
# Page thumbnails:
  # add page thumbnails in a row across the top of the canvas
  # outline the thumbnails using the same color and border style as the words, so they appear associated
  # submissions that are more than one page should appear as a stack of pages with a single border around the whole stack
# Chronological layout:
  # place words in even fractions just to get something simple working
  # do the math to make the horizontal placement be choosen according to a cosine distribution so the word placements are 
    # loosely connected to which document they came from, and so the overall word density across the canvas is constant
  # put this equation in Desmos to start where I left off
  # \left(1-\frac{\arccos\left(2x-1\right)}{\pi\left(D-1\right)}\right)+\frac{d}{D}
  # https://www.desmos.com/calculator
  # d = date number, D = number of dates. The function should make an arccosine wave that claims a d/D fraction of the vertical interval [0-1]
  # Then pass a uniform random number and d and D into this function and you should get a cosine distribution out
  # place the words according to this fuzzy placement, using d and D to clump the words under their page thumbnails
# under the word cloud draw a timeline (arrow and start and end date (Feb 2021 format)) and make the style look like friendly hand drawn marker

# Robustness, Accuracy and Speed:
# The crop cloud endpoints will currently return a code 500 if you request a date with no documents.
  # This should fail more gracefully. Perhaps return an empty word table or just the canvas image
# Caching word bounding boxes for each page and maybe the cropped words too:
  # debug fill_metadata_holes() so that it caches the bounding box locations of words on each page
  # refactor assemble_page_data() to pull saved bounding box data and page images
  # possibly cache the cropped words in the metadata if the time/space tradeoff looks good
# Preprocessing:
  # add auto-deskewing (rotation < 45 degrees)
  # add auto-orienting the page (rotations of 90 degrees)
  # auto-detect the trapezoid of the page/writing and unwarp that instead of deskewing
  # benchmark and optimize the code. perhaps migrate functions to different libraries.
  # during preprocessing, add standardizing the greyscale histogram to read pencil (they don't allow pen in grade school)
  # do hyperparameter tuning to optimize the accuracy you can get from tesseract without retraining
    # do some reading on optimizing segmentation for OCR
    # bundle the optimized preprocessing steps and parameters into a function (raw image in, ready for OCR image out)
    # give the optimized preprocessing function to the tesseract group
# on tesseract add parameters for which mode, engine, and model to use to improve time and accuracy
# plug in the in house tesseract model when it's better than the out of the box one, and re-optimize the best preprocessing parameters
# Testing:
  # write Unit tests
  # write API tests