# Function to produce a json file for web to display a Plotly line graph that
# maps the history of a specific student's submission scores

# Imports
import os
import base64
import json
from zipfile import ZipFile
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
    # This is typically TESSERACT_BINARY = "C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    # on Ubuntu, you can install Tesseract by running `sudo apt install tesseract-ocr` 
    # and then `which tesseract to find out where it went.
    # This is typically TESSERACT_BINARY = "/usr/bin/tesseract"

    # Other settings you can change
    # TESSERACT_ENV = os.getenv("TESSERACT_ENV")
    # TESSERACT_CONFIG = os.getenv("TESSERACT_CONFIG")
    # pytesseract.pytesseract.tesseract_env = TESSERACT_ENV
    # pytesseract.pytesseract.tesseract_config = TESSERACT_CONFIG
else:
    raise RuntimeError("The Tesseract install path is missing from the .env file.")
class PageQuery():
    def __init__(self):
        # load user stories
        
        self.all_pages = pd.read_csv("./data/37_stories_meta.csv")
        self.all_pages["submission_datetime"] = pd.to_datetime(self.all_pages["submission_datetime"], infer_datetime_format=True)

    def get_pages(self, user_id, date_range=None):
        pages = self.all_pages
        pages = pages[pages["username"] == user_id]
        if date_range is None:
            start_date = end_date = None
        else:
            start_date, end_date = date_range
            start_date = pd.to_datetime(start_date, infer_datetime_format=True)
            end_date = pd.to_datetime(end_date, infer_datetime_format=True)
            pages = pages[pages["submission_datetime"] >= start_date]
            pages = pages[pages["submission_datetime"] <= end_date]
        return pages  # a subset of the pages metadata database

def make_monochrome(image, block_size, c, blur):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert to grayscale

    # thresh = 255 - cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    block_size = 31  # for smoothing out a varying exposure. too small etches out text. must be an odd number > 1
    c = 13  # denoising. too small and you have noise, too big erodes text
    image = cv2.adaptiveThreshold(
        src=image,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=block_size,
        C=c)
    
    if blur > 1:
        image = cv2.GaussianBlur(image, (blur, blur), 0)
    # image = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    return image

def parse_page(page_filename, date, format):
    # open zip, read in one image
    stories_archive = "./data/37_story_images.zip"
    with ZipFile(stories_archive, 'r') as zip_file:
        # load and prep image
        raw_data = zip_file.read(page_filename)
        original = cv2.imdecode(np.frombuffer(raw_data, np.uint8), 1)
        mono = make_monochrome(original, block_size=30, c=11, blur=1)  # convert to black and white

        # get the bounding boxes of words
        page_data = pytesseract.image_to_data(mono, output_type='dict')  # segment image

        # process the bounding boxes
        page_data = pd.DataFrame(page_data)
        page_data['conf'] = pd.to_numeric(page_data['conf'], errors='ignore')
        page_data = page_data[ (page_data['text'].str.contains('[A-Za-z]')) & (page_data['text'].str.len() > 2)]
        # page_data['aspect_ratio'] = page_data['width'] / page_data['height']  # wider is larger
        page_data = page_data[(page_data['width'] / page_data['height']) > 1]
        page_data.drop(columns=['level', 'page_num', 'block_num', 'par_num', 'line_num', 'word_num'], inplace=True)

        # add the filename and date for this page, repeated on every row
        page_data["complexity"] = get_complexity(page_data, metric='len_count')
        page_data['filename'] = page_filename
        page_data['date'] = date

        # add the 
        clips = get_clips(original, mono, page_data, format)
        page_data['image_base64'] = clips

        return page_data

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

# crop the words out of the page and return them as a list of images in the same order as boxes
def get_clips(page, mono, boxes, format='.png'):
    clips = []
    for row in boxes.to_dict('records'):
        left = row['left'] # 224
        top = row['top'] # 132
        width = row['width'] # 234
        height = row['height'] # 50b_channel, g_channel, r_channel = cv2.split(img)
        color = page[top:top+height, left:left+width]  # crop the color image
        B, G, R = cv2.split(color)
        A = mono[top:top+height, left:left+width]  # crop out the mask
        A = cv2.GaussianBlur(A, (3, 3), 0)
        A = 255 - A
        BGRA = cv2.merge((B, G, R, A))

        retval, buffer = cv2.imencode(format, BGRA)
        # https://docs.opencv.org/4.5.2/d8/d6a/group__imgcodecs__flags.html#ga292d81be8d76901bff7988d18d2b42ac
        b64_bytes = base64.b64encode(buffer)
        b64_string = b64_bytes.decode()

        clips.append(b64_string)
    return clips

def get_cropped_words(user_id, date_range=None, complexity_metric="len_count", format=".webp"):
    """
    Function produces a line graph of a student's squad scores over time

        Input:
            `user_id` str - a string containing the username
            `date_range` list - a list of two dates in the format of YYYY-MM-DD
            `complexity_metric` str - how to calculate the complexity of words (from 'len', 'syl', 'len_count', 'syl_count')
            `format` str - the format of the cropped word images (from 'png', 'webp', or anything OpenCSV supports)

        Output: A csv table of the cropped words
    """

    page_fetcher = PageQuery()
    pages = page_fetcher.get_pages(user_id=user_id, date_range=date_range)
    print(f"{len(pages)} pages match those parameters")

    user_words = pd.DataFrame()
    for page_url, date in zip(pages["image_url"], pages["submission_datetime"]):
        page_data = parse_page(page_url, date, format)
        user_words = pd.concat([user_words,page_data])

    user_words.drop(columns=['left', 'top', 'conf'], inplace=True, errors='ignore')
    if len(pages) > 0:
        user_words.sort_values(by='complexity', ascending=False, inplace=True)
    words_csv = user_words.to_csv(index=False)
    words_json = json.dumps(words_csv)
    return words_json

if __name__ == "__main__":
    words_json = get_cropped_words(
        user_id="XiChi",
        date_range=("2019-08-26","2020-12-31"),
        complexity_metric="len_count",
        format=".webp",
        )
    print(f"The table is {len(words_json):,d} bytes")
    print(words_json)