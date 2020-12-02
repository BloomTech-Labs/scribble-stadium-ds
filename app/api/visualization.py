import logging

from fastapi import APIRouter

from app.utils.security.header_checking import AuthRouteHandler
from app.api.models import HistogramRequest, LineGraphRequest
from app.utils.visualizations import histogram, line_graph

# global variables and services
router = APIRouter(route_class=AuthRouteHandler)
log = logging.getLogger(__name__)


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
