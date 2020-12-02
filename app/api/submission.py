from hashlib import sha512
import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from requests import get

from app.utils.complexity.squad_score import squad_score, scaler
from app.utils.img_processing.google_api import GoogleAPI, NoTextFoundException
from app.utils.security.header_checking import AuthRouteHandler
from app.api.models import Submission, ImageSubmission

# global variables and services
router = APIRouter(route_class=AuthRouteHandler)
log = logging.getLogger(__name__)
vision = GoogleAPI()


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
            # assert that the hash is the same as the one passed with the file
            # link
            assert hash.hexdigest() == sub.Pages[page_num]["Checksum"]
        except AssertionError:
            # return some useful information about the error including what
            # caused it and the file affected
            return JSONResponse(
                status_code=422,
                content={"ERROR": "BAD CHECKSUM", "file": sub.Pages[page_num]},
            )
        # unpack response from GoogleAPI
        conf_flag, flagged, trans = await vision.transcribe(r.content)
        # concat transcriptions togeather
        transcriptions += trans + "\n"
        # add page to list of confidence flags
        confidence_flags.append(conf_flag)
    # score the transcription using SquadScore algorithm
    score = await squad_score(transcriptions, scaler)

    # return the complexity score to the web team with the SubmissionID
    return JSONResponse(
        status_code=200,
        content={
            "SubmissionID": sub.SubmissionID,
            "IsFlagged": flagged,
            "LowConfidence": True in confidence_flags,
            "Complexity": score,
        },
    )


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
        return JSONResponse(status_code=422, content={"ERROR": "BAD CHECKSUM"})
    # pass file to the GoogleAPI object to safe search filter the file
    response = await vision.detect_safe_search(r.content)
    # respond with the output dictionary that is returned from
    # GoogleAPI.transcribe() method
    return JSONResponse(status_code=200, content=response)
