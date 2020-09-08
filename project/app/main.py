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
    try:
        auth = request.headers["Authorization"]
        if (auth is not None) and (auth == getenv("DS_SECRET_TOKEN", None)):
            response = await next_call(request)
            return response
    except KeyError:
        return Response(status_code=403, content="PATH FORBBIDEN", media_type='text/html')


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
