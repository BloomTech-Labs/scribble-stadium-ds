import logging
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel, Field, validator
from app.utils.google_api import GoogleAPI, NoTextFoundException
import json
import sys

router = APIRouter()
log = logging.getLogger(__name__)
# init the GoogleAPI service to fetch responses from the google vision api
vision = GoogleAPI()


class Submission(BaseModel):
    """URL: '', PageNum: 12, SubmissionID: 12, checksum: ''"""

    SubmissionID: int = Field(..., example=123564)
    StoryId: int = Field(..., example=154478)
    Pages: dict = Field(
        ...,
        example={
            "1": {
                "URL": "link",
                "Checksum": "nla1snkj2fasn44423332sdafv"
            },
            "2": {
                "URL": "link",
                "Checksum": "3alksjdfljwerproifjkmtrews"
            }
        })
    @validator("SubmissionID")
    def check_valid_subid(cls, value):
        # no neg numbers and no int overflows
        assert value >= 0
        assert value < sys.maxsize


class ImageSubmission(BaseModel):
    """request model of image submissions contains a validator for SubmissionID
    where 0 < SubmmisionID < 9223372036854775807 (sys.maxsize or 0x7FFFFFFF)"""

    URL: str = Field(..., example="s3.link.com/path/to/file.end")
    Checksum: str = Field(..., example="alkjsfdljaefnrgit2344asfd4")
    SubmissionID: int = Field(..., example=265458)

    @validator("SubmissionID")
    def check_valid_subid(cls, value):
        # no neg numbers and no int overflows
        assert value >= 0
        assert value < sys.maxsize


class ScoreSquad():
    """placeholder for now"""
    def __init__(self, document: str):
        self.score = len(document.split())

    def get_score(self):
        return self.score


@router.post("/submission/text")
async def submission_text(sub: Submission):
    """will update in future
    """

    # catch custom exception for no text
    try:
        # await for the vision API to process the image
        #transcript = await vision.transcribe()
        for page in sub.pages:
            print(page, sub.pages[page])
    # log the error then return what the error is
    except NoTextFoundException as e:
        log.error(e, stack_info=True)
        return {"error": e}

    return


@router.post("/submission/illustration")
async def submission_illustration(imgsub: ImageSubmission):
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
