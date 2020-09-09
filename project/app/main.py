from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from fastapi.requests import Request
from os import getenv
import uvicorn

from app.api import predict, viz

app = FastAPI(
    title="Labs26-StorySquad-DS-Team B",
    description="A RESTful API for the Story Squad Project",
    version="0.1",
    docs_url="/",
)


@app.middleware("http")
async def check_auth_header(request: Request, next_call):
    """
    Function acts as a custom middleware for http requests, checks if the
    request header contains Authorization and if the value is equal to the
    expected value that is stored in memory.
    Arguments
    -----------
    `request`: {fastapi.requests.Request} - requesting client
    `next_call`: {typing.Callable} - callable function that the middleware
    is intercepting
    Returns
    ---------
    `response`: {fastapi.responses.Response} - response from calling the
    function
    """
    bad_response = Response(
        status_code=403, content="PATH FORBIDDEN", media_type="text/html"
    )
    if request.base_url.path == "/":
        response = await next_call(request)
        return response

    # check for key in headers, doesn't cause an error to raise
    if "Authorization" in request.headers:
        auth = request.headers["Authorization"]
        # make sure that auth token is set to a value, and that that value is
        # what we expect
        if (auth is not None) and (auth == getenv("DS_SECRET_TOKEN", None)):
            response = await next_call(request)
            return response
        else:
            return bad_response
    else:
        return bad_response


app.include_router(predict.router)
app.include_router(viz.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app)
