import logging
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel, Field, validator
from app.utils.google_api import GoogleAPI, NoTextFoundException
import json

router = APIRouter()
log = logging.getLogger(__name__)
# init the GoogleAPI service to fetch responses from the google vision api
vision = GoogleAPI()


class Submission(BaseModel):
    """URL: '', PageNum: 12, SubmissionID: 12, checksum: ''"""

    subId: int = Field(..., example=123564)
    storyId: int = Field(..., example=154478)
    pages: dict = Field(
        ...,
        example={
            "URL": '',
            "PageNum": 12,
            "SubmissionID": 12,
            "checksum": 'acde123345sfd3324jhg34vbj32v4'
        })


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
        transcript = await vision.transcribe(page_file)

    # log the error then return what the error is
    except NoTextFoundException as e:
        log.error(e, stack_info=True)
        return {"error": e}

    return


@router.post("/submission/illustration")
async def submission_illustration(sub: Submission):
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
