import os
from hashlib import sha512
import logging
from app.utils.img_processing.tesseract_api import TesseractAPI
import re

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from requests import get

from app.utils.complexity.squad_score import squad_score, scaler
from app.utils.img_processing.google_api import GoogleAPI, NoTextFoundException
from app.api.models import Submission, ImageSubmission

# Allows user to set environment variable to use different Tesseract model
OCR_MODEL = os.getenv("OCR_MODEL", default="storysquad")

# Global variables and services
router = APIRouter()
log = logging.getLogger(__name__)
# Google Vision is used for drawings so is needed regardless if Tesseract is used for OCR
google_vision = GoogleAPI() 
tesseract_vision = TesseractAPI(OCR_MODEL)


@router.post("/submission/text")
def submission_text(sub: Submission):
    """
    Takes a Submission Object and calls the API (Google or Tesseract) to text annotate
    the passed s3 link, then passes those concatenated transcriptions to the SquadScore
    method, returns:

    Arguments:
    ---
    `sub`: Submission - Submission object **see `help(Submission)` for more info**
    
    Returns:
    ---
    ```
    {"SubmissionID": int, "IsFlagged": boolean, "LowConfidence": boolean, "Complexity": int}
    ```
    """
    # Set model for OCR, checks for Google Vision API Keys
    if sub.Model == "tesseract":
        vision = tesseract_vision
    else:
        vision = google_vision

    # Empty variables for transcription, confidence flags
    # QUESTION: Also need for moderation flags? 
    transcriptions = ""
    confidence_flags = []

    # Use OCR engine on each page in submission
    for page_num in sub.Pages:
        
        # Verify validity of page link:
        # Re-init sha algorithm for every file 
        hash = sha512()
        # Fetch file from s3 bucket
        r = get(sub.Pages[page_num]["URL"])
        # Update the hash with the file's content
        hash.update(r.content)
        try:
            # Assert hash is same as the one passed with the file link
            assert hash.hexdigest() == sub.Pages[page_num]["Checksum"]
        except AssertionError:
            # Return some info on error including cause and file affected
            return JSONResponse(
                status_code=422,
                content={"ERROR": "BAD CHECKSUM", "file": sub.Pages[page_num]},
            )
        
        # Execute OCR to obtain text, confidence flag, moderation flag for page
        conf_flag, content_flagged, trans = vision.transcribe(r.content)
        # Add text to transcription
        transcriptions += trans + "\n"
        # Add confidence to list of confidence flags
        confidence_flags.append(conf_flag)
        # Add moderation flag to list of moderation flags
        # NOT IMPLEMENTED / NEEDED?? / SEE BELOW

    # Score transcription using SquadScore algorithm
    score = squad_score(transcriptions, scaler)

    # Count words in entire submission
    cleaned = re.sub("[^-9A-Za-z ]", "", transcriptions).lower()
    cleaned_words_count = len(cleaned.split())
    
    # Return complexity score, other data to web team with the SubmissionID
    return JSONResponse(
        status_code=200,
        content={
            "SubmissionID": sub.SubmissionID,
            "IsFlagged": content_flagged,  # QUESTION: Is this returning only the flag for the last page? (see above)
            "LowConfidence": True in confidence_flags,
            "Complexity": score,
            "WordCount": cleaned_words_count  
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
    response = google_vision.detect_safe_search(r.content)
    # respond with the output dictionary that is returned from
    # GoogleAPI.transcribe() method
    return JSONResponse(status_code=200, content=response)
