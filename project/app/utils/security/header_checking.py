from typing import Callable
from os import getenv

from fastapi import Request, Response, APIRouter
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from pydantic import ValidationError

from app.utils.img_processing.google_api import NoTextFoundException


class AuthRouteHandler(APIRoute):
    """Custom APIRoute handler that checks the authorization header for
    secret value
    more information about this method for overriding the APIRouter handling can be found here:
    https://fastapi.tiangolo.com/zh/advanced/custom-request-and-route/
    """
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                auth = getenv("DS_SECRET_TOKEN")
                auth_header_value = request.headers.get("authorization")
                assert (auth is not None) and (auth == auth_header_value)
                response: Response = await original_route_handler(request)
                return response
            # bad auth or null token to check against
            except AssertionError:
                return JSONResponse(status_code=403,
                                    content={"ERROR": "USER NOT AUTHORIZED"})
            # POST Validation Error from pydantic
            except ValidationError as ve:
                return Response(status_code=422, content=ve)
            # No Text Found from google API
            except NoTextFoundException:
                return JSONResponse(status_code=452,
                                    content={"ERROR": "GOOGLE:NO TEXT FOUND"})
            # unexpected error
            except Exception as e:
                print(
                    "error at app.utils.security.header_checking.AuthRouteHandler()",
                    e.with_traceback(None))
                return JSONResponse(
                    status_code=500,
                    content={"ERROR": "Unknown error please contact sysadmin"})
            finally:
                # remove secret from memory after using it to authenticate.
                del auth

        return custom_route_handler
