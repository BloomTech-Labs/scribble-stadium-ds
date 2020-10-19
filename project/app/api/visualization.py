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
    return line_graph.line_graph(data.ScoreHistory, data.StudentName)


@router.route("/viz/histogram")
def return_histogram(data: HistogramRequest):
    return histogram.histogram(
        data.GradeList, [data.GradeLevel, data.StudentName, data.StudentScore]
    )
