from os.path import dirname
from dotenv import load_dotenv
from app.utils.moderation.text_moderation import BadWordTextModerator

from cv2 import imdecode, cvtColor, IMREAD_COLOR, COLOR_BGR2RGB
from pytesseract import image_to_string
import numpy as np

# Get name of directory where this file is located
DIR = dirname(__file__)

# Setup globals
BAD_WORDS_CSV = DIR + '/../moderation/bad_single.csv'
MODEL_DIR = DIR + '/../../../models/'
TESSDATA_DIR = MODEL_DIR

# Tell tesseract to look in TESSDATA_DIR for lang trainedata files
TESS_CONFIG = f'--tessdata-dir "{TESSDATA_DIR}"'


class TesseractAPI:
    """
    Interface to Tesseract OCR engine
    Takes single image page and returns transcribed text
    """

    def __init__(self, lang='storysquad'):
        """
        Arguments:
        Tesseract model (default is 'storysquad')
        
        Actions:
        Prepares TesseractAPI to handle requests from the endpoints
        """

        load_dotenv() 
        self.text_moderator = BadWordTextModerator(BAD_WORDS_CSV)
        self.lang = lang

    def img_preprocess(self, image):
        """
        Arguments:
        Single full-page image

        Actions:
        1. Convert image data bytestring to image object
        2. Convert order of image colors from BGR to RGB

        Returns:
        Full-page processed image
        """

        # 1. Convert bytestring to image object
        nparr = np.fromstring(image, np.uint8)
        processed_img = imdecode(nparr, IMREAD_COLOR)

        # 2. Convert image from BGR to RGB
        processed_img = cvtColor(image, COLOR_BGR2RGB)

        # Return processed image
        return processed_img

    def extract_text(self, image):
        """
        Arguments:
        Single full-page image

        Actions:
        1. Extract text from image with Tesseract OCR
        2. Moderate content
        3. Calculate confidence (not implemented)
        
        Returns:
        1. Transcribed text (string)
        2. Bad content flag (T/F)
        3. Low confidence flag (T/F) (currently False as not implemented)
        """

        # 1. Extract text from image using Tesseract OCR
        text = image_to_string(
            image, lang=self.lang, config=TESS_CONFIG)

        # 2. Moderate content by checking all words in text
        content_flagged = False
        for word in text:
            if self.text_moderator.check_word(str(word).lower()):
                content_flagged = True

        # 3. Calculate confidence
        # NOT IMPLEMENTED
        low_confidnce = False

        # Return confidence flag, moderation flag, text
        return low_confidnce, content_flagged, text

    async def transcribe(self, image):
        """
        Arguments:
        Single full-page image

        Actions:
        1. Preprocesses image
        2. Extract text, moderate content, get confidence

        Returns:
        1. Transcribed text (string)
        2. Bad content flag (T/F)
        3. Low confidence flag (T/F)
        """
        
        # Preprocess image
        features = self.img_preprocess(image)
        # Extract text, moderate content, get confidence
        text, content_flagged, low_confidnce = self.extract_text(features)
        
        # Return confidence flag, moderation flag, text
        return low_confidnce, content_flagged, text
