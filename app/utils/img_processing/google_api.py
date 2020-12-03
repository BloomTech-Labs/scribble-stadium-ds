from os import getenv, environ, path

from dotenv import load_dotenv
from google.cloud import vision
from google.cloud.vision import types

from app.utils.moderation.text_moderation import BadWordTextModerator

# XXX: Documentation parses to Markdown on FastAPI Swagger UI
# Attribution: Most of this code is from transcription.py, safe_search.py, and
# confidence_flag.py. To steamline the implementation with the deployed
# environment that code has been refactored into this file.


class GoogleAPI:
    """# An Interface to Google's Vision API"""

    def __init__(self):
        """function that prepares the GoogleAPI to handle requests from the
        endpoints.

        initially, this function will be looking for the environment variable
        GOOGLE_CREDS that hold the content of the credential file from the
        Google API dashboard, as long as this environment variable is set this
        the function will write a temporary file to /tmp/google.json with that
        content the will set a new variable GOOGLE_APPLICATION_CREDENTIALS
        which is used by ImageAnnotatorClient to authorize the google API library
        """
        # TODO: Refactor into separate function
        load_dotenv()
        if getenv("GOOGLE_CREDS") is not None:
            with open("/tmp/google.json", "wt") as fp:
                # write file to /tmp containing all of the cred info
                fp.write(getenv("GOOGLE_CREDS"))
                # make extra sure that the changes get flushed on to the disk
                fp.flush()
                # explicitly close file stream
                fp.close()
            # update the environment with the environment variable that google
            # sdk is looking for
            environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/google.json"
        else:
            raise RuntimeError("Missing Google Credentials, Exiting app")

        # init the client for use by the functions
        self.client = vision.ImageAnnotatorClient()

        self.text_moderator = BadWordTextModerator(
            path.join(
                path.dirname(__file__), "..", "moderation", "bad_single.csv"
            )
        )

    async def transcribe(self, document):
        """Detects document features in images and returns extracted text
        Input:
        --------
        `document`: bytes - The file object to be sent to Google Vision API

        Output:
        --------
        `transcribed_text`: str - Transcribed text from Google Vision API

        """
        # read the file's content and cast into Image type
        # use async friendly await function to fetch read
        image = types.Image(content=document)
        # adding refined language specification to sort out Non-English
        # characters from transcription responses
        language = types.ImageContext(language_hints=["en-t-i0-handwrit"])
        # Connect to Google API client with the file that is built above
        response = self.client.document_text_detection(
            image=image, image_context=language
        )
        # check if there are transcriptions from google
        if response.text_annotations:
            # store and process the response
            transcribed_text = response.text_annotations[0].description
            transcribed_text = transcribed_text.replace("\n", " ")
        else:
            # forward no text in image exception to caller
            raise NoTextFoundException("No Text Was Found In Image")

        flagged = False
        # List of confidence levels of each character
        symbol_confidences = []
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        # check moderation status of word in paragraph
                        if self.text_moderator.check_word(str(word).lower()):
                            flagged = True
                        for symbol in word.symbols:
                            symbol_confidences.append(symbol.confidence)
        # Calculate the overall confidence for the page
        page_confidence = sum(symbol_confidences) / len(symbol_confidences)

        # return flag: True under 85% confident, False 85% confident or over
        # return text transcription
        return (page_confidence < 0.85), flagged, transcribed_text

    async def detect_safe_search(self, document):
        """# Detects adult, violent or racy content in uploaded images

        ## Input:
        --------
        `document`: bytes - The file object to be sent to Google Vision API

        ## Output:
        --------
        response `dict` - a dictionary that contains the following keys:

        ```python3
        {
            # bool to signal moderation
            "is_flagged": [ True / False ],
            "reason": {
                        # probabilities of each metric
                        # occuring in the sourced image
                        "adult:": P(adult)
                        "violence": P(violence)
                        "racy": P(racy)
                      } or None
        }
        ```

        The possible values for the posibilities are:

        ```
            "UNKNOWN",
            "VERY_UNLIKELY",
            "UNLIKELY",
            "POSSIBLE",
            "LIKELY",
            "VERY_LIKELY",
        ```

        """
        # init a empty list
        flagged = []
        image = types.Image(content=document)
        # call safe_search_detection search on the image
        response = self.client.safe_search_detection(image=image)
        safe = response.safe_search_annotation
        # Names of likelihood from google.cloud.vision.enums
        likelihood_name = (
            "UNKNOWN",
            "VERY_UNLIKELY",
            "UNLIKELY",
            "POSSIBLE",
            "LIKELY",
            "VERY_LIKELY",
        )
        # Check illustration against each safe_search category
        # Flag if inappropriate material is 'Possible' or above
        if safe.adult > 2 or safe.violence > 2 or safe.racy > 2:
            # Set flag - provide information about what is inappropriate
            flagged = [
                ("adult: {}".format(likelihood_name[safe.adult])),
                ("violence: {}".format(likelihood_name[safe.violence])),
                ("racy: {}".format(likelihood_name[safe.racy])),
            ]
        # return in API friendly format
        if flagged != []:
            return {"is_flagged": True, "reason": flagged}
        else:
            return {"is_flagged": False, "reason": None}


class NoTextFoundException(Exception):
    """An Exception that occurs when Google Vision API
    finds no text data in the image"""

    pass
