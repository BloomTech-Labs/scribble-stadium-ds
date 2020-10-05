import logging
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel, Field, validator
from app.utils.img_processing.google_api import GoogleAPI, NoTextFoundException
import json
import sys

router = APIRouter()
log = logging.getLogger(__name__)
# init the GoogleAPI service to fetch responses from the google vision api
vision = GoogleAPI()


class Submission(BaseModel):
    """
    # Model that handles text submissions to the API `submission/text` endpoint
    ## **Fields:**

    ### SubmissionID - `int`
    <p>
        SubmissionID unique to this submission from a specific student
    </p>

    ### StoryId - `int`
    <p>
        StoryID for keeping track of which story the submission is in reference to
    </p>

    ### Pages - `dict`
    <p>
        A dictionary containing page number keys and value dictionaries with the
        following keys:
    </p>

    ```python3
    {
        "URL": # The url to the file that will be downloaded for transcription
        "Checksum": # Checksum for the file that is downloaded to verify it's file integrity
    }
    ```

    ## **Validation Functions:**

    ### **check_valid_subid(cls, value)** uses `SubmissionID`

    `Asserts that: 0 < SubmissionID < sys.maxsize`
    <p>
        Function is used to make sure that the passed value for SubmissionID
        is not negative and does not cause an integer overflow.
    </p>

    ### **check_sha_len(cls, value)** uses `Pages`

    <p>
        Function that takes the value of checksum and assert that it's 128
        characters long to ensure that it's the proper length for a SHA512
        checksum.
    </p>
    """
    SubmissionID: int = Field(..., example=123564)
    StoryId: int = Field(..., example=154478)
    Pages: dict = Field(
        ...,
        example={
            "1": {
                "URL": "link",
                "Checksum": "1f40fc92da241694750979ee6cf582f2d5d7d28e18335de05abc54d0560e0f5302860c652bf08d560252aa5e74210546f369fbbbce8c12cfc7957b2652fe9a75"
            },
            "2": {
                "URL": "link",
                "Checksum": "1f40fc92da241694750979ee6cf582f2d5d7d28e18335de05abc54d0560e0f5302860c652bf08d560252aa5e74210546f369fbbbce8c12cfc7957b2652fe9a75"
            }
        })

    @validator("SubmissionID")
    def check_valid_subid(cls, value):
        # no neg numbers and no int overflows
        assert value >= 0
        assert value < sys.maxsize
        return value
    @validator("Pages")
    def check_sha_len(cls, value):
        for page in value:
            assert len(value[page]["Checksum"]) == 128
        return value


class ImageSubmission(BaseModel):
    """
    # Model that handles illustration submissions to the API `submission/illustration` endpoint
    ## **Fields:**

    ### SubmissionID -
    <p>
        Submission id that is passed to identify the illustration
        for moderation purposes
    </p>

    ### URL -
    <p>
        Url to the file that is going to be submitted to Google API
    </p>

    ### Checksum -
    <p>
        SHA512 checksum of the file to verify the integrity of the
        downloaded file
    </p>

    ## **Validation Functions:**

    ### **check_valid_subid(cls, value)** uses `SubmissionID`

    `Asserts that: 0 < SubmissionID < sys.maxsize`

    <p>
        Function is used to make sure that the passed value for SubmissionID
        is not negative and does not cause an integer overflow.
    </p>
    <br>

    ### **check_sha_len(cls, value)** uses `Checksum`

    <p>
        Function that takes the value of checksum and assert that it's 128
        characters long to ensure that it's the proper length for a SHA512
        checksum.
    </p>
    """
    SubmissionID: int = Field(..., example=265458)
    URL: str = Field(..., example="s3.link.com/path/to/file.end")
    Checksum: str = Field(..., example="1f40fc92da241694750979ee6cf582f2d5d7d28e18335de05abc54d0560e0f5302860c652bf08d560252aa5e74210546f369fbbbce8c12cfc7957b2652fe9a75")

    @validator("SubmissionID")
    def check_valid_subid(cls, value):
        # no neg numbers and no int overflows
        assert value >= 0
        assert value < sys.maxsize
        return value

    @validator("Checksum")
    def check_sha_len(cls, value):
        assert len(value) == 128
        return value


class ScoreSquad():
    """placeholder class for now"""
    def __init__(self, document: str):
        self.score = len(document.split())

    def get_score(self):
        return self.score


@router.post("/submission/text")
async def submission_text(sub: Submission):
    """will update in future
    """
    # unpack links for file sin submission object
    # featcha  list of files from s3 server
    # check the SHA 512 of the file that is featched from the s3 bucket
    # send each file to transcription service to be transcribed
    # send transcriptions to complexity score
    # send complexity score to web callback with the submission ID


    # catch custom exception for no text
    try:
        # await for the vision API to process the image
        #transcript = await vision.transcribe()

    # log the error then return what the error is
    except NoTextFoundException as e:
        log.error(e, stack_info=True)
        return {"error": e}

    return


@router.post("/submission/illustration")
async def submission_illustration(sub: ImageSubmission):
    """Function that checks the illustration against the Google Vision
    SafeSearch API and flags if explicit content detected.

    ## Arguments:
    -----------
    files `UploadFile` - UGC to be uploaded, transcribed, and stored

    eg.
    ```python3
    files = {"files": (file.name, file)}
    ```

    ## Returns:
    -----------

    response `json` - {"is_flagged": bool, "reason":`reason`}
    """

    response = await vision.detect_safe_search(files)
    return response
