from os.path import dirname
from dotenv import load_dotenv
from app.utils.moderation.text_moderation import BadWordTextModerator

from cv2 import imdecode, cvtColor, IMREAD_COLOR, COLOR_BGR2RGB
from pytesseract import image_to_string
import numpy as np

# Get the name of the directory where this file
# is located.
DIR = dirname(__file__)

# Setup globals
BAD_WORDS_CSV = DIR + '/../moderation/bad_single.csv'
MODEL_DIR = DIR + '/../../../models/'
TESSDATA_DIR = MODEL_DIR

# Tell tesseract to look in the TESSDATA_DIR dir for
# lang trainedata files.
TESS_CONFIG = f'--tessdata-dir "{TESSDATA_DIR}"'


class TesseractAPI:
    """# An Interface to the Tesseract OCR Engine"""

    def __init__(self, lang='storysquad'):
        """function that prepares the TesseractAPI to handle requests from the
        endpoints.

        """
        load_dotenv()

        self.text_moderator = BadWordTextModerator(BAD_WORDS_CSV)
        self.lang = lang

    def img_preprocess(self, img):
        ret = []

        img = cvtColor(img, COLOR_BGR2RGB)

        ret.append(img)

        # Return processed image
        return ret

    async def transcribe(self, document):
        """Detects document features in images and returns extracted text
        Input:
        --------
        `document`: bytes - The file object to be sent to Tesseract OCR Engine

        Output:
        --------
        `transcribed_text`: str - Transcribed text from Tesseract OCR Engine

        """

        # Convert image data bytestring to image object
        nparr = np.fromstring(document, np.uint8)
        img = imdecode(nparr, IMREAD_COLOR)

        img_blocks = self.img_preprocess(img)
        flagged = False

        transcribed_text = []

        for img_block in img_blocks:
            ttext = image_to_string(
                img_block, lang=self.lang, config=TESS_CONFIG)

            for word in ttext:
                # check moderation status of word in paragraph
                if self.text_moderator.check_word(str(word).lower()):
                    flagged = True

            transcribed_text.append(ttext)

        return False, flagged, ' '.join(transcribed_text)
