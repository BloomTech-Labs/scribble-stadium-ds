import logging

from fastapi import APIRouter

from app.api.models import HistogramRequest, LineGraphRequest, CropCloudRequest
from app.utils.visualizations import histogram, line_graph, crop_cloud

# global variables and services
router = APIRouter()
log = logging.getLogger(__name__)

# New experiment
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

@router.post("/viz/linegraph")
def return_line_graph(data: LineGraphRequest):
    """Endpoint produces a line graph of student's SquadScore history.

    Arguments
    ---
    `ScoreHistory` list - list with history of squadscores for current period

    `StudentName` str - String containing the student's first name

    Returns:
    ---
    `response` json - A graph object produced by Plotly.Graph.to_json() function

    Note:
    ---
    All submissions that are included in this data are post moderation review
    and Approved for COPPA compliance
    """
    return line_graph.line_graph(data.ScoreHistory, data.StudentName)


@router.post("/viz/histogram")
def return_histogram(data: HistogramRequest):
    """Endpoint that makes Plotly histogram of current grade's SquadScore
    distribution for the current period. Graph is annotated with a vertical line
    representing the student's most recent score that has passed the moderation
    phase of submission processing.

    Arguments:
    ---
    `GradeList` list - list containing the other student's scores from this week

    `GradeLevel` int - Current grade level for student

    `StudentName` str - String containing the student's first name

    `StudentScore` float - current student's submission score

    Returns:
    ---
    `response` json - A graph object produced by Plotly.Graph.to_json() function

    Note:
    ---
    All submissions that are included in this data are post moderation review
    and Approved for COPPA compliance
    """
    return histogram.histogram(
        data.GradeList, [data.GradeLevel, data.StudentName, data.StudentScore]
    )

@router.get("/viz/cropped_words")
def return_crop_cloud(data: CropCloudRequest):
    """Endpoint produces a crop cloud of the student's progression in handwritting over time.

    Arguments
    ---
    `user_id` str - a string containing the username
    `date_range` list - a list of two dates in the format of YYYY-MM-DD
    `complexity_metric` str - how to calculate the complexity of words (from 'len', 'syl', 'len_count', 'syl_count')
    `format` str - the format of the cropped word images (from 'png', 'webp', or anything OpenCSV supports)

    Returns:
    ---
    `response` json - a csv table of the cropped words

    Note:
    ---
    All submissions that are included in this data are pre moderation review
    and not Approved for COPPA compliance
    """
    return crop_cloud.get_cropped_words(
        user_id=data.user_id,
        date_range=data.date_range,
        complexity_metric=data.complexity_metric,
        format=data.image_format,
        )
