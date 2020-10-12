from hashlib import sha512
from io import BytesIO
import json
import logging
import sys

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from requests import get

from app.utils.complexity.squad_score import squad_score, scaler
from app.utils.img_processing.google_api import GoogleAPI, NoTextFoundException
from app.utils.security.header_checking import AuthRouteHandler

# global variables and services
router = APIRouter(route_class=AuthRouteHandler)
log = logging.getLogger(__name__)
vision = GoogleAPI()


class Submission(BaseModel):
    """
    # Model that handles text submissions to the API `submission/text` endpoint
    ## **Fields:**

    ### SubmissionID - `int`
    <p>
        SubmissionID used to index the unique student submission to StoryID
        prompt
    </p>

    ### StoryId - `int`
    <p>
        StoryID used to index the writting prompt given to the students
    </p>

    ### Pages - `dict`
    <p>
        A dictionary containing page number keys and value dictionaries with the
        following keys:
    </p>

    ```python3
    {
        "URL": # The url to the file that will be downloaded for transcription
        "Checksum": # Checksum for the file that is downloaded to verify its file integrity
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
                "URL":
                "https://test-image-bucket-14579.s3.amazonaws.com/bucketFolder/1600554345008-lg.png",
                "Checksum":
                "edbd2c0cd247bda620f9a0a3fe5553fb19606929d686ed3440742b1a25df426a8e6d3188b7eec163488764cc72d8cee67faba47e29f7744871d94d2a19dc70de"
            },
            "2": {
                "URL":
                "https://test-image-bucket-14579.s3.amazonaws.com/bucketFolder/1600554345008-lg.png",
                "Checksum":
                "edbd2c0cd247bda620f9a0a3fe5553fb19606929d686ed3440742b1a25df426a8e6d3188b7eec163488764cc72d8cee67faba47e29f7744871d94d2a19dc70de"
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
    URL: str = Field(
        ...,
        example=
        "https://test-image-bucket-14579.s3.amazonaws.com/bucketFolder/1600554345008-lg.png"
    )
    Checksum: str = Field(
        ...,
        example=
        "edbd2c0cd247bda620f9a0a3fe5553fb19606929d686ed3440742b1a25df426a8e6d3188b7eec163488764cc72d8cee67faba47e29f7744871d94d2a19dc70de"
    )

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


@router.post("/submission/text")
async def submission_text(sub: Submission):
    """Takes a Submission Object and calls the Google Vision API to text annotate
    the passed s3 link, then passes those concatenated transcriptions to the SquadScore
    method, returns:
    Arguments:
    ---
    `sub`: Submission - Submission object **see `help(Submission)` for more info**
    Returns:
    ---
    ```
    {"SubmissionID": int, "IsFlagged": boolean,"LowConfidence": boolean, "Complexity": int}
    ```

    """
    transcriptions = ""
    confidence_flags = []
    # unpack links for files in submission object
    for page_num in sub.Pages:
        # re-init the sha algorithm every file that is processed
        hash = sha512()
        # fetch file from s3 bucket
        r = get(sub.Pages[page_num]["URL"])
        # update the hash with the file's content
        hash.update(r.content)
        try:
            # assert that the has is the same as the one passed with the file
            # link
            assert hash.hexdigest() == sub.Pages[page_num]['Checksum']
        except AssertionError:
            # return some useful information about the error including what
            # caused it and the file affected
            return JSONResponse(status_code=422,
                                content={
                                    "ERROR": "BAD CHECKSUM",
                                    "file": sub.Pages[page_num]
                                })
        # add the response from google_api to a string with an ending
        # line break and the confidence flag from the method that determines if
        # the student is reminded about their handwritting
        conf_flag, flagged, trans = await vision.transcribe(r.content)
        transcriptions += trans + "\n"
        confidence_flags.append(conf_flag)
    # score the transcription using SquadScore algorithm
    score = await squad_score(transcriptions, scaler)

    # return the complexity score to the web team with the SubmissionID
    return JSONResponse(status_code=200,
                        content={
                            "SubmissionID": sub.SubmissionID,
                            "IsFlagged": flagged,
                            "LowConfidence": True in confidence_flags,
                            "Complexity": score
                        })


@router.post("/submission/illustration")
async def submission_illustration(sub: ImageSubmission):
    """Function that checks the illustration against the Google Vision
    SafeSearch API and flags if explicit content detected.

    Arguments:
    ---
    sub : ImageSubmission(Object)

    returns:
    ---
    JSON: {"SubmissionID": int, "IsFlagged": boolean, "reason": }
    """
    # fetch file from s3 bucket
    r = get(sub.URL)
    # initalize the sha hashing algorithm
    hash = sha512()
    # update the SHA with the file contents
    hash.update(r.content)
    # assert the the computed hash and the passed hash are the same
    try:
        assert hash.hexdigest() == sub.Checksum
    except AssertionError:
        # return bad hash error with the status_code to an ill-formed request
        return JSONResponse(status_code=422,
                            content={
                                "ERROR": "BAD CHECKSUM",
                            })
    # pass file to the GoogleAPI object to safe search filter the file
    response = await vision.detect_safe_search(r.content)
    # respond with the output dictionary that is returned from
    # GoogleAPI.transcribe() method
    return JSONResponse(status_code=200, content=response)
