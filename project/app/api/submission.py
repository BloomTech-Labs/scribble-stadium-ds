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
    """Data Model to parse Request body JSON, using the Default values
    will check if the s3 API server is currently accepting requests"""

    story_id: str = Field(..., example="12345")
    story_file: str = Field(..., example=b"10gh1r447/s4413.")

    @validator("story_id")
    def no_none_ids(cls, value):
        """Ensure that the value is not passed as None"""
        assert value is not None
        return value

    @validator("story_file")
    def check_file(cls, value):
        # design method to validate file contents
        # XXX: (passing a hash then comparing that?)
        # assert hashlib.sha256(data=file).hexdigest() == passed_hash
        return value


@router.post("/submission/text")
async def submission_text(story_id: str, files: UploadFile = File(...)):
    """This function takes the passed file in Submission and calls two services,
    one that uses the Google Vision API and transcribes the text from the file
    and looks for moderation markers. the other service will take the binary
    file and upload it to an e3 bucket. after the file has been transcribed,
    moderated, and stored there will be an entry added to a submissions
    database with the story_id, s3_path, and the text data from the
    transcription

    ## Arguments:
    -----------
    story_id `str` - story_id
    story_file `UploadFile` - UGC passed with enctype=multipart/form-data

    ## Returns:
    -----------

    response `json` - {"is_flagged": bool, "s3_link": type(url)}
    """
    # catch custom exception for no text
    try:
        # await for the vision API to process the image
        transcript = await vision.transcribe(files)
        story_id = story_id

    # log the error then return what the error is
    except NoTextFoundException as e:
        log.error(e, stack_info=True)
        return {"error": e}
    print((story_id, transcript))

    # return moderation flag and s3_link for that file (not yet implemented)
    return {"is_flagged": None, "s3_path": None}


@router.post("/submission/illustration")
async def submission_illustration(files: UploadFile = File(...)):
    """Function that checks the illustration against the google.cloud.vision
    api and see's if the content is NSFW.

    ## Arguments:
    -----------
    files `UploadFile` - UGC to be uploaded, transcribed, and stored

    eg.
    ```python3
    files = {"files": (file.name, file)}
    ```

    ## Returns:
    -----------

    response `json` - {"is_flagged": bool, "reason":`reason`}"""
    response = await vision.detect_safe_search(files)
    return response

