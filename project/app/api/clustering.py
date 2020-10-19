import logging
import json

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

from app.utils.security.header_checking import AuthRouteHandler
from app.utils.clustering.clustering_mvp import batch_cluster
from app.api.models import ClusterSubmission


# global variables and services
router = APIRouter(route_class=AuthRouteHandler)
log = logging.getLogger(__name__)


@router.post("/cluster")
async def cluster_endpoint(sub: dict):

    response = await batch_cluster(sub)
    return response

