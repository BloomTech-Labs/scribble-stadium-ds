import sys

from pydantic import BaseModel, Field, validator


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
