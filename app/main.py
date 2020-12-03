from os import getenv

from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from fastapi.requests import Request
import uvicorn

from app.api import submission, visualization, clustering, db
from app.utils.security.header_checking import get_api_key

app = FastAPI(
    title="Labs26-StorySquad-DS-Team B",
    description="A RESTful API for the Story Squad Project",
    version="0.1",
    docs_url="/"
)

app.include_router(submission.router, tags=['Submission'], dependencies=[Security(get_api_key)])
app.include_router(visualization.router, tags=['Visualization'], dependencies=[Security(get_api_key)])
app.include_router(clustering.router, tags=['Clustering'], dependencies=[Security(get_api_key)])
app.include_router(db.router, tags=['Database'], dependencies=[Security(get_api_key)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app)
