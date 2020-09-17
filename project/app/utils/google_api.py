# Google Vision function to extract text from a local or uri hosted image

from google.cloud import vision
from google.cloud.vision import types
from os import getenv, environ

"""An interface to googles vision API"""


class GoogleAPI:
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

    async def transcribe(self, image_file: bytes):
        """
        Detects document features in images and returns extracted text
        Input: Path to file where images are stored
            - Assuming 1 image per image_path
            - Code for both local image_path and remote image_path, comment out
                the appropriate one
        Output: Transcribed text as a string
        """
        # read the file's content and cast into Image type
        # use async friendly await function to fetch read
        content = await image_file.read()
        image = types.Image(content=content)
        # Connect to Google API client with the file that is built above
        response = self.client.document_text_detection(image=image)
        # Save transcribed text
        if response.text_annotations:
            transcribed_text = response.text_annotations[0].description
            transcribed_text = transcribed_text.replace("\n", " ")
        else:
            raise NoTextFoundException("No Text Was Found In Image")
        return transcribed_text

    async def detect_safe_search(self, image_file: bytes):
        """
        Detects adult, violent or racy content in uploaded images
        Input: path to the image file
        Output: String, either stating 'No inappropriate material detected'
            or 'Image Flagged' with information about what is inappropriate
        """
        # init a empty list
        flagged = []
        # read the file's content and cast into Image type
        # use async friendly await function to fetch read
        content = await image_file.read()
        image = types.Image(content=content)
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
    pass
