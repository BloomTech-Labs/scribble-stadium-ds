import logging

from fastapi import APIRouter

from app.utils.security.header_checking import AuthRouteHandler

# global variables and services
router = APIRouter(route_class=AuthRouteHandler)
log = logging.getLogger(__name__)
