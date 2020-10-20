import logging

from fastapi import APIRouter, Response

from app.utils.security.header_checking import AuthRouteHandler
from app.utils.clustering.clustering_mvp import batch_cluster


# global variables and services
router = APIRouter(route_class=AuthRouteHandler)
log = logging.getLogger(__name__)


@router.post("/cluster")
async def cluster_endpoint(sub: dict):
    """Endpoint takes a list of cohort and submission objects then returns
    clusters based on cohort in groups of 4.

    Arguments:
    ---

    sub (dict): Submission Object Defined by the following form:
    ```
        {
            "1": { # cohortID
                "1": { # submissionID
                    "Image": "http://lorempixel.com/640/480/abstract",
                    "Inappropriate": False,
                    "Sensitive": False,
                    "Status": "APPROVED",
                    "Complexity": 123,
                    "Pages": {
                        "1": "http://lorempixel.com/640/480/abstract",
                        "2": "http://lorempixel.com/640/480/abstract",
                    },
                },
            },
            "2":{
                "1": {
                    "Image": "http://lorempixel.com/640/480/abstract",
                    "Inappropriate": False,
                    "Sensitive": False,
                    "Status": "APPROVED",
                    "Complexity": 123,
                    "Pages": {
                        "1": "http://lorempixel.com/640/480/abstract",
                        "2": "http://lorempixel.com/640/480/abstract",
                    },
                },
            },
        }
    ```

    Returns:
    ---
    `response` json - a list of clusters defined by the following form:
    {
        "1": [["1","2","3","4"]], # CohortID: [Group1[SubmissionIDs],GroupN]
        "2": [["5","6","7","8"]]
    }

    Note:
    ---
    All submissions that are included in this data are post moderation review
    and Approved for COPPA compliance
    """
    response = await batch_cluster(sub)
    return response
