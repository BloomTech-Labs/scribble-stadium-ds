import logging
from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel, Field, validator

router = APIRouter()
log = logging.getLogger(__name__)


class Submission(BaseModel):
    """Data Model to parse Request body JSON, using the Default values
    will check if the s3 API server is currently accepting requests"""

    story_id: str = Field(..., example="12345")
    story_file: bytes = Field(..., example=b"10gh1r447/s4413.")

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
async def submission_text(sub: Submission):
    """This function takes the passed file in Submission and calls two services,
    one that uses the Google Vision API and transcribes the text from the file
    and looks for moderation markers. the other service will take the binary
    file and upload it to an e3 bucket. after the file has been transcribed,
    moderated, and stored there will be an entry added to a submissions
    database with the story_id, s3_path, and the text data from the
    transcription

    ## Arguments:
    -----------

    sub {Submission} - submission model that is created on post

    ## Returns:
    -----------

    json - {"is_flagged": bool, "s3_link": type(url)}
    """
    return {sub}


@router.post("/submission/illustration")
async def submission_illustration(sub: Submission):
    """Function that takes an illustration from form data and checks the
    illustration against the google.cloud.vision api and see's if the content
    is NSFW

    ## Arguments:
    -----------

    sub {Submission} - submission model that is created on post

    ## Returns:
    -----------

    json - {"is_flagged": bool, "s3_link": type(url)}"""
    return {sub}
