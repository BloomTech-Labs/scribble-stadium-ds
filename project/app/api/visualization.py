import logging

from fastapi import APIRouter

from app.utils.security.header_checking import AuthRouteHandler
from app.api.models import HistogramRequest, LineGraphRequest
from app.utils.visualizations import histogram, line_graph

# global variables and services
router = APIRouter(route_class=AuthRouteHandler)
log = logging.getLogger(__name__)


@router.route("/viz/linegraph")
def return_line_graph(data: LineGraphRequest):
    """Endpoint produces a line graph of a student's squad scores over time

    Input: A list containing the history of the students scores, in
    chronological order. And student's name.

    Output: Plotly JSON for web to display using plotly.js on the
    parent dashboard
    """
    return line_graph.line_graph(data.ScoreHistory, data.StudentName)


@router.route("/viz/histogram")
def return_histogram(data: HistogramRequest):
    """Endpoint that makes Plotly histogram of all of the submission scores for
    the student's grade for the current week. Plots a vertical line for the
    student's most recent score so they can see how it compares to the rest
    of the grade.

    Input:
    List of the current week's scores for the specific grade level

    Student information in a list in this order:
    [grade_number, student_name, student_score]

    Output: Plotly JSON that can be passed to the web to display on the
    parent dashboard
    """
    return histogram.histogram(
        data.GradeList, [data.GradeLevel, data.StudentName, data.StudentScore]
    )
