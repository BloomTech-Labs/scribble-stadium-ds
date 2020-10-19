import logging

from fastapi import APIRouter

from app.utils.security.header_checking import AuthRouteHandler
from app.api.models import HistogramRequest, LineGraphRequest

# global variables and services
router = APIRouter(route_class=AuthRouteHandler)
log = logging.getLogger(__name__)


@router.route("/viz/linegraph")
def return_line_graph(data: LineGraphRequest):
    pass


@router.route("/viz/histogram")
def return_histogram(data: HistogramRequest):
    pass
