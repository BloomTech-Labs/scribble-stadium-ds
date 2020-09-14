from fastapi import APIRouter
import logging
from json import dumps
from pydantic import BaseModel, Field, validator
from requests import get, post

router = APIRouter()
log = logging.getLogger(__name__)


class Submission(BaseModel):
    """Data Model to parse Request body JSON, using the Default values
    will check if the s3 API server is currently accepting requests"""

    story_id: str = Field(..., example="12345")
    story_url: str = Field(..., example="https://s3.amazonaws.com")

    def to_json(self):
        "returns the json representation of the object"
        return dumps(dict(self))

    @validator("story_url")
    def story_exists_in_bucket(cls, value):
        """checks to make sure that the value that is passed in story_url is a
        real address that has a good response code"""
        try:
            # let the server know this is a temporary connection
            r = get(value, headers={"Keep-alive": False})
            assert r.status_code == 200
            r.close()
            return value
        except AssertionError as ae:
            # pass forward the AssertionError
            raise ae
        except Exception as e:
            # add cause message and args to the log handler
            log.warning(e.__cause__, e.args)
            return {"ERROR": e.__cause__}

    @validator("story_id")
    def no_none_ids(cls, value):
        """Ensure that the value is not passed as None"""
        assert value is not None
        return value


@router.post("/submission/text")
async def submission_text(sub: Submission):
    """Function that takes a Submission object from a post request and
    queries the Google API for a transcription of the picture that is passed,
    then stores that transcription along with the story_id in a PostgreSQL
    Database
    ## Arguments:
    -----------

    sub {Submission} - submission model that is created on post

    ## Returns:
    -----------

    json - {"is_flagged": bool}
    """
    # @XXX: change this to the result of the moderation search,
    # for testing just echo
    return sub.to_json()


@router.post("/submission/image")
async def submission_image(sub: Submission):
    """Identical to /submission/text except that it just flags
    inappropriate content in the submission to be reviewed by admins"""
    return sub.to_json()

